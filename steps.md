# Etapes élémentaires de construction

Je tente la méthodo suivante : test unitaire puis fonction associée puis compléter le test fonctionnel.

**Création d'une première page avec la liste des tricount sur laquelle on peut créer un tricount et cela incrémente la liste.**
    -`Ecrire mon test fonctionnel : l'utilisateur voit le titre, voit la liste des tricount disponibles.`
    -`Ouvrir une première page avec marqué tricount en titre.`
    - `Ajouter un bouton Créer un nouveau tricount qui envoie vers une autre page.`
    - `Débugger le test unitaire vérifiant qu'on passe sur la bonne url en cliquant (car ça marche bien)`
    - `Compléter le test fonctionnel et voir s'il passe. Débugger ce test`
    - `Créer en html cette page remplissage qui contient en input Titre, Description, catégorie en liste déroulante.`
    - `Créer la redirection vers la page listecount une fois le formulaire soumis. Débuuger le test (j'ai ajouté l'url, la fonction view et mis l'url dans le form du html) : tester rajouter le csrftoken.`
    -`Débugger pourquoi; même si la redirection vers count marche, cette adresse n'est pas reliée à index.html alors qu'elle le devrait.`
    -`Créer une première classe de données avec les trois infos à entrer.`
    -`Ecrire le test pour la ligne suivante.`
    -`Ajouter la récupération de données dans la fonction addcount.` 
    -`Créer les récupérations de données via une fonction qui redirige vers la liste des tricount.`
    - `Test fonctionnel`
    - `Faire en sorte que le nouveau tricount  apparaîsse dans la page (html).`
    - `Test fonctionnel`
    - `Compléter le test fonctionnel pour entrer un second tricount avec une autre catégorie.`
    - `Débugger : comprendre pourquoi tricount 2 semble avoir un type différent que tricount 1`
    - `Factoriser la fonction du test fonctionnel en créant une fonction faisant une création de tricount.`
    - `Débug : quelle est cette erreur quand j'intègre mes fichiers static?` 
    -`faire le css de la page de la liste des tricount.`
    -`Réfléchir à comment faire pour avoir plusieurs images de fond qui se répètent en css.`
    -`Débugger mon test fonctionnel : comprendre quelle adresse est parcourue après chaque send_keys`
    - `Empêcher l'entrée en base de données si on ne met pas titre ou catégorie et renvoyer vers la page de newcount avec en plus un message d'erreur en rouge au bon endroit.`
    - `si pas de description, on met "pas de description."`
    -`Ajouter des majuscules dans l'affichage des titres et description.`  
    -`Test que les participants apparaissent bien.`
    -`Modifier le code newcount.html pour qu'ils apparaissent.`
    -`Associer les participants créés au tricount.`
    -`Modifier le test unitaire pour prendre en compte le numéro du participant : (créer deux tricount avec des participants diff et compter que le nb de participants est correct.)`
    -`Modifier aussi le test fonctionnel pour vérifier que Jean n'apparait pas dans la page après que le tricount a été validé.`
    -`Faire en sorte qu'une fois le tricount créé, les participants disparaissent de la page newcount. Il suffit dans la fonction newcount de ne passer que les participants du number le plus gd.`
    - `Modifier la page remplissage pour qu'on puisse y intégrer des participants (étape par étape précédé d'un test unitaire).`
    -`Ajouter un bouton retour en arrière sur newcount au cas où il ne veut finalement pas créer de tricount.`
    -`Compléter le test fonctionnel : le participant revient en arrière et retombe sur la bonne page avec la liste des tricount.`
    -`voir si le submit de newcount passe les tests si je le transforme en a ou button. `
    -`je ne peux pas cliquer sur le back de newcount. C'est lié au header images (commenté plus de pb)` 
    -`Débugger le fond bleu de button.`
    -`voir comment on écrit cliquer en css.` 
    -`Mettre le select en cadres arrondis : remplacer mon select par une série de bouton avec des classes différentes. Celui qui est cliqué devient bleu.`
    -`Quand j'envoie le tricount, on doit récupérer dans view la valeur du bouton cliqué (commande isactive?).`
    -`Ajouter les images au bouton.`
    -`Ajouter à l'html le nombre de participants créées.`
    -`Ajouter au test fonctionnel si l'affichage du nombre est correct.`
    -`Faire en sorte qui si on clique sur retour, les participants éventuellement enregistrés en bdd soient supprimés. Réfléchir d'abord aux différentes solutions pour éliminer les participants créés.` 
    -`Créer l'adresse de la page des devises.`
    -`Créer un html.`
    -`Créer une fonction vue qui pointe vers l'html des devises. Faire passer le currency json.`
    -`Modifier le code pour mettre les fichiers css dans un dossier nommé css.`
    -`Modifier le lien lors de la création du tricount : on va vers la page des dépenses et pas vers la liste des tricounts.`
        `Créer une nouvelle p html, une url and une vue pour les dépenses.`
        `Test fonctionnel : on doit arriver sur l'url dépense quand on valide un tricount. Modifier aussi les tests unitaires qui buggeraient.`
        `Test fonctionnel : quand il est sur dépense et qu'il revient en arrière,  on tombe sur le liste des tricount avec les bonnes choses à l'intérieur.`
        `Modifier la fonction vue newcount pour qu'on arrive sur l'html des dépenses quand on valide le tricount.` 
    -`Améliorer le style de spending.html.`
        `ajouter les symboles`
    `-faire en sorte que l'url de la dépense soit associée au tricount (que chaque tricount ait sa page dépense).`
        `commencer par transformer les counts de listecount en liens vers la page tricount.`
        `associer l'id du tricount à l'url : url à changer, view à changer (passer le nom du tricount et des participts grâce à l'id du count qui sera pk).`
        `Modifier aussi la fonction addcount pr rediriger vers la bonne url.`
        `Faire en sorte que quand on clique sur le tricount dans index on soit dirigé vers le bon tricount.`
        `changer le test count en créant deux url et en vérifiant qu'on tombe bien sur deux url différentes.`
        `ajouter les données du tricount dans spending.html (remplacer name tricount et syr tout les participants). Comment récupérer le nom des participants?`
        `comment mesurer le nombre d'objets d'un query set.`
        `test fonctionnel : cliquer sur deux liens différents et voir si on tombe sur deux url uniques associées au bon tricount. Vérifier que le bon nom de tricount et les participants est inscrit.`
        `Bug : quand on reclique sur le tricount 2 (fin de test fonctionnel) le titre est là, en revanche les participants ont disparu.`
        `voir comment obliger à ce qu'il y ait au moins un participant pour valider le tricount : le bug est lié au fait qu'on peut créer un count sans participant du coup dans listecount on passe dans la condition d'élimination des participants;`
        `Factoriser le test fonctionnel , factoriser les fonctions check aussi en plusieurs fonctions élémentaires.`
        `dans spending et newcount, voir si /count ou /count/ (les tests fonc marchent avec les deux mais pas les tests unitaires qu'il faut débugger avec /count/)`
    -`css : en rouge le msg d'erreur pour les participants + les bords deviennent rouges si non remplis`
    -`créer l'entrée d'une dépense.`
        `-créer un nouveau html avec les catégories factices, l'url est la vue associées.`
        -`passer à l'html le nom des participants au tricount et ajouter les montants dans le css`
        -`test fonctionnel`
        - `modifier model pour les données.`
        - `modifier la vue addspending pour récupérer les données : titre, montant, payeur.`
        - `test unitaire  : les données sont bien dans la bdd.`
        - `test fonctionnel : le nom des participants apparaît. Le montant apparaît bien.`
        - `ajouter dans l'html spending les data du spending pour faire passer le test fonctionnel.` 
        -`checkbox toutes cochées par défaut.`
        - `ajouter le retour en arrière qui retourne à la liste des dépenses.`
        - `si pas de titre, titre obligatoire.`
        - `si pas de montant, le montant par défaut est 0`
        - `test unitaire : commencer à créér une dépense revenir en arrière, rien dans la bdd`
        - `test unitaire : pas de montant, la bdd augmente avec le montant 0.`
        - `test unitaire : pas de titre, la bdd n'augmente pas.`
        - `test fonc créer une seconde dépense et voir si ça se passe bien.`
        - `test fonctionnel : retour en arrière, création sans titre puis sans montant. A débugger`
        -`regarder comment Romain importe ses sous fichiers si ceux ci sont constitués de classes. Est-ce qu'on est obligé d'instancier une classe?`
        - `factoriser le code testfonctionnel en utilisant les fonctions élémentaires sans tests qu'on met éventuellement dans un autre fichier. Commencer par testspendingcreation.`
        - `transformer addaparticipant en add participants.`
        - `factoriser aussi les redondances sur les tests unitaires (les blocs d'assert qui se répètent, les beautiful soup...).`
    -`créer le module de calcul des équilibres après dépense.`
        `fabriquer des tests pour chacune des fonctions créée.`
        `ajouter le calcul auto des montants pr chaque participant coché (cas équitable).`
    - `voir test.resolvesolution et test calculate total credit si je ne me suis pas trompé dans le calcul des crédits (si les signes ne sont pas inverses) : car j'ai mis receiving update au lieu de spending update.`
    - `comparer les css et voir si factorisable en un fichier avec structure minimale commune et des spécificités par ailleurs. Voir alors comment importer dans un css la structure commune.`
    - `Ecriture d'un event onclick sur la première page prenant en compte juste le premier bouton.`
    - `écriture du html et js pour display options`
    - `ajouter le comportement lorsqu'on clique sur parameters-options.`
    - Modif du + pour créer un élt qui lui va mener vers la page du nouveau tricount ou une page rejoindre un tricount.
    -`page de nouvelle dépense : JS quand on clique sur  simple, on revient à une répartition équitable des parts de chacun.`
    -`Modifier les tests unitaires et fonctionnels en conséquence pr que ça tourne toujours.`
    - `écrire les tests pr le JS de la page de newcount.`
    - Bug : réussir à supprimer la bdd à distance après le premier test. linktricount-1 échoue car la bdd à distance contient 3 tricounts après le premier test.
    -création de la page d'une dépense donnée :
        -`créer nouvelle url, vue qui renvoit vers l'html élémentaire.`
        -`rentrer l'adresse href du a dans spending pour cliquer sur une dépense donnée`
        -`débugger le premier jet des tests fonctionnels.`
        -`écrire le test fonctionnel et les éventuels tests unitaires.`
        -`css sur la liste des dépenses à améliorer.`
        -`améliorer html et css.`
        -`placer en css précédent et suivant.`  
        -`Décommenter la nouvelle vue de add spending pour voir si cette fois les données sont récupérées et si ça tourne.`
        -`ajouter à la bdd les montants que chacun doit payer pour une dépense donnée : récupérer les montants calculés en JS.`
        -`test unitaire à modifier.` 
        -`transférer les données de la dépense à la page : ajouter à la bdd les montants payés par chacun.`
        -`ajouter la date à la bdd et lors de la création de la dépense.`
        -`modifier le test unitaire pour voir si la date est passée.`
        -`modifier les tests fonctionnels de spending-details.`
        - faire fonctionner le bouton modifier.
    -faire la page équilibre de spending.html:
        `créer nouvelle url`
        `créer l html`
        `préparer le css`
        `créer la vue qui passe les données à cette page`
        `créer l'objet tricount de calculation quand un tricount est créé, ajouter cet objet à la bdd. (vue addcount)`
        `modifier les tests unitaires (avec assertJSONequal). Voir pourquoi receivers contient deux noms (pb de create a tricount?).`
        `comprendre comment marche cls : je pense qu'il faut que dans ma fonction fromjson je crée l'objet et mette à jour puis je retourne l'objet.`
        `A chaque sérialisation, je perds l'objet, il faut donc recréer les objets après chaque déserialisation : attention, en l'état actuel, chaque création remet les valeurs des crédits à 0. Il faut donc réinitialiser en veillant bien à remplacer les valeurs de départ par les dernières valeurs calculées (sont concernés: dict_participants et total_cost).`
        `quand une dépense est ajoutée, modifier l'objet de la bdd. (vue addspending) (essayer la première désérialisation en mettant bien à jour).`
        `modifier les tests unitaires, notamment faire un test avec deux dépenses successives pour voir si les crédits sont corrects : test_multiple_spending (reprendre le test resolvesolution)`
        `dans spending equilibria, récupérer l'objet et lancer updateprocess pour passer en arg totalcredit et transferttoeq.`
        `ajouter à l'html toutes les infos à passer sur les comptes notamment : participants, leur crédit, la solution de paiment pour équilibrer (update_process donne tout). `
        `débugger les tests fonctionnels existants : probable que cela vienne de ma page spendingequilibria.html. Comprendre pourquoi il désérialise dans test_multiplespending et pas dans spending equilibria. Essayer de désérialiser à d'autres endroits (notamment dans une autre vue), afficher le JSON pour voir si identique à plusieurs endroits. Lié au fait qu'on ait modifié l'objet dans la bdd suite à l'ajout d'une dépense? Voir comment on l'a déserialisé dans addspending. Peut-être que je l'ai mal resérialisé dans update_spending...`
        `Voir ptet pour transformer dico python les obj participants puis les envoyer dans le dico de Tricount et ne sérialiser en json qu'à ce moment-là (éviter d'avoir un JSON dans un JSON). (reviendrait à ne pas mettre les participants en json mais juste en python).`
        `modifier le test fonctionnel qui doit voir apparaître les crédits et la solution : créer de multiples dépenses comme testmultiplespending et vérifier que les bonnes infos sont affichées.`
        `dans spending equilibria mettre les noms des participants en alternance à gauche ou à droite.`
        `Améliorer le css de spending equilibria pour faire des barres de taille correspondant au total_credit.`
        `Fusionner la branche.`
        `transformer les boutons dépenses et équilibres en a avec href`
        `tests fonctionnels associés`
    -`suppression de la classe Participant dans la bdd`
        `voir comment avec POST je pourrais récupérer la liste des participants ajoutés. (request.POST.lists())` 
        `supprimer de model`
        `supprimer la fonction vue addparticipant`
        `supprimer l'url addparticpt`
        `récupérer les participants seulement quand on crée le tricount pas avant`
        `faire marcher testnewcountinputs de test.count :`
            `-Pb de client.post : dans test_functions create tricount: comment passer les participants un à un (normalement avec l'input new_participant) comme on le ferait sur la page avec le client. Il est possible qu'on ne puisse pas sans sendkeys de selenium (et que ça marche même si testnewcountinputs ne marche pas) (quand j'affiche request.POST, new_participant contient bien la liste, mais les éléments nameparticipant n'ont pas été créés.2506). Essayer dans test_functions de faire un post directement avec nameparticipant (comme si on les avait entré un par un avant).`
            -`Autre pb sûrement indépendant: comment récupérer les participants dans views.addcount (normalement avec les éléments nameparticipant). Voir avec request.post.lists la syntaxe et tenter de créer un tricount sur la page web. Jusqu'ici, quand je valide le form, il n'arrive pas à récupérer les partcpts et m'affiche "il faut au moins un ptcpt". Pb semble lié au JS car quand je mets deux participants direct dans le html, il voit bien des participants (et le static close passe bien).   ptet que pb dû au fait que le input new_participant soit hors du form.oui`
        `modifier les tests unitaires (au moins les premiers pour créer un tricount) et fonctionnels`
        `modifier ensuite toutes les fonctions de vue une à une puis le test unitaire associé. (J(ai mis un repère à l'endroit à partir duquel modifier.))`
        `les patcpts ne doivent être ajoutés enlevés que via le JS qui rajoute un elt : ce doit être un input text car on veut le récupérer.`
        `newcount.js : faire en sorte que l'image static pour fermer les participants soit acceptée.`
        `voir si dans mes tests_fonctionnels, j'ai un morceau où j'enlève des participants et qu'ils disparaissent de la page.`
        `améliorer le css de newcount.`
        `JS : faire qu'on ne puisse pas ajouter des participants vides.`
        `newcount.js : changer le nb de participants dans nb_participants à chaque ajout de participant. (vérifier que mes mises à jour dans userAddingParticipant et userClosingParticipant fonctionnent).`
    -`voir pour mettre des fichiers dans le gitignore : ce sont ces fichiers qui sont conflictuels.`
    -pour la prochaine grosse fonctionnalité, créer une branche puis essayer de la merger.
    -ajouter le loggage :
        `-recenser les choses à modifier dans les différentes pages.`
        `-créer l'adresse de register et le html de register (en cours).` 
        `-créer la vue register en redirigeant vers le login`
        `-JS de welcome et login : si on ne remplit pas un des champs on ne peut se logger ou s'enregistrer comme nouvel utilisateur.`
        -améliorer le css de ces pages welcome et login.
        `- test fonctionnel associé`
        `-créer l'url de logout et le html de logout (c'est la page obtenue en cliquant sur Mes paramètres.) + css (en cours)`
        -`rediriger mes paramètres vers l'url de logout.`
        `-créer une vue login qui rend login.html`
        -`test unitaire pour vérifier que la bdd est bien incrémentée avec register.`
        -`test unitaire pour login?`
        -`test fonctionnel (enregistrement arrivée sur login.html login et clic sur mes paramètres : arrivée vers logout modifier newvisitortest); Débugger afficher le html comprendre où on atterrit après l'enregistrement.`
        -`factoriser le test fonctionnel avec une fonction pour l'enregistement et une pour le loggage.`
        -`passer à ma vue welcome les messages.info pour les afficher si on utilise un nom déjà utilisé.` 
        -test fonctionnel associé.
        `-créer une url et vue obtenue quand on crée un nouvel utilisateur` 
        `-créer une url et vue obtenue quand on se connecte, qui va regarder si l'user est dans la bdd et rediriger vers la bonne page.`
        `-Débugger le NewVisitorTest et Modifier tous les tests fonctionnels et unitaires pr prendre en compte le str:user dans les url.`
        `-test unitaire + test fonctionnel`
        `-créer une url et vue obtenue quand on se délogge, qui va délogger le participant et rediriger vers la page de connection.`
        `-test unitaire + test fonctionnel`
        `-revoir comment on fait en django avec auth.`
        -mettre en première proposition dans tout tricount créé le participant loggé. 
        -enlever des tests fonctionnels de création de tricount le participant loggé qui doit être automatiquement créé.
        -il faudra ptet enlever la page welcome et tout ce qui lui est relié sauf si on introduit une première page autre que l'enregistrement/connection. 
        -afficher en bas de la liste des dépenses, le coût total du loggé.
        -page spending equilibria : proprio en gras + les équilibrages concernant le proprio doivent être dans Comment puis-je équilibrer? 
        -merger la branche puis créer un dépôt distant github et y déposer mon git supprimer ma branche puis travailler avec gitflow pour apprendre.
    - Ecrire un fichier de commande qui permet de lancer tous les tests fonctionnels ou alors certains d'entre eux.
    -Ajouter la possibilité d'une arrivée d'argent et d'un transfert et pas juste une dépense:
        Ajouter au html et au css le bouton correspondant
        Faire le JS correspondant.
        Prendre en compte dans la vue addspending que ce soit une dépense ou un reçu.
    Points qui nécessitent sûrement JS.
        -`Ajouter le nombre de caractère écrit sous le titre et la description et le limiter à   50 (resp 500). (Javascript nécessaire pour récupérer des données en temps réel).`
        -`Ajouter la possibilité de supprimer les participants qu'on vient d'ajouter via la  petite croix. Pour le moment quand je clique sur les croix, ça ajoute des    participants. (Je pense que j'ai besoin de JS aussi).`
        -Ajouter dans devise.html la recherche de currency (JS sûrement nécessaire).
        -Ajouter dans newcount.html, le select de la devise qui mène à currency.html : il   semble que JS soit nécessaire pour revenir. 
        -Ajouter à l'html les devises via le json. 
        -Test fonctionnel pour voir si tout est affiché et si on va vers la bonne url.
        -`pb à résoudre : quand j'écris un titre et que j'entre un participant, le titre n'est pas conservé : voir comment garder ça : (devrait être résolu en passant en JS : plus de chgt d'url)`
        -quand on clique sur la loupe dans la page de dépenses, on a une barre de recherche qui apparaît.
    Tests JS : voir comment en faire facilement sans selenium.


# Bug non résolu : 
    

# Bugs intéressants 
    - TIME SEND KEYS : Après send_Keys, il faut laisser du temps pour que la page se charge.
    - URL : Faire bien attention à respecter le fait qu'il y ait ou non / dans les adresses (faire pareil que dans le path : si j'ai mis count/ dans le path il faut le mettre après dans les redirections) sinon on aura une réponse inappropriée ( 404 ou autre).
    - URL SELECTONE : la méthode selectone de BeautifoulSoup donne l'url sans / à la fin. Attention à ne pas oublier de le rajouter si nécessaire.
    - FAUX BUG de redirect : quand on utilise la fonction post du client et que cela mène à une redirection, la réponse n'a pas de contenu c'est juste une redirection même si on redirige vers une autre fonction de view qui elle a un contenu.
    - CSS NON CHARGE : quand je mets à jour un css et que je lance le serveur, le css n'est pas forcément appliqué. Le navigateur utilise en fait l'ancien css gardé dans la mémoire cache. Il suffit de supprimer le cache dans l'historique récent.
    - STATICLIVESERVER : Attention avec Liveservertestcase, les tests fonctionnels ne parviennent pas à charger les fichiers css. Il faut utiliser le serveur de test Staticliveservertestcase.
    - GET(Pk=1) différent de first() : first() ne correspond pas forcément à pk=1 quand on veut récupérer un objet. Il se peut qu'on ait créé des objets avant comme pour ma classe participants par exemple. 
    - FORM SUBMIT : Il semble que si on remplace le input ayant la classe submit par un button avec la même classe, l'envoie des données se fasse alors que si on choisit un a cela n'envoie plus les données.
    - SELECTONE ID : attention quand on sélectionne un élément via a#qqch, qqch est l'identifiant (repéré par un # comme en css). qqch ne peut être la classe.
    - TYPE FLOAT BDD : Si on entre un float ou int dans la bdd via un request, celui-ci est convertit en str par request.POST. Donc ne pas oublier de le convertir si on a utilisé un champ FloatField.
    - SEVERAL FUNCTIONAL TESTS : when we launch tests, it creates a database and destroys it at the end of all tests. So to avoid bugs, don't forget to erase the database created by the first test.
    - Le JS apparaît et disparaît : c'est sûrement dû à un comportement par défaut. Dans mon cas c'était un lien a qui par défaut envoie vers une autre page.
    - DEFAULTVALUENOTSUBMITTEDBYpost : Quand j'introduis un input avec value (par défaut) et que j'utilise la méthode post du client django : la valeur n'est pas transmise. Pourquoi? C'est la méthode post du client django qui ne les soumet pas, elle envoie les données qu'on spécifie et ne permet pas de récupérer les spécifiées. En revanche quand un utilisateur soumet, les valeurs par défaut sont bien envoyées. Une solution : on peut récupérer les valeurs par défaut avec un get puis les passer dans le post.
        # Récupérez la page du formulaire avec self.client.get
        response = self.client.get("/count/newcount/addcount")

        # Extrayez les valeurs par défaut des champs depuis le contenu de la réponse HTML
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        default_test_value = soup.find("input", {"name": "test"})["value"]

        # Utilisez les valeurs par défaut extraites pour construire le dictionnaire de données
        form_data = {
            "newtricount_title": title,
            "newtricount_description": description,
            "newtricount_category": category,
            "test": default_test_value  # Utilisez la valeur par défaut
        }

        # Soumettez le formulaire avec self.client.post
        response = self.client.post("/count/newcount/addcount", data=form_data)
    -TAGS DJANGO EN JS : dans un fichier JS qui crée un html avec un tag django, il faut spécifier l'adresse d'un fichier static (ne pas utiliser les tags mais "/static/...). Il ne reconnaît pas les tags DJANGO côté client seulement côté serveur.
    -JSONfield : Attention pour stocker des chaînes JSON, mieux vaut utiliser models.Textfield que JsonField car celui-ci rend un objet JsonStr qui est différent d'un str et si on veut utiliser json.loads pour recréer un dico python, cela peut bugger du fait du type de l'objet. 
    -NOSUCHTABLE : pb de bdd, supprimer la base, vérifier que le dossier migrations et init existent bien et refaire les migrations.
    -JS PREVENTDEFAULT : quand je cliquais sur un input submit avec un event click qui m'affichait 1, il n'affichait pas 1 car le comportement par défaut était de soumettre le formulaire.
    -JS PREVENTDEFAULT 2 : quand on empêche l'event par défaut de submit, les inputs ne sont pas remis à 0 : cela implique que le texte précédemment tapé est toujours là.

# Mes difficultés principales


# Des enseignements intéressants :
    -pour rendre les tests lisibles : créer des fonctions sans tests avec des noms équivoques et mettre les tests en dehors. L'idée est que quand je lis le test fonctionnel, je comprenne ce qu'on fait. J'ai créé un module avec une classe de fonctions élémentaires sans tests. Chaque fonction idéalement doit avoir une action. 