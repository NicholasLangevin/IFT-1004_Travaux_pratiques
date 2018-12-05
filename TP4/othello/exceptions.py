from tkinter import Tk
from tkinter import messagebox
from othello.partie import Partie


class ErreurPositionCoup(Partie):

    def __init__(self, interface):

        super().__init__()
        self.interface = interface
        self.message_erreur = ""

    def message_erreur_approprie(self, coup_desire):

        self.message_erreur = self.valider_position_coup(coup_desire)[1]
        messagebox.showerror("Erreur", self.message_erreur, parent=self.interface)

"""section Test

root = Tk()
message_erreur_test = ErreurPositionCoup(root)
message_erreur_test.message_erreur_approprie((3,3))

"""