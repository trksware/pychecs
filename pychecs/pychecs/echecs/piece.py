# -*- coding: utf-8 -*-
"""Module contenant la classe de base Piece, ainsi qu'une classe fille pour chacun des types de pièces du jeu d'échecs.

"""
# mettez cette constante (variable globale) à False. Un tutoriel est présent sur le site Web
# du cours pour vous aider à faire fonctionner les caractères Unicoe sous Windows.
UTILISER_UNICODE = True


class Piece:
    """Une classe de base représentant une pièce du jeu d'échecs. C'est cette classe qui est héritée plus bas pour fournir
    une classe par type de pièce (Pion, Tour, etc.).

    Attributes:
        couleur (str): La couleur de la pièce, soit 'blanc' ou 'noir'.
        peut_sauter (bool): Si oui ou non la pièce peut "sauter" par dessus d'autres pièces sur un échiquier.

    Args:
        couleur (str): La couleur avec laquelle créer la pièce.
        peut_sauter (bool): La valeur avec laquelle l'attribut peut_sauter doit être initialisé.

    """
    def __init__(self, couleur, peut_sauter):
        # Validation si la couleur reçue est blanc ou noir.
        assert couleur in ('blanc', 'noir')

        # Création des attributs avec les valeurs reçues.
        self.couleur = couleur
        self.peut_sauter = peut_sauter

    def est_blanc(self):
        """Retourne si oui ou non la pièce est blanche.

        Returns:
            bool: True si la pièce est blanche, et False autrement.

        """
        return self.couleur == 'blanc'

    def est_noir(self):
        """Retourne si oui ou non la pièce est noire.

        Returns:
            bool: True si la pièce est noire, et False autrement.

        """
        return self.couleur == 'noir'

    def peut_se_deplacer_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut se déplacer d'une position à une autre.

        Une position est une chaîne de deux caractères.
            Le premier caractère est une lettre entre a et h, représentant la colonne de l'échiquier.
            Le second caractère est un chiffre entre 1 et 8, représentant la rangée de l'échiquier.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Warning:
            Comme nous sommes dans la classe de base et non dans l'une des classes filles, nous ne savons pas
            (encore) comment cette pièce se déplace. Cette méthode est donc à redéfinir dans chacune des
            classes filles.

        Warning:
            Comme la classe Piece est indépendante de l'échiquier (et donc on ne sait pas si une pièce est "dans le
            chemin"), on doit ignorer le contenu de l'échiquier : on ne se concentre que sur les règles de mouvement
            des pièces.

        Returns:
            bool: True si le déplacement est valide en suivant les règles de la pièce, et False autrement.

        """
        # On lance une exception (on y reviendra) indiquant que ce code n'a pas été implémenté. Ne touchez pas
        # à cette méthode : réimplémentez-la dans les classes filles!
        raise NotImplementedError

    def peut_faire_une_prise_vers(self, position_source, position_cible):
        """Vérifie si, selon les règles du jeu d'échecs, la pièce peut "manger" (faire une prise) une pièce ennemie.
        Pour la plupart des pièces, la règle est la même, on appelle donc la méthode peut_se_deplacer_vers.

        Si ce n'est pas le cas pour une certaine pièce, on peut simplement redéfinir cette méthode pour programmer
        la règle.

        Args:
            position_source (str): La position source, suivant le format ci-haut. Par exemple, 'a8', 'f3', etc.
            position_cible (str): La position cible, suivant le format ci-haut. Par exemple, 'b6', 'h1', etc.

        Returns:
            bool: True si la prise est valide en suivant les règles de la pièce, et False autrement.

        """
        return self.peut_se_deplacer_vers(position_source, position_cible)


class Pion(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def peut_se_deplacer_vers(self, position_source, position_cible):
        # pour chacune des autres classes filles, ci-bas. Nous ne vous demandons pas de documenter ces méthodes,
        # puisque la documentation est déjà ci-haut, dans la classe mère.


        if position_cible[0] != position_source[0]:         # si les deux position ne se trouve pas sur la meme colonne
            return False
        elif super().est_blanc():
            if position_source[1] == "2" and (position_cible[1] != "3" and position_cible[1] != "4"):   # exeption de départ
                return False                                                                            # 1 ou 2 cases
            elif position_source[1] != "2" and position_cible[1] != str(int(position_source[1]) + 1):   # sinon 1 cases
                return False                                                                            # pour le reste de la partie
            else:
                return True
        elif super().est_noir():                                     # les mêmes cas pour les pièces noir, mais dans le sens inverse
            if position_source[1] == "7" and (position_cible[1] != "6" and position_cible[1] != "5"):
                return False
            elif position_source[1] != "7" and position_cible[1] != str(int(position_source[1]) - 1):
                return False
            else:
                return True

    def peut_faire_une_prise_vers(self, position_source, position_cible):
        r = True
        if super().est_blanc() and position_cible[1] != str(int(position_source[1]) + 1): # la prise tout comme le
            return  False                                                                 # déplacement se fait en avant
        elif super().est_noir() and position_cible[1] != str(int(position_source[1]) - 1):
            return False

        if position_source[0] == 'a' and position_cible[0] != 'b':                      # le cas des bords colonne a et h
            r = False
        elif position_source[0] == 'h' and position_cible[0] != 'g':
            r = False
        elif position_source[0] in 'bcdefg':                                                # le reste des colonnes de l'échiquier
            if position_cible[0] != chr(ord(position_source[0]) + 1) and position_cible[0] != chr(ord(position_source[0]) - 1):
                r = False
            else:
                r = True
        return r


    def __repr__(self):
        """Redéfinit comment on affiche un pion à l'écran. Nous utilisons la constante UTILISER_UNICODE
        pour déterminer comment afficher le pion.

        Returns:
            str: La chaîne de caractères représentant le pion.

        """
        if self.est_blanc():
            if UTILISER_UNICODE:
                return '\u2659'
            else:
                return 'PB'
        else:
            if UTILISER_UNICODE:
                return '\u265f'
            else:
                return 'PN'


class Tour(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def __repr__(self):
        if self.est_blanc():
            if UTILISER_UNICODE:
                return '\u2656'
            else:
                return 'TB'
        else:
            if UTILISER_UNICODE:
                return '\u265c'
            else:
                return 'TN'
    def peut_se_deplacer_vers(self, position_source, position_cible):
        po_s_l, po_s_c = ord(position_source[0]), ord(position_source[1])             # on stocke les codes ascii correspondant des composantes des positions
        po_c_l, po_c_c = ord(position_cible[0]), ord(position_cible[1])

        if po_c_l == po_s_l and po_c_c != po_s_c:       # faut s'assurer que la position source et cible ne sont pas égales
            return True
        elif po_c_l != po_s_l and po_c_c == po_s_c:
            return True
        else:
            return False


class Cavalier(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, True)

    def __repr__(self):
        if self.est_blanc():
            if UTILISER_UNICODE:
                return '\u2658'
            else:
                return 'CB'
        else:
            if UTILISER_UNICODE:
                return '\u265e'
            else:
                return 'CN'

    def peut_se_deplacer_vers(self, position_source, position_cible):
        po_s_l, po_s_c = ord(position_source[0]), ord(position_source[1])         # on stocke les codes ascii correspondant des composantes des positions
        po_c_l, po_c_c = ord(position_cible[0]), ord(position_cible[1])

        if po_s_c == po_c_c + 1 or po_s_c == po_c_c -1:     # on assume que la position est valide, valide les entrées
            if po_s_l == po_c_l + 2 or po_s_l == po_c_l -2: # on évalue toutes les possibilités
                return True
            else:
                return False
        elif po_s_c == po_c_c + 2 or po_s_c == po_c_c -2:
            if po_s_l == po_c_l + 1 or po_s_l == po_c_l -1:
                return True
            else:
                return False

class Fou(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def __repr__(self):
        if self.est_blanc():
            if UTILISER_UNICODE:
                return '\u2657'
            else:
                return 'FB'
        else:
            if UTILISER_UNICODE:
                return '\u265d'
            else:
                return 'FN'
    def peut_se_deplacer_vers(self, position_source, position_cible):
        po_s_l, po_s_c = ord(position_source[0]), ord(position_source[1])
        po_c_l, po_c_c = ord(position_cible[0]), ord(position_cible[1])

        d = po_c_c - po_s_c
        if abs(d) != abs(po_c_l - po_s_l) or abs(d) == 0 == abs(po_c_l - po_s_l): # si les deux positions sont les mêmes
            return False
        elif abs(d) == abs(po_c_l - po_s_l):  # si le deplacement est diagonale c'est à dire que la distance parcourue
            return True                     # par rapport à l'axe, des chiffres et celui des lettres est égale
        else:
            return False


class Roi(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def __repr__(self):
        if self.est_blanc():
            if UTILISER_UNICODE:
                return '\u2654'
            else:
                return 'RB'
        else:
            if UTILISER_UNICODE:
                return '\u265a'
            else:
                return 'RN'
    def peut_se_deplacer_vers(self, position_source, position_cible):
        po_s_l, po_s_c = ord(position_source[0]), ord(position_source[1])
        po_c_l, po_c_c = ord(position_cible[0]), ord(position_cible[1])

        # cette pièce fonctionne comme la pièce pion

        if (po_c_c == po_s_c + 1 or po_c_c == po_s_c - 1) and (po_c_l == po_s_l + 1 or po_c_l == po_s_l - 1):
            return True
        elif po_c_c == po_s_c and (po_c_l == po_s_l + 1 or po_c_l == po_s_l - 1):
            return True
        elif po_c_l == po_s_l and (po_c_c == po_s_c + 1 or po_c_c == po_s_c - 1):
            return True
        else:
            return False


class Dame(Piece):
    def __init__(self, couleur):
        super().__init__(couleur, False)

    def __repr__(self):
        if self.est_blanc():
            if UTILISER_UNICODE:
                return '\u2655'
            else:
                return 'DB'
        else:
            if UTILISER_UNICODE:
                return '\u265b'
            else:
                return 'DN'
    def peut_se_deplacer_vers(self, position_source, position_cible):
        po_s_l, po_s_c = ord(position_source[0]), ord(position_source[1])
        po_c_l, po_c_c = ord(position_cible[0]), ord(position_cible[1])

        d = po_c_c - po_s_c               # le même fonctionnement que pour la tour et le fou
        if po_c_l == po_s_l and po_c_c == po_s_c:
            return False
        elif po_c_l == po_s_l and po_c_c != po_s_c:
            return True
        elif po_c_l != po_s_l and po_c_c == po_s_c:
            return True
        elif abs(d) == abs(po_c_l - po_s_l):
            return True
        else:
            return False