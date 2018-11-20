# coding=utf-8
from othello.planche import Planche
from othello.joueur import JoueurOrdinateur, JoueurHumain


class Partie:
    def __init__(self, nom_fichier=None):
        """
        Méthode d'initialisation d'une partie. On initialise 4 membres:
        - planche: contient la planche de la partie, celui-ci contenant le dictionnaire de pièces.
        - couleur_joueur_courant: le joueur à qui c'est le tour de jouer.
        - tour_precedent_passe: un booléen représentant si le joueur précédent a passé son tour parce qu'il
           n'avait aucun coup disponible.
        - deux_tours_passes: un booléen représentant si deux tours ont été passés de suite, auquel cas la partie
           devra se terminer.
        - coups_possibles : une liste de tous les coups possibles en fonction de l'état actuel de la planche,
           initialement vide.

        On initialise ensuite les joueurs selon la paramètre nom_fichier. Si l'utilisateur a précisé un nom_fichier,
        on fait appel à la méthode self.charger() pour charger la partie à partir d'un fichier. Sinon, on fait appel
        à self.initialiser_joueurs(), qui va demander à l'utilisateur quels sont les types de joueurs qu'il désire.
        """
        self.planche = Planche()

        self.couleur_joueur_courant = "noir"

        self.tour_precedent_passe = False

        self.deux_tours_passes = False

        self.coups_possibles = []

        if nom_fichier is not None:
            self.charger(nom_fichier)
        else:
            self.initialiser_joueurs()

    def initialiser_joueurs(self):
        """
        On initialise ici trois attributs : joueur_noir, joueur_blanc et joueur_courant (initialisé à joueur_noir).

        Pour créer les objets joueur, faites appel à demander_type_joueur()
        """
        self.joueur_noir = self.demander_type_joueur("noir")
        self.joueur_blanc = self.demander_type_joueur("blanc")
        self.joueur_courant = self.joueur_noir

    def demander_type_joueur(self, couleur):
        """
        Demande à l'usager quel type de joueur ('Humain' ou 'Ordinateur') il désire pour le joueur de la couleur.

        Tant que l'entrée n'est pas valide, on continue de demander à l'utilisateur.

        Faites appel à self.creer_joueur() pour créer le joueur lorsque vous aurez le type.

        Args:
            couleur: La couleur pour laquelle on veut le type de joueur.

        Returns:
            Un objet Joueur, de type JoueurHumain si l'usager a entré 'Humain', JoueurOrdinateur s'il a entré
            'Ordinateur'.
        """
        type_desire = input("""Quel type de joueur désirez vous associé à la couleur ({}) ? Les choix possibles sont: 
        "Humain" ou "Ordinateur" """.format(couleur))

        if type_desire == "Humain" or type_desire == "Ordinateur":
            return self.creer_joueur(type_desire, couleur)

        else:
            self.demander_type_joueur(couleur)


    def creer_joueur(self, type, couleur):
        """
        Crée l'objet Joueur approprié, selon le type passé en paramètre.

        Pour créer les objets, vous n'avez qu'à faire appel à leurs constructeurs, c'est-à-dire à
        JoueurHumain(couleur), par exemple.

        Args:
            type: le type de joueur, "Ordinateur" ou "Humain"
            couleur: la couleur du pion joué par le jouer, "blanc" ou "noir"

        Returns:
            Un objet JoueurHumain si le type est "Humain", JoueurOrdinateur sinon
        """
        if type == "Humain":
            joueur_cree = JoueurHumain(couleur)

        else:
            joueur_cree = JoueurOrdinateur(couleur)

        return joueur_cree

    def valider_position_coup(self, position_coup):
        """
        Vérifie la validité de la position désirée pour le coup. On retourne un message d'erreur approprié pour
        chacune des trois situations suivantes :

        1) Le coup tenté ne représente pas une position valide de la planche de jeu.

        2) Une pièce se trouve déjà à la position souhaitée.

        3) Le coup ne fait pas partie de la liste des coups valides.

        ATTENTION: Utilisez les méthodes et attributs de self.planche ainsi que la liste self.coups_possibles pour
                   connaître les informations nécessaires.
        ATTENTION: Bien que cette méthode valide plusieurs choses, les méthodes programmées dans la planche vous
                   simplifieront la tâche!

        Args:
            position_coup: La position du coup à valider.

        Returns:
            Un couple où le premier élément représente la validité de la position (True ou False), et le
            deuxième élément est un éventuel message d'erreur.
        """

        validite_position = True
        message_erreur = ""

        if not self.planche.position_valide(position_coup):
            validite_position = False
            message_erreur = "Le coup tenté ne représente pas une position valide de la planche de jeu."

        elif position_coup in self.planche.cases:
            validite_position = False
            message_erreur = "Une pièce se trouve déjà à la position souhaitée."

        elif position_coup not in self.coups_possibles:
            validite_position = False
            message_erreur = "Le coup ne fait pas partie de la liste des coups valides"

        return validite_position, message_erreur


    def tour(self):
        """
        Cette méthode simule le tour d'un joueur, et doit effectuer les actions suivantes:
        - Demander la position du coup au joueur courant. Tant que la position n'est pas validée, on continue de
          demander. Si la position est invalide, on affiche le message d'erreur correspondant. Pour demander la
          position, faites appel à la fonction choisir_coup de l'attribut self.joueur_courant, à laquelle vous
          devez passer la liste de coups possibles. Pour valider le coup retourné, pensez à la méthode de validation
          de coup que vous avez déjà à implémenter.
        - Jouer le coup sur la planche de jeu, avec la bonne couleur.
        - Si le résultat du coup est "erreur", afficher un message d'erreur.

        ***Vous disposez d'une méthode pour demander le coup à l'usager dans cette classe et la classe planche
        possède à son tour une méthode pour jouer un coup, utilisez-les !***
        """
        position_demande = self.joueur_courant.choisir_coup(self.coups_possibles)
        if not self.valider_position_coup(position_demande)[0]:
            message_erreur = self.valider_position_coup(position_demande)
            print(message_erreur[1])
            self.tour()

        coup_jouer = self.planche.jouer_coup(position_demande, self.couleur_joueur_courant)

        if coup_jouer == "erreur":
            print("Le déplacement n'a pas été effectuer car il n'est pas valide.")


    def passer_tour(self):
        """
        Affiche un message indiquant que le joueur de la couleur courante ne peut jouer avec l'état actuel de la
        planche et qu'il doit donc passer son tour.
        """
        print("Le joueur de couleur {} n'a aucun coup disponible,"
              " il doit donc passer son tour.".format(self.couleur_joueur_courant))


    def partie_terminee(self):
        """
        Détermine si la partie est terminée, Une partie est terminée si toutes les cases de la planche sont remplies
        ou si deux tours consécutifs ont été passés (pensez à l'attribut self.deux_tours_passes).
        """

        partie_terminee = False

        if len(self.planche.cases) >= 64:
            partie_terminee = True

        if self.deux_tours_passes:
            partie_terminee = True

        return partie_terminee

    def determiner_gagnant(self):
        """
        Détermine le gagnant de la partie. Le gagnant est simplement la couleur pour laquelle il y a le plus de
        pions sur la planche de jeu.

        Affichez un message indiquant la couleur gagnante ainsi que le nombre de pièces de sa couleur ou encore
        un message annonçant un match nul, le cas échéant.
        """
        compteur_blanc = 0
        compteur_noir = 0
        for piece in self.planche.cases.values():
            if piece.est_noir():
                compteur_noir += 1
            elif piece.est_blanc:
                compteur_blanc += 1
        

        if compteur_noir < compteur_blanc :
            message_gagnant = "Le joueur blanc est le gagnant avec {} pièces".format(compteur_blanc)

        elif compteur_blanc < compteur_noir:
            message_gagnant = "Le joueur noir est le gagnant avec {} pièces".format(compteur_noir)

        else:
            message_gagnant = "Aucun gagnant, c'est une match nul"

        print(message_gagnant)

    def jouer(self):
        """
        Démarre une partie. Tant que la partie n'est pas terminée, on fait les choses suivantes :

        1) On affiche la planche de jeu ainsi qu'un message indiquant à quelle couleur c'est le tour de jouer.
           Pour afficher une planche, faites appel à print(self.planche)

        2) On détermine les coups possibles pour le joueur actuel. Pensez à utiliser une fonction que vous avez à
           implémenter pour Planche, et à entreposer les coups possibles dans un attribut approprié de la partie.

        3) Faire appel à tour() ou à passer_tour(), en fonction du nombre de coups disponibles pour le joueur actuel.
           Mettez aussi à jour les attributs self.tour_precedent_passe et self.deux_tours_passes.

        4) Effectuer le changement de joueur. Modifiez à la fois les attributs self.joueur_courant et
           self.couleur_joueur_courant.

        5) Lorsque la partie est terminée, afficher un message mentionnant le résultat de la partie. Vous avez une
           fonction à implémenter que vous pourriez tout simplement appeler.
        """

        while not self.partie_terminee():
            print(self.planche)
            print("Joueur de couleur {}, c'est ton tour à jouer".format(self.couleur_joueur_courant))
            self.coups_possibles = self.planche.lister_coups_possibles_de_couleur(self.couleur_joueur_courant)

            if len(self.coups_possibles) > 0:
                self.tour()
                self.tour_precedent_passe = False

            elif len(self.coups_possibles) == 0:
                self.passer_tour()

                if self.tour_precedent_passe:
                    self.deux_tours_passes = True

                elif not self.tour_precedent_passe:
                    self.tour_precedent_passe = True



            if self.joueur_courant == self.joueur_noir:
                self.joueur_courant = self.joueur_blanc
                self.couleur_joueur_courant = "blanc"

            elif self.joueur_courant == self.joueur_blanc:
                self.joueur_courant = self.joueur_noir
                self.couleur_joueur_courant = "noir"


        # Print la planche final et annonce le gagnant
        print(self.planche)
        self.determiner_gagnant()




    def sauvegarder(self, nom_fichier):
        """
        Sauvegarde une partie dans un fichier. Le fichier condiendra:
        - Une ligne indiquant la couleur du joueur courant.
        - Une ligne contenant True ou False, si le tour précédent a été passé.
        - Une ligne contenant True ou False, si les deux derniers tours ont été passés.
        - Une ligne contenant le type du joueur blanc.
        - Une ligne contenant le type du joueur noir.
        - Le reste des lignes correspondant à la planche. Voir la méthode convertir_en_chaine de la planche
         pour le format.

        ATTENTION : L'ORDRE DES PARAMÈTRES SAUVEGARDÉS EST OBLIGATOIRE À RESPECTER.
                    Des tests automatiques seront roulés lors de la correction et ils prennent pour acquis que le
                    format plus haut est respecté. Vous perdrez des points si vous dérogez du format.

        Args:
            nom_fichier: Le nom du fichier où sauvegarder, un string.
        """
        partie_sauvegarde = open(nom_fichier, 'w')

        partie_sauvegarde.write(self.couleur_joueur_courant)
        partie_sauvegarde.write(str(self.tour_precedent_passe))
        partie_sauvegarde.write(str(self.deux_tours_passes))
        partie_sauvegarde.write(self.joueur_blanc.obtenir_type_joueur())
        partie_sauvegarde.write(self.joueur_noir.obtenir_type_joueur())
        partie_sauvegarde.write(self.planche.convertir_en_chaine())

        partie_sauvegarde.close()


    def charger(self, nom_fichier):
        """
        Charge une partie dans à partir d'un fichier. Le fichier a le même format que la méthode de sauvegarde.

        Args:
            nom_fichier: Le nom du fichier à charger, un string.
        """
        partie_charge = open(nom_fichier, 'r')

        self.couleur_joueur_courant = partie_charge.readline()
        self.tour_precedent_passe = eval(partie_charge.readline())
        self.deux_tours_passes = eval(partie_charge.readline())
        self.joueur_blanc = self.creer_joueur(partie_charge.readline(), "blanc")
        self.joueur_noir = self.creer_joueur(partie_charge.readline(), "noir")

        char_planche = ""
        while partie_charge.readline() != "":
            char_planche = char_planche + partie_charge.readline()

        self.planche = self.planche.charger_dune_chaine(char_planche)
        partie_charge.close()



