from othello.planche import Planche
import ast

planche_de_jeu = Planche()
print(planche_de_jeu)

planche_de_jeu.jouer_coup((5,4), "noir")
print(planche_de_jeu)


chaine = planche_de_jeu.convertir_en_chaine()
print(chaine)
chaine_en_liste = chaine.split("\n")[:-1]
print(chaine_en_liste)
print(chaine_en_liste[0][4:])
# compteur_blanc = 0
# compteur_noir = 0
# i = 0
# while i <= len(chaine_en_liste) - 1:
#     if chaine_en_liste[i][4:] == "noir":
#         compteur_noir += 1
#     elif chaine_en_liste[i][4:] == "blanc":
#         compteur_blanc += 1
#     i += 1
# print(compteur_blanc)
# print(compteur_noir)

# x = 3, 5, 5

#
# planche_de_jeu.jouer_coup((5,5), "blanc")
# print(planche_de_jeu)
# planche_de_jeu.charger_dune_chaine(chaine)
#
# print(planche_de_jeu)

'''
get_piece(self, position)
print(planche_de_jeu.get_piece((5,4)))

position_valide(self, position)
print(planche_de_jeu.position_valide((5,4)))

## obtenir_positions_mangees_direction(self, couleur, direblancn, position)
print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [1,1], (5,4)))
print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [1,0], (5,4)))
print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [1,-1], (5,4)))
print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [0,1], (5,4)))
print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [0,-1], (5,4)))
print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [-1,1], (5,4)))
print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [-1,0], (5,4)))
print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [-1,-1], (5,4)))

## coup_est_possible(self, position, couleur)
#print(planche_de_jeu.coup_est_possible((5,4), "noir"))

'''