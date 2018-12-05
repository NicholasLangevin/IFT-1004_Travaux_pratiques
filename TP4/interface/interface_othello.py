from tkinter import Tk, Label, Canvas, messagebox
from othello.planche import Planche
from othello.piece import Piece
from othello.partie import Partie
from othello.exceptions import ErreurPositionCoup

class Interphace_Othello(Tk):
	""" Classe de l'interphace graphique du jeu othello """

	def __init__(self):
	
		super().__init__()
		self.title("Jeu de othello")

		# Initialisation de la partie
		self.partie_othello = Partie()

		# Création de la planche de jeux
		self.canvas_othello = Planche_de_jeu(self, 100, self.partie_othello.planche)
		self.canvas_othello.grid()

		# Pour le redimentionnement
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)

		self.messages = Label(self)
		self.messages.grid()

		# Lien entre le click et la méthode poser_piece()
		self.canvas_othello.bind('<Button-1>', self.jouer_piece)


		self.erreur_position_coup = ErreurPositionCoup(self, self.partie_othello)

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
		if position in self.canvas_othello.planche.cases:
			couleur = self.canvas_othello.planche.cases[position].couleur
		else:
			couleur = None

		if self.canvas_othello.planche.position_valide(position):
			return position, couleur
		else:
			return None, None # Si la position n'est pas valide, il n'y a pas de couleur.

	def jouer_piece(self, event):


		pos, couleur_case = self.get_info_case(event)

		self.partie_othello.coups_possibles = self.partie_othello.planche.lister_coups_possibles_de_couleur(self.partie_othello.couleur_joueur_courant)


		# if pos != None and couleur_case == None:
		if self.erreur_position_coup.message_erreur_approprie(pos):
			coup_terminer = self.canvas_othello.planche.jouer_coup(pos, self.partie_othello.couleur_joueur_courant)
			
			if coup_terminer == "ok":
				self.canvas_othello.delete('piece')
				self.canvas_othello.dessiner_piece()

			if self.partie_othello.couleur_joueur_courant == "blanc":
				self.partie_othello.joueur_courant = self.partie_othello.joueur_noir
				self.partie_othello.couleur_joueur_courant = "noir"
			else:
				self.partie_othello.joueur_courant = self.partie_othello.joueur_blanc
				self.partie_othello.couleur_joueur_courant = "blanc"

		# else:
		# 	self.erreur_position_coup.message_erreur_approprie(pos)
		self.messages['text'] = self.partie_othello.couleur_joueur_courant

	def verifier_partie(self):
		message_partie = ""
		situation_partie = False
		if self.partie_othello.partie_terminee():
			compteur_blanc = self.partie_othello.determiner_gagnant()[0]
			compteur_noir = self.partie_othello.determiner_gagnant()[1]
			if compteur_noir < compteur_blanc:
				message_partie = "Le joueur blanc est le gagnant avec {} pièces".format(compteur_blanc)
				situation_partie = True

			elif compteur_blanc < compteur_noir:
				message_partie = "Le joueur noir est le gagnant avec {} pièces".format(compteur_noir)
				situation_partie = True

			else:
				message_partie = "Aucun gagnant, c'est une match nul"
				situation_partie = True

		return message_partie, situation_partie

	def passer_tour_message(self):
		message_tour = ""
		if len(self.planche.lister_coups_possibles_de_couleur(self.partie_othello.couleur_joueur_courant)) == 0:
			message_tour = "Aucun coup possible est disponible, vous devez passer votre tour"

			if self.partie_othello.tour_precedent_passe:
				self.partie_othello.deux_tours_passes = True

			else:
				self.partie_othello.tour_precedent_passe = True

		else:
			self.partie_othello.tour_precedent_passe = False

		return message_tour

	def generateur_message_partie(self):

		if self.passer_tour_message() != "":
			messagebox.showinfo("Information pour le joueur courant", self.passer_tour_message())

			if self.verifier_partie()[1]:
				messagebox.showinfo("Partie terminée", self.verifier_partie()[0])
				question_rejouabilite = messagebox.askyesno("Recommencer", "Désirez-vous faire une autre partie?")
				if question_rejouabilite:
					Interphace_Othello()

				elif not question_rejouabilite:
					self.quit()



class Planche_de_jeu(Canvas):
	""" Classe représentant le canvas de la planche de jeu """

	def __init__(self, parent, nb_pixels_par_case, planche):
        # Héritage de Planche(from othello)
		self.planche = planche
		
		self.nb_lignes = self.planche.nb_cases
		self.nb_colonnes = self.planche.nb_cases
		
		self.chiffre_lignes = [0, 1, 2, 3, 4, 5, 6, 7] 	
		self.chiffre_colonnes = [0, 1, 2, 3, 4, 5, 6, 7] 

		self.nb_pixels_par_case = nb_pixels_par_case

		# Héritage de Canvas(from tkinter)
		super().__init__(parent, width=self.nb_lignes * nb_pixels_par_case, height=self.nb_colonnes * nb_pixels_par_case)
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

		for pos in self.planche.cases.keys():

			coord_x = pos[1] * self.nb_pixels_par_case + self.nb_pixels_par_case // 2
			coord_y = pos[0] * self.nb_pixels_par_case + self.nb_pixels_par_case // 2

			couleur_piece = self.planche.cases[pos].couleur

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


