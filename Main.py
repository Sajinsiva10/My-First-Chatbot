import Core
import time
question_starters = {"Comment":"Après analyse, ",
                     "Pourquoi": "Car ",
                     "Peux-tu":"Oui, bien sûr ! "
                     }
print("Bienvenue dans le menu principal")
time.sleep(1.3)
while True:
    ans = str(input("Voulez-vous accéder aux fonctionnalités de la partie I ou au mode Chatbot ? \n"))
    if ans.lower() in ["fonctionnalités", "partie i", "partie 1", "1"]:
        stay = True
        while stay:

            print("1. Afficher la liste des mots les moins importants dans le corpus de documents.")
            print("2. Afficher les mots ayant le score TD-IDF le plus élevé.")
            print("3. Indiquer les mots les plus répétés par le président Chirac "
                  "hormis les mots dits « Non importants ».")
            print("4. Indiquer les noms des présidents qui ont parlé de la « Nation »")
            print("5. Indiquer le premier président à parler du climat et/ou de l’écologie")
            print("6. Hormis les mots dits «non importants», "
                  "quel(s) est (sont) le(s) mot(s) que tous les présidents ont évoqués.")
            print("7. Quitter le mode fonctionnalités.")
            choice = int(input("Choisissez un nombre entre 1 et 7 : "))

            if choice == 1:
                print("La liste des mots les moins importants sont :", Core.ex1())
                time.sleep(3)
            elif choice == 2:
                print("La liste des mots ayant le score TD-IDF le plus élevé est :", Core.ex2())
                time.sleep(3)
            elif choice == 3:
                print("Les mots les plus répétés par le président Chirac sont :", Core.ex3())
                time.sleep(3)
            elif choice == 4:
                print("Les présidents ayant évoqué la nation sont : ", end="")
                for i in range(len(Core.ex4())-1):
                    print(Core.ex4()[i], end=", ")
                print(Core.ex4()[-1])
                time.sleep(3)
            elif choice == 5:
                print("Les présidents parlant du climat et/ou de l'écologie sont :", Core.ex5())
                time.sleep(3)
            elif choice == 6:
                print("Voici la liste des mots répétés par tous les présidents, "
                      "hormis les mots non-importants :", Core.ex6())
                time.sleep(3)
            elif choice == 7:
                rester = False
            else:
                print("Choix invalide. Veuillez choisir une option de 1 à 6.")
                time.sleep(2.5)
    elif ans.lower() == "chatbot":
        q = input("Entrez votre question ci-dessous : \n")
        qlist = q.split(" ")
        if qlist[0] in question_starters:
            print(question_starters[qlist[0]])
            Core.phrase(Core.calcul_pertinent(Core.matrix,Core.question_tf_idf(q),Core.prez_files)[0:2])
        else:
            Core.phrase(Core.calcul_pertinent(Core.matrix, Core.question_tf_idf(q), Core.prez_files)[0:2])

        print("\n")
