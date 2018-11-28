import tkinter as tk  
from othello.planche import Planche
from othello.piece import Piece
from othello.partie import Partie


class Interphace_Othello(tk.Tk):
	""" Classe de l'interphace graphique du jeu othello """

	def __init__(self):
	
		super().__init__()
		self.title("Jeu de othello")

		# Création de la planche de jeux
		self.canvas_othello = Planche_de_jeu(self, 100)
		self.canvas_othello.grid(sticky=tk.NSEW)

		# Pour le redimentionnement
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self.messages = tk.Label(self)
		self.messages.grid()

		# Lien entre le click et la méthode poser_piece()
		self.canvas_othello.bind('<Button-1>', self.jouer_piece)

		# Initialisation de la partie
		self.partie_othello = Partie()

		# Temporaire afficher le joueur courent
		self.messages['text'] = self.partie_othello.couleur_joueur_courant


	def get_info_case(self, event):
		"""
		
		return
			possition: position si une position du jeux, none autrement 
			couleur: couleur de la piece dans la case, none autrement 

		"""
		ligne = event.y // self.canvas_othello.nb_pixels_par_case
		colonne = event.x // self.canvas_othello.nb_pixels_par_case
		position = (ligne, colonne)


		# Selectionne la couleur de la piece, si piece il y a
		if position in self.canvas_othello.cases:
			couleur = self.canvas_othello.cases[position].couleur
		else:
			couleur = None

		if self.canvas_othello.position_valide(position):
			return position, couleur
		else:
			return None, None # Si la position n'est pas valide, il n'y a pas de couleur.

	def jouer_piece(self, event):
		#TODO gestion des erreurs


		pos, couleur_case = self.get_info_case(event)

		if pos != None and couleur_case == None:
			coup_terminer = self.canvas_othello.jouer_coup(pos, self.partie_othello.couleur_joueur_courant)
			
			if coup_terminer == "ok":
				self.canvas_othello.delete('piece')
				self.canvas_othello.dessiner_piece()

			if self.partie_othello.joueur_courant.couleur == "blanc":
				self.partie_othello.joueur_courant = self.partie_othello.joueur_noir
				self.partie_othello.couleur_joueur_courant = "noir"
			else:
				self.partie_othello.joueur_courant = self.partie_othello.joueur_blanc
				self.partie_othello.couleur_joueur_courant = "blanc"

		self.messages['text'] = self.partie_othello.couleur_joueur_courant

			


class Planche_de_jeu(tk.Canvas, Planche):
	""" Classe représentant le canvas de la planche de jeu """

	def __init__(self, parent, nb_pixels_par_case):
        # Héritage de Planche(from othello)
		Planche.__init__(self)
		
		self.nb_lignes = self.nb_cases
		self.nb_colonnes = self.nb_cases
		
		self.chiffre_lignes = [0, 1, 2, 3, 4, 5, 6, 7] 	
		self.chiffre_colonnes = [0, 1, 2, 3, 4, 5, 6, 7] 

		self.nb_pixels_par_case = nb_pixels_par_case

		# Héritage de Cancas(from tkinter)
		super().__init__(parent, width=self.nb_lignes * nb_pixels_par_case,
                                 height=self.nb_colonnes * nb_pixels_par_case)


		self.bind('<Configure>', self.redimensionner)

	def dessiner_cases(self):
		""" Méthode qui dessine la planche d'othello """
		for i in range(self.nb_lignes):
			for j in range(self.nb_colonnes):
				debut_ligne = i * self.nb_pixels_par_case
				fin_ligne = debut_ligne + self.nb_pixels_par_case
				debut_colonne = j * self.nb_pixels_par_case
				fin_colonne = debut_colonne + self.nb_pixels_par_case

				self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill='green', tags='case')

	def dessiner_piece(self):
		""" Méthode qui désine les pièce initiales """

		caracteres_pieces = {'noir': '\u26C2', 'blanc': '\u26C0'}

		for pos in self.cases.keys():
			
			
			coord_x = pos[1] * self.nb_pixels_par_case + self.nb_pixels_par_case // 2
			coord_y = pos[0] * self.nb_pixels_par_case + self.nb_pixels_par_case // 2

			couleur_piece = self.cases[pos].couleur
			

			# Création des pièces
			self.create_text(coord_x, coord_y, text=caracteres_pieces[couleur_piece],
                             font=('Deja Vu', self.nb_pixels_par_case//2), tags='piece')


	def redimensionner(self, event):
		nouvelle_taille = min(event.width, event.height)

		self.nb_pixels_par_case = nouvelle_taille // self.nb_lignes

		self.delete('case')
		self.dessiner_cases()

		self.delete('piece')
		self.dessiner_piece()

class Frame(tk.Frame):
	pass

class Menu(tk.Menu):
	pass