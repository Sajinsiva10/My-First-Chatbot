import os
import math


def list_files(directory
               ,extension):  # fonction qui permet de parcourir la liste des fichiers d’une extension donnée et dans un répertoire donné.
    files_names = []  # créaton d'une liste files_names pour stocker les noms de chaque fichier.
    for filename in os.listdir(directory):  # Parcours tous le fichiers dans le répertoire spécifié
        if filename.endswith(extension):  # Vérifie si le nom du fichier se termine par l'extension
            files_names.append(filename)
    return files_names


prez_files = list_files("speeches-20231108",
                        ".txt")  # Utilisation de la fonction liste_fichiers pour obtenir la liste des fichiers avec l'extension .txt
# Calcul le nombre de fichier de la liste prez_fichiers
nfile = len(prez_files)
prez_name = {"Jacques": "Chirac",
            # Création d'un dictionnaire associant chaque prénom à des noms de dirigeants politiques

            "Valéry": "Giscard dEstaing",
            "François": "Hollande",
            "Emmanuel": "Macron",
            "françois": "Mitterand",
            "Nicolas": "Sarkozy"}


def prez_lastname():  # Fonction pour stocker les noms de president dans une liste
    prez_lastnam = []
    for filename in prez_files:
        with open("speeches-20231108/" + filename, "r") as file:  # Ouverture du fichier en mode lecture
            j = 0
            for char in file.read():
                if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                            "."]:  # Si le caractère est un chiffre ou un point, arrête la boucle
                    break
                else:
                    j += 1
            if (file.read(11)[
                11:j]) not in prez_lastnam:  # Lecture d'une portion du fichier pour obtenir le nom de famille puis vérifie si le nom est dans la liste prez_lastam
                prez_lastnam.append(file.read(11)[11:j])
    return prez_lastnam


def convert():
    for element in prez_files:
        with open("speeches-20231108/" + element, "r") as r, open("Cleaned/" + element,
                                                                  "w") as c:  # Ouverture du fichier original en mode lecture (r) et du fichier nettoyé en mode écriture (w)
            for line in r.readlines():
                for character in line:
                    if ord("A") <= ord(character) <= ord("Z"):  # Convertit les majuscules en minuscules
                        c.write(chr(ord(character) + (ord("a") - ord("A"))))
                    elif ord(character) == ord("'"):  # Remplace l'apostrophe par la lettre "e" et ajoute un espace
                        c.write("e ")
                    elif ord(character) == ord("-") or ord(character) == ord(
                            "_"):  # Remplace le tiret ou le tiret du bas par un espace
                        c.write(" ")
                        # Supprime la ponctuation spécifiée
                    elif (ord(",") <= ord(character) <= ord(".") or ord(":") <= ord(character) <= ord(";") or ord(
                            character) == ord("?") or ord(character) == 33):
                        c.write("")
                    else:
                        c.write(character)


def score_tf(string):  # focntion qui calcule le score tf de chaque mot grâce à un dictionnaire
    dic = {}  # Initialisation du dictionnaire pour stocker les occurrences des mots
    if type(string) == list:  # Vérification, si l'entré est une liste
        for i in range(len(string)):
            if string[i] in dic:  # Vérifie si le mot est dans le dictionnaire
                dic[string[i]] += 1  # Si oui, incrémentation du compteur
            else:
                dic[string[i]] = 1  # Si non, incrémentation du compteur à 1
        return dic

    else:
        # Si l'entrée est une chaîne de caractères, séparation des mots en utilisant l'espace comme délimiteur
        b = string.replace('\n', ' ')
        a = b.split(" ")
        for i in range(len(a)):
            if a[i] in dic:
                dic[a[i]] += 1
            else:
                dic[a[i]] = 1
        return dic


def score_idf():  # focntion qui calcule le score idf grâce à un dictionnaire.
    dic = {}  # Dictionnaire pour stocker les occurrences des mots dans tous les documents
    dicidf = {}  # Dictionnaire pour stocker le score IDF pour chaque mot

    for element in prez_files:
        with open("Cleaned/" + element, "r") as c:
            for ligne in c.readlines():
                for lr in ligne.splitlines():  # Division de la ligne en une liste de lignes
                    a = lr.split(" ")
                    for i in range(len(a)):
                        if a[i] in dic and a[i] != "":
                            dic[a[i]] += 1
                        elif a[i] not in dic and a[i] != "":
                            dic[a[i]] = 1

    for element2 in prez_files:
        # Dictionnaire temporaire pour stocker la présence de mots dans chaque document
        tempdic = {}
        with open("Cleaned/" + element2, "r") as d:
            for ligne2 in d.readlines():
                for lr in ligne2.splitlines():
                    b = lr.split(" ")
                    # Parcours de chaque mot dans le premier dictionnaire
                    for mot in dic:
                        # Vérification si le mot est présent dans la ligne
                        if mot in b:
                            tempdic[mot] = 1

        for el in tempdic:
            dicidf[el] = dicidf.get(el, 0) + 1  # Incrémentation du compteur global du mot

    for ele in dicidf:
        dicidf[ele] = math.log10(nfile / dicidf[ele])  # Calcul du score IDF pour chaque mot

    return dicidf


def tf_idf_matrix():  # focntion qui permet de calculer les scores tfidf et de les stocker dans une matrice
    idfdic = score_idf()  # création d'une matrice tfidf
    mtfidf = []  # Liste pour stocker les scores TF-IDF du document actuel

    for element in prez_files:
        newlist = []
        with open("Cleaned/" + element) as f:
            readfile = f.read()
            for e in idfdic:
                if e in score_tf(readfile):  # Vérification de la présence du terme dans les scores TF
                    newlist.append(
                        round(score_tf(readfile)[e] * idfdic[e], 2))  # Calcul du score TF-IDF et ajout à la liste
                else:
                    newlist.append(0.0)
        mtfidf.append(newlist)

    return mtfidf  # Retour de la matrice TF-IDF complète
matrix = tf_idf_matrix()

def print_tfidf_matrix():  # fonction qui permet d'afficher la matrice
    mtfidf = matrix
    idfdic = score_idf()
    x = 0
    print(" " * 34, end=" ")
    maxlen = 0
    for word in idfdic:
        if len(word) > maxlen:  # Mise à jour de la longueur maximale si nécessaire
            maxlen = len(word)
        print(word, " " * (34 - len(word)), end=" ")  # Affichage du mot avec un espacement approprié
    print(maxlen)
    print("\n")
    for element in prez_files:
        print(element, " " * (32 - len(element)), end=" ")
        for value in mtfidf[x]:
            if len(str(value)) == 2:
                print(value, " " * 32,
                      end=" ")  # Affichage de la valeur avec un espacement approprié basé sur la longueur du nombre
            elif len(str(value)) == 3:
                print(value, " " * 31, end=" ")
            elif len(str(value)) == 4:
                print(value, " " * 30, end=" ")
        print("\n")
        x += 1


def ex1():
    idfdic = score_idf()
    matrixx = matrix
    uniml = []  # Liste pour stocker les termes uniques
    x = 0
    for element in idfdic:
        unim = True
        for i in range(8):
            if matrixx[i][x] != 0.0:  # Vérification si la valeur est différente de zéro
                unim = False
        if unim:
            uniml.append(element)
        x += 1
    return uniml


def ex2():
    idfdic = score_idf()
    matrixx = matrix
    maximum = 0.0
    maxlist = []
    x = 0  # Initialisation de la valeur maximale
    for _ in idfdic:
        for i in range(8):
            if matrixx[i][x] > maximum:  # Vérification si la valeur est supérieure à la valeur maximale actuelle
                maximum = matrixx[i][x]
        x += 1
    for i in range(8):
        x = 0
        for element in idfdic:
            if maximum == matrix[i][
                x]:  # Si la valeur maximale dans le document i est égale à la valeur actuelle dans la matrice TF-IDF
                maxlist.append(element)
            x += 1
        x += 1
    if len(maxlist) == 1:
        return maxlist[0]
    else:
        return maxlist


# focntion qui retourne le(s) mot(s) le(s) plus répété(s)
def ex3():
    unimportant_words = ex1()
    max1 = 0
    max1w = ""
    max2 = 0
    max2w = ""
    with open("Cleaned/Nomination_Chirac1.txt", "r") as file:
        read1 = file.read()
        dic1 = score_tf(read1)
        dic2 = score_tf(read1)

        for element in dic1:
            if dic1[element] > max1 and element != '' and element not in unimportant_words:
                max1 = dic1[element]
                max1w = element
        for element in dic2:
            if dic2[element] > max2 and element != '' and element not in unimportant_words:
                max2 = dic2[element]
                max2w = element
        if max1w == max2w:
            return max1w
        else:
            return max1w, max2w


# focntion qui indique le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation » et celui qui l’a répété le plus de fois
def ex4():
    listprez = []
    for element in prez_files:
        f = open("Cleaned/" + element)
        reading = f.read()
        dic = score_tf(reading)
        if "nation" in dic and element.strip("Nomination_").strip(".txt").strip("1").strip(
                "2") not in listprez:  # Vérification de la présence du mot "nation" dans le dictionnaire et exclusion des duplicatas
            listprez.append(element.strip("Nomination_").strip(".txt").strip("1").strip(
                "2"))  # Ajout du nom du président dans la liste
    return listprez


def ex5():
    prez = []
    for element in prez_files:
        f = open("Cleaned/" + element)
        reading = f.read()
        dic = score_tf(reading)
        if "climat" or "écologie" in dic:
            if element.strip("Nomination_").strip(".txt").strip("1").strip(
                    "2") not in prez:  # Vérification de la présence du mot "climat" ou "écologie" dans le dictionnaire et exclusion des duplicatas
                prez.append(element.strip("Nomination_").strip(".txt").strip("1").strip("2"))
    return prez


def ex6():
    dic = {}
    unim = ex1()
    f = open("Cleaned/Nomination_Chirac1.txt")
    reading = f.read()
    f.close()
    basewordlist = reading.split()
    for element in prez_files:
        f = open("Cleaned/" + element)
        reading = f.read()
        wordlist = reading.split()
        for element2 in basewordlist:
            if element2 not in wordlist:
                basewordlist.remove(element2)
    for i in range(len(basewordlist)):
        if basewordlist[i] in dic:
            dic[basewordlist[i]] += 1
        else:
            dic[basewordlist[i]] = 1
    basewordlist = []
    for element3 in dic:
        if element3 not in unim:
            basewordlist.append(element3)
    return basewordlist


def tokenisation(string):
    motvide = ["le", "de", "et", "la", "à", "est", "les", "pour", "un", "une"]
    motquestion = ["comment", "pourquoi"]
    finalstr = ""
    for charac in string:
        if ord("A") <= ord(charac) <= ord("Z"):  # Convertit les lettres majuscules en minuscules
            charac = chr(ord(charac) + (ord("a") - ord("A")))
            finalstr += charac
        elif ord(charac) == ord("'"):
            charac = "e "  # Remplace les apostrophes par 'e'
            finalstr += charac
        elif ord(charac) == ord("-") or ord(charac) == ord("_"):
            charac = " "  # Remplace les tirets et underscores par des espaces
            finalstr += charac
        elif (ord(",") <= ord(charac) <= ord(".") or ord(":") <= ord(charac) <= ord(";") or ord(charac) == ord("?")
              or ord(charac) == 33):

            charac = ""  # Supprime certains caractères de ponctuation
            finalstr += charac
        else:
            finalstr += charac
    exstr = finalstr.split()  # Divise la chaîne traitée en une liste de mots
    for element in exstr:
        if element in motvide or element in motquestion:  # Crée une nouvelle liste avec les mots qui ne sont pas dans motvide et motquestion
            exstr.remove(element)
    return exstr


def whichincorpus(q):
    wordic = score_idf()
    wordlist = tokenisation(q)  # Tokenise la question
    for element in wordlist:
        if element not in wordic.keys():  # Vérifie si l'élément n'est pas dans le dictionnaire des scores IDF
            wordlist.remove(element)
    print(wordlist)


def question_tf(
        string):  # Fonction qui permet de retourner un dictionnaire des scores TF après tokenisation de la question
    string2 = tokenisation(string)
    dictfq = score_tf(string2)
    return dictfq


def question_tf_idf(string):
    qlist = []
    tf_s = question_tf(string)
    idfs = score_idf()
    for element in tf_s:
        if element in idfs:  # Vérifie si l'élément est présent dans les scores IDF
            qlist.append(round(tf_s[element] * idfs[element], 2))  # Calcul du score TF-IDF et ajoute à la liste
        else:
            qlist.append(0.0)

    return qlist, tokenisation(string)[
        qlist.index(max(qlist))]  # Retourne la liste des scores TF-IDF et le terme ayant le score maximal


def produit_scalaire(a, b):
    scal = 0.0  # Initialisation de la variable pour stocker le résultat du produit scalaire
    for i in range(len(b)):
        scal += a[i] * b[i]  # Ajout du produit de chaque paire d'éléments correspondants
    scal += sum(a[i:])
    return scal


def norme(a):
    normv = 0.0
    for element in a:
        normv += element ** 2
    normv = 0.0
    for element in a:
        normv += element ** 2  # Ajoute le carré de chaque élément à la somme
    normv = math.sqrt(normv)  # Calcul de la racine carrée de la somme des carrés pour obtenir la norme
    return normv


def calcul_similarite(a, b):
    sim = produit_scalaire(a, b) / norme(a) * norme(
        b)  # Calcul de la similarité cosinus en utilisant la formule (a . b) / (|a| * |b|)
    return sim


def calcul_pertinent(corpus, v_question, listenoms):  # Focntion qui retourne le nom du document le plus pertinent

    maximum = 0.0
    vlist = v_question[0]
    filename = ""
    mot_pertinent = v_question[1]

    x = 0  # Compteur pour parcourir les éléments dans listenoms
    for element in listenoms:

        sim = calcul_similarite(corpus[x],
                                vlist)  # Calcul  la similarité  entre le vecteur question et le vecteur du corpus
        if sim > maximum:  # Mise à jour du maximum et du nom du fichier si la similarité actuelle est plus grande
            maximum = sim
            filename = element

        x += 1
    if filename == '':
        return "Désolé, nous ne pouvons pas répondre à cette question pour le moment."
    return "speeches-20231108/" + filename, mot_pertinent, maximum  # Retourne le résultat final (nom du fichier, mot pertinent, et similarité maximale)


def phrase(fichier):
    try:
        with open(fichier[0], 'r') as f:
            r = f.read()
            saviour = r.splitlines()
            for element in saviour:
                x = element.split(" ")
                if str(fichier[1]) in x:
                    for e in x:
                        print(e, end=" ")
                    break
    except FileNotFoundError:
        return "Désolé, nous ne pouvons pas répondre à cette question pour le moment."
