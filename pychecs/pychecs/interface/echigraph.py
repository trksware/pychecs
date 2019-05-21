"""Solution du laboratoire, permettant de bien comprendre comment hériter d'un widget de tkinter, de dessiner
un échiquier dans un Canvas, puis de déterminer quelle case a été sélectionnée.

Auteur: Jean-Francis Roy

"""
from tkinter import Tk, Canvas, Frame, Label, NSEW, Button, messagebox, LabelFrame, Label, Button, RIDGE, N, S, W, E,\
    filedialog, Toplevel, Entry, filedialog, Radiobutton, Checkbutton, IntVar, BooleanVar, Toplevel, Toplevel, RIGHT,\
    Scrollbar, Y
from pychecs2.echecs.echiquier import Echiquier, PositionSourceInvalide, DeuxPositionsDeMemeCouleur, DeplacementNonValide
from pychecs2.echecs.piece import Pion, Tour, Fou, Cavalier, Dame, Roi, UTILISER_UNICODE
from pychecs2.echecs.partie import Partie, CestPasLeBonJoueur
import random

# Exemple d'importation de la classe Partie.
from pychecs2.echecs.partie import Partie
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class ChoisirDaborsPositionSource(Exception):
    pass
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class CanvasEchiquier(Canvas):
    """Classe héritant d'un Canvas, et affichant un échiquier qui se redimensionne automatique lorsque
    la fenêtre est étirée.

    """
    def __init__(self, parent, n_pixels_par_case):
        # Nombre de lignes et de colonnes.
        self.n_lignes = 8
        self.n_colonnes = 8

        # Noms des lignes et des colonnes.
        self.chiffres_rangees = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.lettres_colonnes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        # Nombre de pixels par case, variable.
        self.n_pixels_par_case = n_pixels_par_case

        # Appel du constructeur de la classe de base (Canvas).
        # La largeur et la hauteur sont déterminées en fonction du nombre de cases.
        super().__init__(parent, width=self.n_lignes * n_pixels_par_case,
                         height=self.n_colonnes * self.n_pixels_par_case)

        # On fait en sorte que le redimensionnement du canvas redimensionne son contenu. Cet événement étant également
        # généré lors de la création de la fenêtre, nous n'avons pas à dessiner les cases et les pièces dans le
        # constructeur.
        self.echiquier = Echiquier()
        self.echiquier.initialiser_echiquier_depart()
        self.bind('<Configure>', self.redimensionner)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def dessiner_cases(self):
        """Méthode qui dessine les cases de l'échiquier.

        """
        for i in range(self.n_lignes):
            for j in range(self.n_colonnes):
                debut_ligne = i * self.n_pixels_par_case
                fin_ligne = debut_ligne + self.n_pixels_par_case
                debut_colonne = j * self.n_pixels_par_case
                fin_colonne = debut_colonne + self.n_pixels_par_case

                # On détermine la couleur.
                if (i + j) % 2 == 0:
                    couleur = 'white'
                else:
                    couleur = 'gray'

                # On dessine le rectangle. On utilise l'attribut "tags" pour être en mesure de récupérer les éléments
                # par la suite.
                self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill=couleur, tags='case')
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def dessiner_pieces(self):
        # Caractères unicode représentant les pièces. Vous avez besoin de la police d'écriture DejaVu.
        self.caracteres_pieces = {Pion('blanc'): '\u2659',
                             Pion('noir'): '\u265f',
                             Tour('blanc'): '\u2656',
                             Tour('noir'): '\u265c',
                             Cavalier('blanc'): '\u2658',
                             Cavalier('noir'): '\u265e',
                             Fou('blanc'): '\u2657',
                             Fou('noir'): '\u265d',
                             Roi('blanc'): '\u2654',
                             Roi('noir'): '\u265a',
                             Dame('blanc'): '\u2655',
                             Dame('noir'): '\u265b'
                             }

        # Pour tout paire position, pièce:
        for position in self.echiquier.dictionnaire_pieces:
            # On dessine la pièce dans le canvas, au centre de la case. On utilise l'attribut "tags" pour être en
            # mesure de récupérer les éléments dans le canvas.
            coordonnee_y = (self.n_lignes - self.chiffres_rangees.index(position[1]) - 1) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            coordonnee_x = self.lettres_colonnes.index(position[0]) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            piece = self.echiquier.dictionnaire_pieces[position]
            uni = ""
            for e in list(self.caracteres_pieces.keys()):
                if type(e) == type (piece) and e.couleur == piece.couleur:
                    uni = self.caracteres_pieces[e]
                    break
            self.create_text(coordonnee_x, coordonnee_y, text= uni, font=('Deja Vu', self.n_pixels_par_case//2), tags='piece')
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def redimensionner(self, event):
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.
        nouvelle_taille = min(event.width, event.height)

        # Calcul de la nouvelle dimension des cases.
        self.n_pixels_par_case = nouvelle_taille // self.n_lignes

        # On supprime les anciennes cases et on ajoute les nouvelles.
        self.delete('case')
        self.dessiner_cases()

        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.delete('piece')
        self.dessiner_pieces()

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

class Fenetre(Tk):
    def __init__(self):
        super().__init__()

        # Nom de la fenêtre.
        self.title("Chess")


        # quelques attributs à utiliser plustard
        self.position_source = None
        self.option_indice = 0
        self.protocol('WM_DELETE_WINDOW', self.demander)    # cette instruction fait appel a une fonction si le joueur
                                                            # click sur le bouton fermé de la fenetre tk

        # Création du canvas échiquier.
        self.canvas_echiquier = CanvasEchiquier(self, 50)
        self.canvas_echiquier.grid(padx=0, pady=0, sticky=NSEW, row=0, column=0, rowspan=2)

        # Redimensionnement automatique du canvas.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Label pour les infos sur la partie, voir les paramètres 'text=...' pour avoir plus de détails sur chaque sous-fram
        self.frame_infos = LabelFrame(self, borderwidth=3, relief=RIDGE, text="Information sur la partie")
        self.frame_infos.grid(row=0, column=1, sticky=N)

        self.mon_label_info = Label(self.frame_infos, font=("DejaVu Sans", 16),text="C'est au tour du joueur blanc")
        self.mon_label_info.grid(columnspan=4)

        self.prises_blanc = Label(self.frame_infos, borderwidth=2, relief=RIDGE, font=("DejaVu Sans", 8), text="Prises du\njoueur blanc")
        self.prises_blanc.grid(row=1, column=0,sticky=N+W)

        self.prises_noir = Label(self.frame_infos, borderwidth=2, relief=RIDGE, font=("DejaVu Sans", 8), text="Prises du\njoueur noir")
        self.prises_noir.grid(row=1, column=1,sticky=N+E)

        self.depla_blanc = Label(self.frame_infos, borderwidth=2, relief=RIDGE, font=("DejaVu Sans", 8), text="Liste des déplacements\njoueur blanc")
        self.depla_blanc.grid(row=1, column=2,sticky=N+W)

        self.depla_noir = Label(self.frame_infos, borderwidth=2, relief=RIDGE, font=("DejaVu Sans", 8), text="Liste des déplacements\njoueur noir")
        self.depla_noir.grid(row=1, column=3,sticky=N+E)

        # Label pour le menu (contenant des bouton) de la partie, voir les paramètres 'text=...' pour avoir plus de
        # détails sur cache bouton: chaque bouton envoi vers une fonction voir les paramètres 'command=...'
        self.frame_menu = LabelFrame(self, borderwidth=3, relief=RIDGE, text="Menu de la partie")
        self.frame_menu.grid(row=1, column=1, sticky=NSEW, padx=10, pady=0)

        self.nouvelle = Button(self.frame_menu, text="Nouvelle partie", command=self.nouvelle_partie)
        self.nouvelle.grid(sticky=NSEW, row=0, column=0)

        self.sauv = Button(self.frame_menu, text="Sauvegarder la partie", command=self.save)
        self.sauv.grid(sticky=NSEW, row=1, column=0)

        self.load = Button(self.frame_menu, text="Charger une partie", command=self.load)
        self.load.grid(sticky=NSEW, row=2, column=0)

        self.infos = Button(self.frame_menu, text="Informations sur le jeu", command=self.infos_et_règles)
        self.infos.grid(sticky=NSEW, row=3, column=0)

        self.annul = Button(self.frame_menu, text="Annuler le dernier déplacement", command=self.annuler)
        self.annul.grid(sticky=NSEW, row=4, column=0)

        self.o = Button(self.frame_menu, text="Passez la main à l'ordi", command =self.ordi)
        self.o.grid(sticky=N+E+W, row=0, column=1)

        self.o_h_a = Checkbutton(self.frame_menu, text="Activer cette case puis faites un\nclick droit sur la piece "
                                                       "voulu\npour voir les possibilitées\nqui s'offrent à "
                                                       "vous", command =self.activer_indice)
        self.o_h_a.grid(sticky=NSEW, row=1, column=1, rowspan=3)

        self.partie = Partie(self.canvas_echiquier.echiquier)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self, font=("DejaVu Sans", 16))
        self.messages.grid(row=2, columnspan=2)

        # On lie un clic sur le CanvasEchiquier à une méthode.
        self.canvas_echiquier.bind('<Button-3>', self.option_hint)
        self.canvas_echiquier.bind('<Button-1>', self.selectionner_source)
        self.canvas_echiquier.bind('<ButtonRelease-1>', self.selectionner_cible)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# fonctions liées
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def selectionner_source(self, event):
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.canvas_echiquier.n_pixels_par_case

        # On récupère l'information sur la pièce à l'endroit choisi, lors le de la pression du bouton gauche
        try:
            position = "{}{}".format(self.canvas_echiquier.lettres_colonnes[colonne], int(self.canvas_echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]))

            # on essaie de récupérer la piece et on la place dans un attribut
            self.position_source = position
            self.piece_source = self.canvas_echiquier.echiquier.dictionnaire_pieces[self.position_source]

            self.messages['foreground'] = 'black'
            self.messages['text'] = 'Pièce sélectionnée : {} à la position {}.'.format(self.piece_source, self.position_source)

        except KeyError:        # sauf si la positions est vide
            self.messages['foreground'] = 'red'
            self.messages['text'] = "La position source que vous avez choisi est invalide veuillez choisir de nouveau"
        except IndexError:
            self.messages['foreground'] = 'red'
            self.messages['text'] = ""
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    def selectionner_cible(self, event):
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_echiquier.n_pixels_par_case
        colonne = event.x // self.canvas_echiquier.n_pixels_par_case

        # On récupère l'information sur la pièce à l'endroit choisi lors du relachement du bouton gauche
        try:
            position = "{}{}".format(self.canvas_echiquier.lettres_colonnes[colonne], int(self.canvas_echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]))
            self.position_cible = position
            self.partie.jouer(self.position_source, self.position_cible)   # on envoie à la fonction qui fait le déplacement dans le dict de l'échiquier
            self.affichage_info()
            if self.partie.partie_terminee():       # on fait un envois à la fonction qui verifie si la partie est terminé
                self.partie.joueur_suivant()        # on retourne vers le joueur gagnant et on affiche une messagebox
                reponse=messagebox.askquestion('La partie_terminée', 'La partie est terminée, félicitation au joueur {}.\nVoulez-vous '
                                                                     'jouer une nouvelle partie ou quitter?\nCliquez sur "Oui" pour '
                                                                     'rejouer ou sur non pour quitter.'.format(self.partie.joueur_actif))
                if reponse == "yes":                # le message box nous demande si on veut vraiment quitter ou
                    self.nouvelle_partie()          # jouer une nouvelle partie
                else:
                    self.destroy()
        except ChoisirDaborsPositionSource as e:    # il ya 5 cas ou le deplacement ne peut pas étre effectué
            self.messages['foreground'] = 'red'     # ces exceptions se situent dans d'autre modules
            self.messages['text'] = e               # le nom des class des exceptions est assez expressif...
        except PositionSourceInvalide as e:
            self.messages['foreground'] = 'red'
            self.messages['text'] = e
        except DeuxPositionsDeMemeCouleur as e:
            self.messages['foreground'] = 'red'
            self.messages['text'] = e
        except DeplacementNonValide as e:
            self.messages['foreground'] = 'red'
            self.messages['text'] = e
        except CestPasLeBonJoueur as e:
            self.messages['foreground'] = 'red'
            self.messages['text'] = e
        except IndexError:
            self.messages['foreground'] = 'red'
            self.messages['text'] = ""
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    # si le joueur click sur le bouton nouvelle partie
    def nouvelle_partie(self):
        reponse=messagebox.askquestion("C'est une bonne partie...courage", "Si vous quittez, vous risquez de perdre la "
                                                                           "partie courante?\nCliquez sur 'Oui' pour sau"
                                                                           "vegarder la partie ou sur 'Non' pour "
                                                                           "quitter.".format(self.partie.joueur_actif))
        if reponse == "yes":            # on affiche une messagebox qui pose une question au joueur
            self.save()                 # s'il reponds qu'il veut sauver la partie on fait un appel de fonction (voir en bas)
        else:                           # sinon on réinitialise l'echiquier, réaffiche le canvas
            self.canvas_echiquier.echiquier.initialiser_echiquier_depart()
            self.canvas_echiquier.delete('piece')
            self.canvas_echiquier.dessiner_pieces()
            self.partie.joueur_actif = 'blanc'
            self.messages['foreground'] = 'black'
            self.messages['text'] = "c'est parti"
            self.mon_label_info['text'] = "C'est au tour du joueur blanc"
            self.prises_blanc['text'] = "Prises du\njoueur blanc"
            self.prises_noir['text'] = "Prises du\njoueur noir"
            self.depla_blanc['text'] = "Liste des déplacements\njoueur blanc"
            self.depla_noir['text'] = "Liste des déplacements\njoueur noir"
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # si le joueur click sur le bouton sauvegarder
    def save(self):     # on ouvre une fenetre de dialogue pour le (path) de sauvegarde, (seulement .txt et prédefini),
                        # et aussi un demande un nom de fichier
        destination = filedialog.asksaveasfilename(title='Choisissez un répertoire où sauvegarder votre '
                                                         'partie', defaultextension='.txt', filetypes=[('text seulement', '.txt')])
        if destination:
            sauvegarde = open(destination, "w")
            for e in self.canvas_echiquier.echiquier.dictionnaire_pieces:
                sauvegarde.write(e)                                             # on y écrit chaque position pleine.
                piece = self.canvas_echiquier.echiquier.dictionnaire_pieces[e]
                caracteres_pieces_w = {Pion('blanc'): 'PB', Pion('noir'): 'PN',
                                 Tour('blanc'): 'TB', Tour('noir'): 'TN',
                                 Cavalier('blanc'): 'CB', Cavalier('noir'): 'CN',
                                 Fou('blanc'): 'FB', Fou('noir'): 'FN',
                                 Roi('blanc'): 'RB', Roi('noir'): 'RN',
                                 Dame('blanc'): 'DB', Dame('noir'): 'DN'}
                for p in caracteres_pieces_w:                                   # pour chque position on compare le type
                    if type(p) == type(piece) and p.couleur == piece.couleur:   # de piece qu'elle contient avec le dict
                        sauvegarde.write(caracteres_pieces_w[p])                # defini au dessus puis on ecrit le caract
                sauvegarde.write('\n')                                          # correspondant, puis on saute la ligne
            sauvegarde.write(self.partie.joueur_actif)                          # apres avoir parcouru toutes les piece
            sauvegarde.close()                                                  # on ecrit le nom du joueur actif
            self.messages['foreground'] = 'black'
            self.messages['text'] = 'La partie à été enregistré avec success'   # enfin on affiche un message que tout c'est bien passé

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # si le joueur click sur le bouton charger une nouvelle partie
    def load(self):
        reponse=messagebox.askquestion("C'est une bonne partie...courage", "Si vous chargez une nouvelle partie, vous "
                                                                           "risquez de perdre la partie courante?\nCliquez sur "
                                                                           "'Oui' pour sauvegarder la partie courante ou sur 'Non' pour "
                                                                           "continuer.".format(self.partie.joueur_actif))
        if reponse == "yes":            # on affiche une fenetre pour demander si vraiment on veut quitter la partie en cours
            self.save()
        fichier_source = filedialog.askopenfilename(title='Choisissez le fichier où est sauvegardé vôtre '
                                                          'partie', defaultextension='.txt', filetypes=[('text seulement', '.txt')])
        if fichier_source:
            load = open(fichier_source, 'r')                # le même fonctionnement que pour sel.save()
            dicos_chaine = load.readlines()
            caracteres_pieces_r = {'PB' : Pion('blanc'), 'PN':Pion('noir'),
                                 'TB' : Tour('blanc'), 'TN' : Tour('noir'),
                                 'CB' : Cavalier('blanc'),'CN' : Cavalier('noir'),
                                 'FB' : Fou('blanc'), 'FN' : Fou('noir'),
                                 'RB' : Roi('blanc'), 'RN' : Roi('noir'),
                                 'DB' : Dame('blanc'), 'DN' : Dame('noir')}
            pos = ''
            piece = None
            piece_class = ''
            self.canvas_echiquier.echiquier.dictionnaire_pieces = {}
            for l in range(len(dicos_chaine) - 1):
                pos = dicos_chaine[l][0:2]
                piece = dicos_chaine[l][2:4]
                for p in caracteres_pieces_r:
                    if piece == p:
                        piece_class = caracteres_pieces_r[p]
                self.canvas_echiquier.echiquier.dictionnaire_pieces[pos] = piece_class
            self.partie.joueur_actif = dicos_chaine[-1]
            load.close()
            self.canvas_echiquier.delete('piece')
            self.canvas_echiquier.dessiner_pieces()
            self.messages['foreground'] = 'black'
            self.messages['text'] = 'La partie à été chargé avec succès'
            self.messages['text'] = "c'est parti"
            self.mon_label_info['text'] = "C'est au tour du joueur {}".format(self.partie.joueur_actif)
            self.mon_label_info['text'] = "C'est au tour du joueur blanc"
            self.prises_blanc['text'] = "Prises du\njoueur blanc"
            self.prises_noir['text'] = "Prises du\njoueur noir"
            self.depla_blanc['text'] = "Liste des déplacements\njoueur blanc"
            self.depla_noir['text'] = "Liste des déplacements\njoueur noir"
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # annuler le dernier déplacement et seulement le dérnier
    def annuler(self):
        # ce premier bloque s'assure qu'il n'y a pas eu d'appel de cette fonction juste avant, on ne peut annuler qu'un seul déplaclement à la fois
        # et ceci en regardant si la derniere position source est bien vide.
        if self.canvas_echiquier.echiquier.poss_annuler not in self.canvas_echiquier.echiquier.dictionnaire_pieces:
            self.canvas_echiquier.echiquier.dictionnaire_pieces[self.canvas_echiquier.echiquier.poss_annuler] = self.canvas_echiquier.echiquier.piece_s_dep
            # après cela nous avons deux cas soit on recupère la dernier pièce mangée (si c'est le cas) que nous avons
            # stocké dans un attribut de echiquier.py
            if self.canvas_echiquier.echiquier.piece_cible_mangé:
                self.canvas_echiquier.echiquier.dictionnaire_pieces[self.canvas_echiquier.echiquier.posc_annuler] = self.canvas_echiquier.echiquier.piece_cible_mangé
            else:       # sinon on remet la piece à sa place
                del self.canvas_echiquier.echiquier.dictionnaire_pieces[self.canvas_echiquier.echiquier.posc_annuler]
        else:
            self.messages['text'] = 'Plus aucun déplacement à annuler'
        # puis on réaffiche le tout avec un message que tout s'est bien passé
        self.partie.joueur_actif = self.canvas_echiquier.echiquier.piece_s_dep.couleur
        self.canvas_echiquier.delete('piece')
        self.canvas_echiquier.dessiner_pieces()
        self.messages['foreground'] = 'black'
        self.messages['text'] = 'Le dernier déplacement a été annulé avec succès'
        if self.partie.joueur_actif == 'blanc':                 # on affiche le déplacement dans la liste des infos
            self.depla_blanc['text'] = self.depla_blanc['text'] + '(annulé)'
        else:
            self.depla_noir['text'] = self.depla_noir['text'] + '(annulé)'

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # si le joueur active la case pour les indices l'attribut self.option_indice se change en true.
    # et puis s'il clique sur la piece de son choix avec le bouton droit il fait un appel vers cette fonction
    def option_hint(self, event):
        try:
            if self.option_indice == True:
                self.canvas_echiquier.delete('piece')       # ce bloque sert lors du changement de piece sélectionné
                self.canvas_echiquier.dessiner_pieces()     # comme ça les indices de l'ancienne pièce sont effacé
                self.canvas_echiquier.dessiner_cases()
                l = ''
                ligne = event.y // self.canvas_echiquier.n_pixels_par_case  # on recupère la position de l'évènement
                colonne = event.x // self.canvas_echiquier.n_pixels_par_case
                position = "{}{}".format(self.canvas_echiquier.lettres_colonnes[colonne], int(self.canvas_echiquier.chiffres_rangees[self.canvas_echiquier.n_lignes - ligne - 1]))
                liste = self.canvas_echiquier.echiquier.hint(position)  # on recupère la liste des positions possible depuis une fonction dans un autre module
                if self.canvas_echiquier.echiquier.dictionnaire_pieces[position].couleur == self.partie.joueur_actif:
                    for e in range(len(liste)):
                        lettr = ord(liste[e][0]) - 97           # on recupère les positions équivalentes dans l'echiquier
                        chiff = abs(int(liste[e][1]) - 1 - 7)   # pour chaque position de la liste precedente.
                        debut_ligne = chiff * self.canvas_echiquier.n_pixels_par_case
                        fin_ligne = debut_ligne + self.canvas_echiquier.n_pixels_par_case
                        debut_colonne = lettr * self.canvas_echiquier.n_pixels_par_case
                        fin_colonne = debut_colonne + self.canvas_echiquier.n_pixels_par_case
                        couleur = 'yellow'          # puis seulement pour chaque position de la liste on réaffiche la case
                        self.canvas_echiquier.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill=couleur, tags='case')


        except PositionSourceInvalide as e:     # exception le joueur choisi une position invalide
            self.messages['foreground'] = 'red'
            self.messages['text'] = e
        except IndexError:
            self.messages['foreground'] = 'red'
            self.messages['text'] = ""
        finally:
            self.canvas_echiquier.delete('piece')       #puis on raffiche les pieces sur le nouvelle echiquier
            self.canvas_echiquier.dessiner_pieces()
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # comme expliqué plus haut lorsque le joueur active la case pour les indices l'attribut self.option_indice se change
    # en true.
    def activer_indice(self):
        if self.option_indice == 0:
            self.option_indice = 1
        else:
            self.option_indice = 0
            self.canvas_echiquier.dessiner_cases()
            self.canvas_echiquier.delete('piece')
            self.canvas_echiquier.dessiner_pieces()
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # lorsque le joueur blanc clique sur le bouton 'passer la main à l'ordi' ce code est appeller pour faire jouer une
    # pièce par l'ordi (l'odri joue les pièces noirs)
    def ordi(self):
        try:

            if self.partie.joueur_actif == 'blanc':
                raise CestPasLeBonJoueur("C'est à vous de jouer maintenant")
            list_possit_noir = []
            for pos_piece_noir in self.canvas_echiquier.echiquier.dictionnaire_pieces:
                if self.canvas_echiquier.echiquier.dictionnaire_pieces[pos_piece_noir].couleur == 'noir':
                    list_possit_noir.append(pos_piece_noir) # on récupère les positions de toutes les pièces noirs
            self.position_source= ''
            self.position_cible = ''
            list_pos_s_posib = []
            list_indice = []
            for i in list_possit_noir:  # pour chaque pièces
                list_indice = self.canvas_echiquier.echiquier.hint(i)   # donne moi la liste des possibilités de déplacement
                if list_indice:                 # si cette pièce peut se déplacer
                    list_pos_s_posib.append(i)  # crée une liste des pièce noires qui peuvent se déplacer
            for j in list_pos_s_posib:          # maintenant pour chaque pièce noir qui peut se déplacer
                list_indice = []
                list_indice = self.canvas_echiquier.echiquier.hint(j)   # récupère la liste des possibilités de déplacemen
                for k in list_indice:                   # si dans la liste des possibilités de déplacemen
                    if k in self.canvas_echiquier.echiquier.dictionnaire_pieces and self.canvas_echiquier.echiquier.dictionnaire_pieces[k].couleur != 'noir':
                        self.position_cible = k                  # tu trouve une piece dans l'échiquier et qui est blanche
                        self.position_source = j                 # réfléchi pas! mange la!
                        self.piece_source = self.canvas_echiquier.echiquier.dictionnaire_pieces[self.position_source]
                        break


            if not self.position_source and not self.position_cible:  # si après tout ça tu trouves rien
                self.position_source = random.choice(list_pos_s_posib)   # pioche une position de pièce noir
                self.piece_source = self.canvas_echiquier.echiquier.dictionnaire_pieces[self.position_source]
                list_indice = []
                list_indice = self.canvas_echiquier.echiquier.hint(self.position_source) # récupère la liste des possibilités de déplacemen
                self.position_cible = random.choice(list_indice)         # et pioche une position cible
            self.partie.jouer(self.position_source, self.position_cible)      # enfin le déplacement
            self.affichage_info()


            if self.partie.partie_terminee():       # on fait un envois à la fonction qui verifie si la partie est terminé
                self.partie.joueur_suivant()        # on retourne vers le joueur gagnant et on affiche une messagebox
                reponse=messagebox.askquestion('La partie_terminée', 'La partie est terminée, félicitation au joueur {}.\nVoulez-vous '
                                                                     'jouer une nouvelle partie ou quitter?\nCliquez sur "Oui" pour '
                                                                     'rejouer ou sur non pour quitter.'.format(self.partie.joueur_actif))
                if reponse == "yes":                # le message box nous demande si on veut vraiment quitter ou
                    self.nouvelle_partie()          # jouer une nouvelle partie
                    return
                else:
                    self.destroy()
                    return

        except CestPasLeBonJoueur as e:                             # exception le joueur na pas encore jouer
            self.messages['foreground'] = 'red'
            self.messages['text'] = e
        self.messages['text'] = "Humain! c'est à ton tour"          # on rassur le jouer (et surtout moi!) que tout s'est bien passé
        self.mon_label_info['text'] = "C'est au tour du joueur blanc"

        # question philosophique qu'es ce que l'intelligence???
#######################################################################################################################
    # si le joueur click sur le bouton fermé tk il affiche un message pour demander s'il veut vraiment quitter ou sauvé
    def demander(self):
        reponse=messagebox.askquestion("C'est une bonne partie...courage", "Si vous quittez, vous risquez de perdre la "
                                                                           "partie courante?\nCliquez sur 'Oui' pour "
                                                                           "sauvegarder la partie ou sur 'Non' pour "
                                                                           "quitter.".format(self.partie.joueur_actif))
        if reponse == "yes":
            self.save()
        else:
            self.destroy()
#######################################################################################################################
    def affichage_info(self):
        if self.canvas_echiquier.echiquier.piece_cible_mangé:               # si une piece à été manger
            c = self.canvas_echiquier.echiquier.piece_cible_mangé.couleur   # on fait l'affichage dans la liste
            if c == 'blanc':                                                # des prises
                self.prises_noir['text'] = self.prises_noir['text'] + '\n{}'.format(self.canvas_echiquier.echiquier.piece_cible_mangé)
            elif c == 'noir':
                self.prises_blanc['text'] = self.prises_blanc['text'] + '\n{}'.format(self.canvas_echiquier.echiquier.piece_cible_mangé)

        if self.partie.joueur_actif == 'blanc':                 # on affiche le déplacement dans la liste des infos
            self.depla_noir['text'] = self.depla_noir['text'] + '\n->{} de {} à {}'.format(self.piece_source, self.position_source, self.position_cible)
        else:
            self.depla_blanc['text'] = self.depla_blanc['text'] + '\n->{} de {} à {}'.format(self.piece_source, self.position_source, self.position_cible)
        self.canvas_echiquier.dessiner_cases()
        self.canvas_echiquier.delete('piece')
        self.canvas_echiquier.dessiner_pieces()
        self.mon_label_info['text'] = "C'est au tour du joueur {}".format(self.partie.joueur_actif)
        self.messages['foreground'] = 'black'
        self.messages['text'] = 'Le déplacement a été effectué avec succès'
#######################################################################################################################
    # cette fonction ouvre le fichier ReadME.txt qui contient les règles et consignes d'utilisation, ce fichier se
    # trouve dans le dossier actuel ou se trouve ce module
    def infos_et_règles(self):
        fenetre_infos = Toplevel()
        fenetre_infos.title('Informations sur le jeu')
        label_consignes = Label(fenetre_infos, borderwidth=2, relief=RIDGE, font=("DejaVu Sans", 10), text="Vous trouverez les règles du jeu d'échecs en bas. "
                                                                                                          "Mais d'alors je vous explique les fonctionnalités du programme.\n"
                                                                                                          "- La partie commence avec le joueur blanc (toujours)\n"
                                                                                                          "####################################################################################################################\n"
                                                                                                          "Label Info. (cette section contient certaines informations sur la partie)\n"
                                                                                                          "####################################################################################################################\n"
                                                                                                          "- Un texte dans le labelframe indique c'est le tour de quel joueur, selon l'alternance des tours.\n"
                                                                                                          "- Pour déplacer une pièce maintenez là avec le bouton gauche de la souris et déposez là dans la position de votre"
                                                                                                          " choix, le déplacement sera effectué ou non, selon la validité de celui-ci.\n"
                                                                                                          "- Tous les déplacements sont affichés dans les listes à gauche de l'échiquier 'Liste des déplacements joueur blanc' et "
                                                                                                          "'Liste des déplacements joueur noir' selon le joueur.\n"
                                                                                                          "- Si le déplacement génère une prise, la pièce mangée est affichée dans les listes, encore une fois, à gauche de l'échiquier "
                                                                                                          "'Prises du joueur blanc' et 'Prises du joueur noir' selon le joueur.\n"
                                                                                                          "####################################################################################################################\n"
                                                                                                          "Label menu. (cette section contient les principales fonctionnalités du jeu)\n"
                                                                                                          "####################################################################################################################\n"
                                                                                                          "- Un bouton 'Nouvelle partie', pour démarrer une nouvelle partie, le programme va vous proposer de sauvegarder la partie " \
                                                                                                        "courante.\n" \
                                                                                                        "- Un bouton 'Sauvegarder la partie' qui sauvegarde la partie dans un fichier .txt (vous devrez choisir l'emplacement " \
                                                                                                        "et le nom du fichier).\n" \
                                                                                                        "- Un bouton 'Charger une partie' qui charge la partie depuis un fichier .txt (vous devrez choisir l'emplacement  " \
                                                                                                        "du fichier).\n" \
                                                                                                        "- Un bouton 'Informations sur le jeu' qui ouvre le présent document.\n" \
                                                                                                        "- Un bouton 'Annuler le dernier déplacement' qui annule le dernier déplacement, et seulement le dernier déplacement.\n" \
                                                                                                        "- Une case à cocher si vous voulez que le programme vous montre les déplacements possibles pour une certaine pièce\ " \
                                                                                                        "(il vafalloir choisir la pièce que vous voulez avec le bouton droit de la souris).")
        label_consignes.grid(row=0, column=0,sticky=N+E+W)
        label_règles = Label(fenetre_infos, borderwidth=2, relief=RIDGE, font=("DejaVu Sans", 10), text = "Quelques règles de jeu d'échecs..."
                                                                                                         "\n####################################################################################################################"
                                                                                                         "\nJe vois dans les mots-clés que certains aimeraient savoir comment on va à dame, ou comment on"
                                                                                                         "récupère une pièce, ou si on peut manger le roi... Alors hop! \nPetit cours d'échecs, rapide, sur ce qui"
                                                                                                         "semble vous préoccuper."
                                                                                                         "\nUn échiquier comporte 64 cases sur lesquelles il y a, au début de la partie, 32 pièces : 8 pions + 8"
                                                                                                         "pièces légères/lourdes et roi \n(2 tours, 2 cavaliers, 2 fous, la dame, le roi) aussi bien chez les"
                                                                                                         "noirs que chez les blancs."
                                                                                                         "\nLa dame se place 'sur sa couleur' : une dame blanche se place sur la case blanche centrale de sa rangée."
                                                                                                         "\nUne dame noire sur la case noire, en face de la dame blanche de toute façon. Le roi se place sur la case voisine."
                                                                                                         "\nDe gauche à droite, chez les blancs (qui se placent sur les colonnes 1 et 2, voir chiffres et lettres sur les côtés"
                                                                                                         "\nde la plupart des échiquiers), on a : tour cavalier fou dame roi fou cavalier tour. Et un pion devant chaque pièce."
                                                                                                         "\nLa case la plus proche d'un joueur, tout à droite, doit être une case blanche, sinon c'est que l'échiquier est mal fichu."
                                                                                                         "\nOn ne mange pas le roi. Sauf en blitz chez les disons euh... bourrins, et en parties amicales uniquement. Mais dans"
                                                                                                         "\nun tournoi de blitz, prendre le roi sera considéré comme un coup illégal et occasionnera la perte de la partie pour"
                                                                                                         "\ncelui qui a mangé le roi. Alors qu'il suffit de dire à l'adversaire qu'il a perdu car son roi était en échec et"
                                                                                                         "\nqu'il n'a pas paré l'échec."
                                                                                                         "\nPour récupérer une pièce, il faut amener un pion à promotion, c'est-à-dire le faire avancer jusqu'à ce qu'il soit"
                                                                                                         "\narrivé sur la rangée tout au bout de l'échiquier et donc qu'il ne puisse plus avancer. Au moment où on pose le pion"
                                                                                                         "\nsur la dernière case, on peut le remplacer par n'importe quelle pièce de sa couleur, sauf le roi. Si on choisit"
                                                                                                         "\nune dame mais qu'on a toujours la sienne sur l'échiquier, on peut prendre une tour retournée ou une pièce, ou ce"
                                                                                                         "\nqu'on veut pour représenter la deuxième dame. Mais attention!!! En tournoi, une tour renversée reste une tour,"
                                                                                                         "\nil faut donc arrêter la pendule (cet appareil qui mesure le temps de réflexion des joueurs et est, selon les"
                                                                                                         "\nparties, amie ou ennemie...), appeler l'arbitre et lui demander une dame. On peut aussi choisir une autre pièce,"
                                                                                                         "\nmais la dame étant la pièce la plus polyvalente, c'est généralement elle qui est choisie. [mais bien évidemment,"
                                                                                                         "\nsi en choisissant une dame on met l'autre pat il vaut mieux choisir une autre pièce]."
                                                                                                         "\n####################################################################################################################"
                                                                                                         "\nSource:"
                                                                                                         "meosine, Quelques règles de jeu d'échecs...<http://meosine.canalblog.com/archives/2008/02/18/8003563.html>, 18 février 2008"
                                                                                                         "\n######################################################################################################################")
        label_règles.grid(row=1, column=0,sticky=N+E+W)
