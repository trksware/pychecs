# -*- coding: utf-8 -*-

from pychecs2.echecs.piece import Pion, Tour, Fou, Cavalier, Dame, Roi, UTILISER_UNICODE


class PositionSourceInvalide(Exception):
    pass

class DeuxPositionsDeMemeCouleur(Exception):
    pass

class DeplacementNonValide(Exception):
    pass

class Echiquier:
    def __init__(self):
        # Le dictionnaire de pièces, vide au départ, mais ensuite rempli par la méthode initialiser_echiquier_depart().
        self.dictionnaire_pieces = {}
        self.initialiser_echiquier_depart()
        self.chiffres_rangees = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    def chemin_libre_entre_positions(self, position_source, position_cible):

        po_s_l, po_s_c = ord(position_source[0]), ord(position_source[1])
        po_c_l, po_c_c = ord(position_cible[0]), ord(position_cible[1])
        d = po_c_c - po_s_c
        r = True

        if po_s_l == po_c_l:          # dans le cas d'un déplacement horizontale
            if po_s_c > po_c_c:
                po_s_c, po_c_c = ord(position_cible[1]), ord(position_source[1])

            po_s_c += 1
            while po_s_c < po_c_c:
                if chr(po_s_l) + chr(po_s_c) in self.dictionnaire_pieces:
                    return False
                po_s_c += 1

        elif po_s_c == po_c_c:        # dans le cas d'un deplacement verticale
            if po_s_l > po_c_l:
                po_s_l, po_c_l = ord(position_cible[0]), ord(position_source[0])

            po_s_l += 1
            while po_s_l < po_c_l:
                if chr(po_s_l) + chr(po_s_c) in self.dictionnaire_pieces:
                    return False
                po_s_l += 1

        elif abs(d) == abs(po_c_l - po_s_l):              # dans le cas d'un déplacement diagonale
            if (po_s_l < po_c_l and po_s_c < po_c_c) or (po_s_l > po_c_l and po_s_c > po_c_c):
                if po_s_l > po_c_l and po_s_c > po_c_c:
                    po_s_l, po_s_c, po_c_l = ord(position_cible[0]), ord(position_cible[1]), ord(position_source[0])

                po_s_l += 1
                po_s_c += 1
                while po_s_l < po_c_l:
                    if chr(po_s_l) + chr(po_s_c) in self.dictionnaire_pieces:
                        return False
                    po_s_l += 1
                    po_s_c += 1

            elif (po_s_l < po_c_l and po_s_c > po_c_c) or (po_s_l > po_c_l and po_s_c < po_c_c):
                if po_s_l > po_c_l and po_s_c < po_c_c:
                    po_s_l, po_s_c, po_c_l = ord(position_cible[0]), ord(position_cible[1]), ord(position_source[0])

                po_s_l += 1
                po_s_c -= 1
                while po_s_l < po_c_l:
                    if chr(po_s_l) + chr(po_s_c) in self.dictionnaire_pieces:
                        return False
                    po_s_l += 1
                    po_s_c -= 1

        return r

    def deplacer(self, position_source, position_cible):

        self.piece_s_dep = None
        self.piece_cible_mangé = None
        self.poss_annuler = ''
        self.posc_annuler = ''
        if position_source not in self.dictionnaire_pieces:
            raise PositionSourceInvalide("La position source que vous avez choisi est invalide. Veuillez choisir de nouveau")
        piece_source = self.dictionnaire_pieces[position_source]

        if position_cible in self.dictionnaire_pieces:
            piece_cible = self.dictionnaire_pieces[position_cible]
            if isinstance(piece_source, Pion):
                if not piece_source.peut_faire_une_prise_vers(position_source, position_cible):
                    raise DeplacementNonValide("Ce déplacement ne respecte pas les normes du jeu d'échecs")
            elif isinstance(piece_source, Cavalier) and not piece_source.peut_se_deplacer_vers(position_source, position_cible):
                raise DeplacementNonValide("Ce déplacement ne respecte pas les normes du jeu d'échecs")
            elif not piece_source.peut_se_deplacer_vers(position_source, position_cible) or not self.chemin_libre_entre_positions(position_source, position_cible):
                raise DeplacementNonValide("Ce déplacement ne respecte pas les normes du jeu d'échecs")
            if piece_source.couleur == piece_cible.couleur:
                raise DeuxPositionsDeMemeCouleur("Vous ne pouvez pas vous déplacer là, car la position cible contient une de vos pièces")

        else:
            if isinstance(piece_source, Cavalier) and not piece_source.peut_se_deplacer_vers(position_source, position_cible):
                raise DeplacementNonValide("Ce déplacement ne respecte pas les normes du jeu d'échecs")
            elif not piece_source.peut_se_deplacer_vers(position_source, position_cible) or not self.chemin_libre_entre_positions(position_source, position_cible):
                raise DeplacementNonValide("Ce déplacement ne respecte pas les normes du jeu d'échecs")

        if position_cible in self.dictionnaire_pieces:
            self.piece_cible_mangé = piece_cible
        self.poss_annuler = position_source
        self.posc_annuler = position_cible
        self.piece_s_dep = piece_source

        self.dictionnaire_pieces[position_cible] = self.piece_s_dep
        del self.dictionnaire_pieces[position_source]
        return True

    def roi_de_couleur_est_dans_echiquier(self, couleur):
        """Vérifie si un roi de la couleur reçue en argument est présent dans l'échiquier.

        Args:
            couleur (str): La couleur (blanc ou noir) du roi à rechercher.

        Returns:
            bool: True si un roi de cette couleur est dans l'échiquier, et False autrement.

        """
        # en parcourant tout le dictionnaire des pièces on cherche le roi d'une certaine couleur

        r = False
        roi = Roi(couleur)
        for e in list(self.dictionnaire_pieces.values()):            # et on recherche s'il ya un roi.
            if type(e) == Roi and e.couleur == couleur:
                return True
        return r




    def hint(self, position_source):
        r = True
        liste_possible = []
        self.piece_cible_mangé = None
        if position_source not in self.dictionnaire_pieces:
            raise PositionSourceInvalide("La position source que vous avez choisi est invalide. Veuillez choisir de nouveau")
        piece_source = self.dictionnaire_pieces[position_source]

        for i in self.lettres_colonnes:
            for j in self.chiffres_rangees:
                position_cible = i+j
                if position_cible in self.dictionnaire_pieces:
                    piece_cible = self.dictionnaire_pieces[position_cible]
                    if isinstance(piece_source, Pion):
                        if not piece_source.peut_faire_une_prise_vers(position_source, position_cible):
                            continue
                    elif isinstance(piece_source, Cavalier) and not piece_source.peut_se_deplacer_vers(position_source, position_cible):
                        continue
                    elif not piece_source.peut_se_deplacer_vers(position_source, position_cible) or not self.chemin_libre_entre_positions(position_source, position_cible):
                        continue
                    if piece_source.couleur == piece_cible.couleur:
                        continue
                else:
                    if isinstance(piece_source, Cavalier) and not piece_source.peut_se_deplacer_vers(position_source, position_cible):
                        continue
                    elif not piece_source.peut_se_deplacer_vers(position_source, position_cible) or not self.chemin_libre_entre_positions(position_source, position_cible):
                        continue
                liste_possible=liste_possible + [position_cible]

        return liste_possible





    def initialiser_echiquier_depart(self):
        """Initialise l'échiquier à son contenu initial. Pour faire vos tests pendant le développement,
        nous vous suggérons de vous fabriquer un échiquier plus simple, en modifiant l'attribut
        dictionnaire_pieces de votre instance d'Echiquier.

        """
        self.dictionnaire_pieces = {
            'a1': Tour('blanc'),
            'b1': Cavalier('blanc'),
            'c1': Fou('blanc'),
            'd1': Dame('blanc'),
            'e1': Roi('blanc'),
            'f1': Fou('blanc'),
            'g1': Cavalier('blanc'),
            'h1': Tour('blanc'),
            'a2': Pion('blanc'),
            'b2': Pion('blanc'),
            'c2': Pion('blanc'),
            'd2': Pion('blanc'),
            'e2': Pion('blanc'),
            'f2': Pion('blanc'),
            'g2': Pion('blanc'),
            'h2': Pion('blanc'),
            'a7': Pion('noir'),
            'b7': Pion('noir'),
            'c7': Pion('noir'),
            'd7': Pion('noir'),
            'e7': Pion('noir'),
            'f7': Pion('noir'),
            'g7': Pion('noir'),
            'h7': Pion('noir'),
            'a8': Tour('noir'),
            'b8': Cavalier('noir'),
            'c8': Fou('noir'),
            'd8': Dame('noir'),
            'e8': Roi('noir'),
            'f8': Fou('noir'),
            'g8': Cavalier('noir'),
            'h8': Tour('noir'),
        }



if __name__ == '__main__':
    # Exemple de __main__ qui crée un nouvel échiquier, puis l'affiche à l'éran. Vous pouvez ajouter des instructions ici
    # pour tester votre échiquier, mais n'oubliez pas que le programme principal est démarré en exécutant __main__.py.
    echiquier = Echiquier()
    print(echiquier)
