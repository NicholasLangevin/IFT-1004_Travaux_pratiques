"""
Module principal du package othello. C'est ce module que nous allons exécuter pour démarrer votre jeu.
"""

from interface.interface_othello import InterphaceOthello

if __name__ == '__main__':
    
    app = InterphaceOthello()
    app.mainloop()