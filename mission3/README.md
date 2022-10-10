# Mission 3

## Objectif

L'objectif final de cette mission est de produire à l'écran un dessin du drapeau de l'Union Européenne :

Pour y parvenir, vous allez devoir décomposer votre problème en une combinaison de sous-problèmes plus simples, et correctement et précisément spécifier ces sous-problèmes, les résoudre sous forme de fonctions Python, que vous utiliserez ensuite pour résoudre votre problème principal.

Vous allez travailler avec les graphiques tortue de Python, en utilisant le module turtle. Vous allez procéder par étapes.

Organisation : vous travaillerez à nouveau en binômes de deux étudiants. Associez-vous à un étudiant différent de la semaine dernière; faites une tournante au sein de votre groupe.

Considérez le programme suivant :

    import turtle                # module des graphiques tortue
    tortue = turtle.Turtle()     # créer une nouvelle tortue
    tortue.speed("fastest")      # tracé rapide

    def square(size, color):
        """Trace un carré plein de taille `size` et de couleur `color`.

        pre: `color` spécifie une couleur.
                La tortue `tortue` est initialisée.
                La tortue est placée à un sommet et orientée en direction d'un
                côté du carré.
        post: Le carré a été tracé sur la droite du premier côté.
                La tortue est à la même position et orientation qu'au départ.
        """
        tortue.color(color)
        tortue.pendown()
        tortue.begin_fill()
        for i in range(4):
            tortue.forward(size)
            tortue.right(90)
        tortue.end_fill()
        tortue.penup()

Ce programme définit une fonction square qui trace un carré avec la tortue. Essayez de lire et de comprendre ce programme. Sur base de la spécification en tête de la définition de square, pouvez-vous prédire précisément le résultat de l'exécution de square(200, "red") ?

Créez un nouveau fichier flags.py qui contiendra votre programme pour cette mission, et recopiez-y le programme ci-dessus. Exécutez-le dans Thonny, puis exécutez l'instruction square(200, "red") et observez son comportement. Le résultat est-il conforme à votre prédiction ? Testez les différentes couleurs disponibles :

["black", "blue", "green", "red", "magenta", "cyan", "yellow", "white"]

Exécutez help(square) dans l'interpréteur pour afficher la documentation de square [1].

Dans votre fichier, écrivez une fonction rectangle(width, height, color) qui trace un rectangle de dimensions width x height et de couleur color. Ecrivez d'abord la spécification, développez ensuite le code qui réalise cette spécification. Exécutez et testez votre programme.

Ecrivez (et spécifiez) une fonction belgian_flag(width) qui dessine un drapeau belge de largeur width et de proportions 3/2. Utilisez bien sûr la fonction rectangle que vous venez de construire.

Ecrivez (et spécifiez) une fonction plus générale three_color_flag(width, color1, color2, color3) qui dessine un drapeau tricolore de couleurs données. belgian_flag peut maintenant être re-défini comme three_color_flag(100, "black", "yellow", "red"). Ecrivez de même des fonctions dutch_flag, german_flag, luxemburg_flag et french_flag qui dessinent les drapeaux des pays voisins de la Belgique. Sur quelle fonction plus générale allez-vous vous baser ?

## Notes de moi même

Le programme "condensé" se trouve dans main_standalone.py
Mais j'ai, pour plus de lisibilité, découpé mon projet en classes et en plusieurs fichiers.
Le fichier *main_standalone.py* est donc **standalone**, il peut s'executer tout seul
Tandis que le rest est une unité, dont le point d'entée est main.py