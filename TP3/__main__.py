# coding=utf-8
"""
Module principal du package othello. C'est ce module que nous allons exécuter pour démarrer votre jeu.
"""

from othello.partie import Partie

if __name__ == '__main__':
    # Création d'une instance de Partie.
    partie = Partie()

    # # Si on veut charger une partie à partir d'une partie sauvegardée.
<<<<<<< Updated upstream
    #partie = Partie("othello/partie_deux_tours_a_passer.txt")
=======
    partie = Partie("othello/partie_un_tour_a_passer.txt")
>>>>>>> Stashed changes

    # # Si on veut sauvegarder une partie.
    partie.sauvegarder("ma_partie.txt")

    # Démarrage de cette partie.
    partie.jouer()
