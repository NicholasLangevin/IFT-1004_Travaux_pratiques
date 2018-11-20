from othello.partie import Partie
from othello.joueur import JoueurHumain

joueur = JoueurHumain("noir")


print(joueur.choisir_coup([(3,3), (2,2)]))