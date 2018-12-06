from tkinter import Tk
from tkinter import messagebox
# from othello.partie import Partie


class ErreurPositionCoup():

    def __init__(self, interface, partie):

        super().__init__()
        self.interface = interface
        self.message_erreur = ""
        self.partie_othello = partie

    def message_erreur_approprie(self, coup_desire):

        is_message = True
        validation_coup = self.partie_othello.valider_position_coup(coup_desire)

        if not validation_coup[0]:
            self.message_erreur = validation_coup[1]
            messagebox.showerror("Erreur", self.message_erreur, parent=self.interface)
            is_message = False
        return is_message



        

"""section Test

root = Tk()
message_erreur_test = ErreurPositionCoup(root)
message_erreur_test.message_erreur_approprie((3,3))

"""