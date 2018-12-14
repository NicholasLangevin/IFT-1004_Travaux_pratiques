from tkinter import Tk, Label, Canvas, messagebox
from othello.partie import Partie
from othello.exceptions import ErreurPositionCoup
import sys


class InterphaceOthello(Tk):
	""" Classe de l'interphace graphique du jeu othello """

	def __init__(self, nom_fichier=None):
	
		super().__init__()
		self.title("Jeu de othello")

		# Initialisation de la partie
		self.partie_othello = Partie(nom_fichier)

		# Création de la planche de jeux
		self.canvas_othello = Planche_de_jeu(self, 100, self.partie_othello.planche)
		self.canvas_othello.grid()

		# Pour le redimentionnement
		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(0, weight=1)

		# Message indiquant en bas du plateau à qui le tour
		self.messages = Label(self)
		self.messages.grid()

		# Lien entre le click et la méthode poser_piece()
		self.canvas_othello.bind('<Button-1>', self.jouer_piece)

		# Vérification d'initiation de partie
		if self.nb_prochain_tour_valide() == 'deux':
			self.Message_fin_de_partie()
		elif self.nb_prochain_tour_valide() in ('noir', 'blanc'):
			messagebox.showinfo("Info","Le joueur {} passe sont tour".format(self.nb_prochain_tour_valide()))
			self.changer_joueur()

		# Affiche le premier joueur à jouer (sera mit à jour plus tard)
		self.messages['text'] = 'C\'est au joueur {} de jouer'.format(self.partie_othello.couleur_joueur_courant)

	# fonction pour savoir la case relié au click
	def get_info_case(self, event):
		
		ligne = event.y // self.canvas_othello.nb_pixels_par_case
		colonne = event.x // self.canvas_othello.nb_pixels_par_case
		return ligne, colonne

	# fonction qui joue la pièce en fonction du click du joueur si aucune erreur est captée
	#  autrement affiche un message d'erreur
	def jouer_piece(self, event):

		pos = self.get_info_case(event)
		self.partie_othello.coups_possibles = self.partie_othello.planche.lister_coups_possibles_de_couleur(self.partie_othello.couleur_joueur_courant)
		try:
			self.partie_othello.valider_position_coup(pos)
			self.canvas_othello.planche.jouer_coup(pos, self.partie_othello.couleur_joueur_courant)
			self.canvas_othello.delete('piece')
			self.canvas_othello.dessiner_piece()

			# Gestion des tours
			if self.nb_prochain_tour_valide() == 'deux':
				self.partie_othello.deux_tours_passes = True
			elif self.nb_prochain_tour_valide() == 'aucun':
				self.changer_joueur()
			elif self.nb_prochain_tour_valide() == self.partie_othello.couleur_joueur_courant:
				messagebox.showinfo("Info","Le joueur {} passe sont tour".format(self.nb_prochain_tour_valide()))
				self.changer_joueur()
			elif self.nb_prochain_tour_valide() != self.partie_othello.couleur_joueur_courant:
					messagebox.showinfo("Info","Le joueur {} passe sont tour".format(self.nb_prochain_tour_valide()))	
			
			if self.partie_othello.partie_terminee():
				self.Message_fin_de_partie()

		except ErreurPositionCoup as message:
			messagebox.showerror("Erreur", message)

		finally:
			self.messages['text'] = 'C\'est au joueur {} de jouer'.format(self.partie_othello.couleur_joueur_courant)

	def nb_prochain_tour_valide(self):
		joueur_skip = "aucun"
		
		# Valide si au moins un des 2 prochains coups est valide
		coup_blanc = self.partie_othello.planche.lister_coups_possibles_de_couleur('blanc')
		coup_noir = self.partie_othello.planche.lister_coups_possibles_de_couleur('noir')
		if len(coup_blanc) == 0 and len(coup_noir) == 0:
			joueur_skip = 'deux'
		elif len(coup_blanc) == 0:
			joueur_skip = 'blanc'
		elif len(coup_noir) == 0:
			joueur_skip = 'noir'

		return joueur_skip

	# fonction qui s'occupe de changer de joueur lorsqu'on y fait appel
	def changer_joueur(self):
		if self.partie_othello.couleur_joueur_courant == "blanc":
				self.partie_othello.joueur_courant = self.partie_othello.joueur_noir
				self.partie_othello.couleur_joueur_courant = "noir"
		else:
			self.partie_othello.joueur_courant = self.partie_othello.joueur_blanc
			self.partie_othello.couleur_joueur_courant = "blanc"
	
	# determine le gagnant et génère le massage qui annonce le résultat final
	# demande à l'utilisateur s'il veut rejouer, si oui appel la fonction pour recommencer, autrement ferme l'interface
	def Message_fin_de_partie(self):

		compteur_blanc, compteur_noir = self.partie_othello.determiner_gagnant()
		if compteur_noir < compteur_blanc:
			message_partie = "Le joueur blanc est le gagnant avec {} pièces".format(compteur_blanc)

		elif compteur_blanc < compteur_noir:
			message_partie = "Le joueur noir est le gagnant avec {} pièces".format(compteur_noir)

		else:
			message_partie = "Aucun gagnant, c'est une match nul"

		messagebox.showinfo('Fin de partie', message_partie)
		nouvelle_partie = messagebox.askyesno("Recommencer", "Désirez-vous faire une autre partie?")
		if nouvelle_partie:
			self.recommencer_nouvelle_partie()
		else:
			sys.exit()

	# reinitialise l'interface et des paramètre pour une nouvelle partie
	def recommencer_nouvelle_partie(self):
		self.partie_othello.planche.initialiser_planche_par_default()
		self.partie_othello.deux_tours_passes = False
		self.canvas_othello.dessiner_cases()
		self.canvas_othello.dessiner_piece()



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

	# gere le redimenssionnement de la planche de jeu
	def redimensionner(self, event):
		nouvelle_taille = min(event.width, event.height)

		self.nb_pixels_par_case = nouvelle_taille // self.nb_lignes

		self.delete('case')
		self.dessiner_cases()

		self.delete('piece')
		self.dessiner_piece()


