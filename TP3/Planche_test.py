from othello.planche import Planche

planche_de_jeu = Planche()
print(planche_de_jeu)

## get_piece(self, position)
#print(planche_de_jeu.get_piece((5,4)))

## position_valide(self, position)
#print(planche_de_jeu.position_valide((5,4)))

## obtenir_positions_mangees_direction(self, couleur, direblancn, position)
# print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [1,1], (5,4)))
# print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [1,0], (5,4)))
# print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [1,-1], (5,4)))
# print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [0,1], (5,4)))
# print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [0,-1], (5,4)))
# print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [-1,1], (5,4)))
# print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [-1,0], (5,4)))
# print(planche_de_jeu.obtenir_positions_mangees_direction("noir", [-1,-1], (5,4)))

## coup_est_possible(self, position, couleur)
print(planche_de_jeu.coup_est_possible((5,4), "noir"))

