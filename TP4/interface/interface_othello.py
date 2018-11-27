import tkinter as tk  
from ..othello.planche import Planche

class Interphace_Othello(tk.Tk):
	""" Classe de l'interphace graphique du jeu othello """

	def __init__(self):
	
		super().__init__()
		self.title("Jeu de othello")
		self.geometry("800x600")
		self.minsize(800, 600)
		self.resizable(width=False, height=False)
		self.configure(background='green')
		
class Planche_de_jeu(tk.Canvas):
	""" Classe représentant le canvas de la planche de jeu """

	def __init__(self, nb_pixel_par_case):
		super().__init__()
		self.nb_lignes = 8
		self.nb_colonnes = 8
		
		self.chiffre_ligne = [0, 1, 2, 3, 4, 5, 6, 7] 	
		self.chiffre_colonne = [0, 1, 2, 3, 4, 5, 6, 7] 

		self.nb_pixel_par_case = nb_pixel_par_case


if __name__ == __name__:
	app = Interphace_Othello()
	app.mainloop()
