"""
Module principal du package othello. C'est ce module que nous allons exécuter pour démarrer votre jeu.
"""

from othello.partie import Partie
from interface.interface_othello import Interphace_Othello, Planche_de_jeu

if __name__ == '__main__':
    # Création d'une instance de Partie.
    # partie = Partie()

    # # Si on veut charger une partie à partir d'une partie sauvegardée.
    # partie = Partie("partie_un_tour_a_passer.txt")

    # # Si on veut sauvegarder une partie.
    # partie.sauvegarder("ma_partie.txt")

    # Démarrage de cette partie.
    # partie.jouer()

    app = Interphace_Othello('partie_deux_tours_a_passer.txt')
    app.mainloop()