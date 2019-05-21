# -*- coding: utf-8 -*-
"""Ce module contient une classe contenant les informations sur une partie d'échecs,
dont un objet échiquier (une instance de la classe Echiquier).

"""
from pychecs2.echecs.echiquier import Echiquier, PositionSourceInvalide, DeuxPositionsDeMemeCouleur, DeplacementNonValide

class CestPasLeBonJoueur(Exception):
    pass

class EchiquierNonValide(Exception):
    pass

class Partie:
    """La classe Partie contient les informations sur une partie d'échecs, c'est à dire un échiquier, puis
    un joueur actif (blanc ou noir). Des méthodes sont disponibles pour faire avancer la partie et interagir
    avec l'utilisateur.

    Attributes:
        joueur_actif (str): La couleur du joueur actif, 'blanc' ou 'noir'.
        echiquier (Echiquier): L'échiquier sur lequel se déroule la partie.

    """
    def __init__(self, echiquier):
        # Le joueur débutant une partie d'échecs est le joueur blanc.
        self.joueur_actif = 'blanc'

        # Création d'une instance de la classe Echiquier, qui sera manipulée dans les méthodes de la classe.
        self.echiquier = echiquier
        if type(self.echiquier) != Echiquier:
            raise EchiquierNonValide ("Vous n'avez pas rempli tous les champs.")

    def determiner_gagnant(self):
        """Détermine la couleur du joueur gagnant, s'il y en a un. Pour déterminer si un joueur est le gagnant,
        le roi de la couleur adverse doit être absente de l'échiquier.

        Returns:
            str: 'blanc' si le joueur blanc a gagné, 'noir' si c'est plutôt le joueur noir, et 'aucun' si aucun
                joueur n'a encore gagné.

        """
        # si lun des deux roi nest pas dans lechiquier alors lautre joueur est gagnant

        if not self.echiquier.roi_de_couleur_est_dans_echiquier('blanc'):
            return 'noir'

        elif not self.echiquier.roi_de_couleur_est_dans_echiquier('noir'):
            return 'blanc'

        return 'aucun'

    def partie_terminee(self):
        """Vérifie si la partie est terminée. Une partie est terminée si un gagnant peut être déclaré.

        Returns:
            bool: True si la partie est terminée, et False autrement.

        """
        # si lun des deux joueur est gagnany alors la partie est terminee
        if self.echiquier.roi_de_couleur_est_dans_echiquier('blanc') and self.echiquier.roi_de_couleur_est_dans_echiquier('noir'):
            return False
        return True


    def joueur_suivant(self):
        """Change le joueur actif: passe de blanc à noir, ou de noir à blanc, selon la couleur du joueur actif.

        """

        if self.joueur_actif == 'blanc':
            self.joueur_actif = 'noir'

        elif self.joueur_actif == 'noir':
            self.joueur_actif = 'blanc'

    def jouer(self, position_source, positions_cible):
        """Tant que la partie n'est pas terminée, joue la partie. À chaque tour :
            - On affiche l'échiquier.
            - On demande les deux positions.
            - On fait le déplacement sur l'échiquier.
            - On passe au joueur suivant.

        Une fois la partie terminée, on félicite le joueur gagnant!

        """
        if position_source not in self.echiquier.dictionnaire_pieces:
            raise PositionSourceInvalide("La position source que vous avez choisi est invalide. Veuillez choisir de nouveau")
        piece_source = self.echiquier.dictionnaire_pieces[position_source]
        if piece_source.couleur != self.joueur_actif:
            raise CestPasLeBonJoueur("Cest seulement le joueur {} qui peut jouer maintenant". format(self.joueur_actif))

        self.echiquier.deplacer(position_source, positions_cible)
        self.joueur_suivant()