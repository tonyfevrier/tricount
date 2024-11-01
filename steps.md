# Etapes élémentaires de construction

Méthodo : écriture d'une fonctionnalité puis écriture de tests unitaires (si la fonctionnalité touche à des choses internes : bdd) puis compléter le test fonctionnel. 


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
    `-faire la page équilibre de spending.html:`
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
    `-pour la prochaine grosse fonctionnalité, créer une branche puis essayer de la merger.`
    `-ajouter le loggage :`
        `-recenser les choses à modifier dans les différentes pages.`
        `-créer l'adresse de register et le html de register (en cours).` 
        `-créer la vue register en redirigeant vers le login`
        `-JS de welcome et login : si on ne remplit pas un des champs on ne peut se logger ou s'enregistrer comme nouvel utilisateur.`
        `-améliorer le css de ces pages welcome et login.`
        `- test fonctionnel associé`
        `-créer l'url de logout et le html de logout (c'est la page obtenue en cliquant sur Mes paramètres.) + css (en cours)`
        -`rediriger mes paramètres vers l'url de logout.`
        `-créer une vue login qui rend login.html`
        -`test unitaire pour vérifier que la bdd est bien incrémentée avec register.`
        -`test unitaire pour login?`
        -`test fonctionnel (enregistrement arrivée sur login.html login et clic sur mes paramètres : arrivée vers logout modifier newvisitortest); Débugger afficher le html comprendre où on atterrit après l'enregistrement.`
        -`factoriser le test fonctionnel avec une fonction pour l'enregistement et une pour le loggage.`
        -`passer à ma vue welcome les messages.info pour les afficher si on utilise un nom déjà utilisé.` 
        `-test fonctionnel associé.`
        `-créer une url et vue obtenue quand on crée un nouvel utilisateur` 
        `-créer une url et vue obtenue quand on se connecte, qui va regarder si l'user est dans la bdd et rediriger vers la bonne page.`
        `-Débugger le NewVisitorTest et Modifier tous les tests fonctionnels et unitaires pr prendre en compte le str:user dans les url.`
        `-test unitaire + test fonctionnel`
        `-créer une url et vue obtenue quand on se délogge, qui va délogger le participant et rediriger vers la page de connection.`
        `-test unitaire + test fonctionnel`
        `-revoir comment on fait en django avec auth.`
        `-mettre en première proposition dans tout tricount créé le participant loggé.` 
        `-enlever des tests fonctionnels de création de tricount le participant loggé qui doit être automatiquement créé. Modifier le newcount.JS pour refuser un participant déjà ajouté.`
        -il faudra ptet enlever la page welcome et tout ce qui lui est relié sauf si on introduit une première page autre que l'enregistrement/connection. 
        `-afficher en bas de la liste des dépenses, le coût total du loggé.`
        `-Débugger : comprendre pourquoi dans mon test fonc, quand je crée une dépense dans le tricount de Dulciny, Dulciny n'apparait dans le dict_participants. Bug dans la vue addcount le get list ne récupère pas le premier participant.`
        `-Débugger, mes tests fonctionnels ne passent plus à cause de createspending qui répartit uniformément sur les participants alors que je voudrais que ce ne soit que sur Jean et Henri. Changer cela : la répartition est automatique sur les ptctps via JS donc ajouter le 3ème.`
        `-page spending equilibria : proprio en gras + les équilibrages concernant le proprio doivent être dans Comment puis-je équilibrer?` 
        `-merger la branche puis créer un dépôt distant github et y déposer mon git supprimer ma branche puis travailler avec gitflow pour apprendre.`
    - Ecrire un fichier de commande qui permet de lancer tous les tests fonctionnels ou alors certains d'entre eux.
        -`Ajouter le nombre de caractère écrit sous le titre et la description et le limiter à   50 (resp 500). (Javascript nécessaire pour récupérer des données en temps réel).`
        -`Ajouter la possibilité de supprimer les participants qu'on vient d'ajouter via la  petite croix. Pour le moment quand je clique sur les croix, ça ajoute des    participants. (Je pense que j'ai besoin de JS aussi).`
    -branche currency
        -`créer une page avec les currency qui sont des a qui redirigent vers la page newcount en passant l'argument de la currency.`
        -`page newcount : input dans lequel on va passer la currency choisie.`
        -`test fonctionnel : dans la création du tricount, on clique sur la page des currency et on vérifie que la bonne monnaie est passée.`
        -`améliorer le css de currency.html`
        -`compléter newcount.js pour que lorsqu'on clique sur currency on mette ce qui est rempli dans le localstorage et quand on revient on préremplit avec ce localstorage.`
        -`deux bugs : quand je reviens en arrière et que je relance un tricount puis je clique sur currency, le localstorage des participants précédents réapparait.`
        -`bug 2 : je peux mettre plusieurs fois le même participant.`
        -`test fonctionnel modifier : retourner changer de currency après avoir mis des participants et vérifier s'ils sont toujours là.`
        -`modifier la bdd et la création des tricounts.`
        -`modifier les tests unitaires pour contrôler les modifs dans la bdd.` 
        -`Modifier dans toutes les pages de dépenses EUR par la currency choisie.`
        -`Ajouter dans devise.html la recherche de currency (JS).`
        -`écrire un test fonctionnel pour vérifier que ce JS fonctionne bien.`
        -`merger la branche puis la pousser vers le dépôt distant.`
    -consommer l'API currency converter de rapid API pour afficher dans la liste des dépenses le total en livres.
        - `créer une branche API currency.`
        - `importer l'API dans la vue de spending`
        - `y convertir le total amount en livre par exemple`
        - `afficher le contenu de la réponse dans la vue pour l'afficher dans un test `
        - `le transmettre à l'html.`
        - `lancer les tests pour voir ce qui est affiché (normalement il existe déjà des tests qui lancent spending)`
        - bug : comprendre pourquoi le coût en euro n'apparaît plus (css). 
        - écrire test fonctionnel pour voir si la monnaie changée est bien affichée.
        - `merger la branche avec master`
        - `rebaser la branche chat à master.`
    -`branche pour le chat entre les participants :`
        - `voir comment fonctionne ajax et quelles sont les autres sol pr l'affichage en temps réel.`
        - `partie du serveur à l'utilisateur :` 
            `créer la base de app.py`
            `créer la base du JS pour l'ouverture et la fermeture de la websocket : elle s'ouvre quand on entre sur la page et elle se ferme si on la quitte.`
            `tester dans count, l'ouverture d'une websocket quand la page chat est lancée.`
            `partie client en JS : si on envoie un message, envoi via protocole socket`
            `partie client : si un message arrive, il est ajouté à la page.`
    - `interaction multiutilisateur sur un même tricount:`
            `bug : pourquoi mettre eltinitially hidden avant footer.append fait que clonertricount s'affiche alors qu'après ce n'est pas le cas. (à mon avis ça vient de goback`
            `ajouter une popup lorsqu'on crée un tricount pour laisser choisir entre créer de rien ou cloner un tricount existant`
            `si on clique hors de la page la popup disparaît`
            `test fonctionnel`
            `ajouter l'ajout d'un mdp de tricount lors de la création d'un tricount`
            `obliger à mettre un pwd pour la validation`
            `modif test fonctionnel et serveur`
            `clic sur clone, apparition d'une popup où l'user doit entrer son prenom et mot de passe`
            `améliorer le css des boutons et form`
            `bug au premier clic sur cloner le form s'affiche mais si je recommence ce n'est plus le cas.`
            `finir d'écrire clone tricount de userexperience puis le test fonctionnel.`
            `si prenom ou mdp incorrect, rediriger vers la liste des tricount du user et envoyer un message du style "aucun tricount n'a ce mdp".`
            `si on laisse le form vide, fonction JS qui laisse un msg d'erreur`
            `test fonctionnel`
            `ajouter liste d'admin au tricount, y intégrer le créateur`
            `débugger mes tests : bug de multiUsers à comprendre (le clic sur id newcount ne semble pas ouvrir clonecount)`
            `dire de n'afficher le tricount que si le user est dans la liste des admins.`
            `documenter mieux `
            `puis pousser à distance sur github`
            `si mdp correct, ajouter à la liste des admin du tricount`
            `modifier views (listecount je pense) pour afficher les tricount dont la personne est admin (et pas tous les tricount)`
            `test serveur pour vérifier que les données sont apparues dans la bdd du user, et que des tricount dont il n'est pas admin n'apparaissent pas.`
            `test fonctionnel`  
            `JS à vérif : le error n'apparaît pas.`
            `débugger le test (impression qu'il y a un pb avec le JS de id newcount parfois : regarder sous quelle condition j'ai bloqué le bouton)`
            `test fonctionnel à compléter`
            `faire en sorte qu'il y ait mdp + un identifiant (comme le nom du créateur du tricount)`
            `finir debug test fonctionnel`
    - `modifier les données d'un tricount et des dépenses déjà crées`
            `page après clic sur le titre du count`
            `mettre l'html avec même format que celui de la creation`
            `ajouter les données au inputs qu'on peut modifier`
            `css`
            `renvoi vers la page du tricount après modif` 
            `bouton pour soumettre le nouveau formulaire`
            `créer l'url et la view qui récupère le form et modifie le tricount.`
            `enregistrement dans la bdd des nouvelles data après modif`
            `test unitaire pour vérifier les modifs changer ptcp titre, description`
            `test unitaire : calcul de dépense toujours correct (1 dépense, 1 ajout de participant, 1 dépense, toujours correct)`
            `tester le cas où on ajoute, le cas où on enlève et le cas où on ajoute et enlève`
            Un cas à penser : celui où on enlèverait un participant puis le remettrait (il serait réinitialisé à 0).
            `Ajouter à count.data modifyregister de views (si les participants ont été modifiés seulement), Robert en clé du dict_participants et en receveur des objets des autres participants, initialiser aussi le crédit de Robert pour tous les participants.`
            `debug du redirects`
            `Bug : le titre et la description si on ne la change pas et qu'on soumet le tricount, sont remplacés par rien!`
            `test fonctionnel où on change les mêmes choses et on arrive sur les bonnes url. (et avant les donnée du count appariassent bien en placeholder). dans test fonc vérifier que si un participant est exclu du groupe il est toujours dans les comptes à la fin.`
            `débug test fonc de registerspending et NewVisitor`
            `receiverbox devrait être in find elements et pas element. Pourquoi les id ne donnent pas les noms? voir comment envoyer une liste de checked via selenium`          
            `ajouter option supprimer + popup JS confirmer`
            `comprendre ce qu'il se passe avec useAPIcurrency : pb de l'api, éventuelt changer d'API.`
            `supprimer de la bdd le count supprimé`
            `test count pour vérifier que disparu de la bdd`
            `si bug avec le tag django dans le js, je peux créer l'alert en hidden dans le html.`
            `bug : pour lui dernier élement est une div, ne récupère pas le a! n'arrive pas à cliquer sur le lien a : ajouter un nom de classe et ensuite le trouver de la même manière que backtolistecount. Il faudra sûrement modifier le JS. (Il trouve les éléments mais n'arrive pas à cliquer dessus : peut-être qu'il ne voit pas un a).`
            `bug : si pas EUR ca bug`
            `bug : dans modifycount les validations de tricount et le retour ne marchent pas sûrement à cause du JS alertBlockScreen`
            `CSS de l'alert` 
            `test fonc` 
            -` modifier l'entrée de dépenses (currency dans le form de addspending) pour permettre à l'utilisateur de rentrer dans une autre monnaie une dépense.` 
            -` ajouter monnaie au html en select` 
            -`views : rediriger vers la page de sélection des trucs` 
            -`JS pour transférer la monnaie choisie via url à la page de addspending` 
            -`views de la dépense : convertir la monnaie en la monnaie du tricount.`
            - `test unitaire où j'entre une dépense dans une autre monnaie`
            - `Debugger : trouver comment utiliser ma nouvelle api`
            - ` test unitaire : vérifier que la bonne monnaie est prise pr tricount mais aussi spending` 
            -` test fonc` 
    - modifier une dépense:
            - `créer le html, les url et vues : identique à newspending avec un bouton supprimer et titre modifier`
            - `bouton modifier à relier avec la bonne url`
            - `passer les données de la dépense à la vue et voir ce qu'il faut changer dans l'html.`
            - `calculer aussi le prix dans modify count register s'il change la currency.`
            - `test unitaire pour voir si la dépense est bien modifiée`
            - `test_unitaire : modifier modify a spending pour entrer des montants respectifs.`
            - `addspending et modifyspending (attention si on change de monnaie, les montants récupérés doivent aussi être modifiés) dico_receivers[receiver] = float(request.POST[receiver])`
            - `Debug des tests actuels unitaires` 
            - `test unitaire : vérifier que la dépense déjà entrée dans les calculs a bien été retirée des calculs puis que la nouvelle dépense a bien été ajoutée.`
            - `rajouter les montants respectifs dans modify spending de test count (views à modifier aussi pour updater les calculs liés au tricount).`
            - `test fonctionnel : modification d'une dépense vérification `
            - `Bug : quand je clique sur la monnaie de modifyspending, je suis renvoyé vers nouvelle dépense au lieu de modify dépense.`
            - s`BUG : quand je modifie l'amount de modify spending, il faudra supprimer ce qui est déjà écrit dans la case sinon il rentre 100.0100.`
            - `Bug : quand je crée un tricount en usd, les dépenses me sont proposées en euro, faudrait que ce soit en dollar. Sûrement relié au bug du test fonc où quand je modifie une dépense, il considère que je rentre des dollars. Une explication? Modifyspending.html est mis par défaut en EUR : passer à la vue la monnaie du tricount. Reproduire en test unitaire la config de mon test fonc : 2 tricount 1 en euro, 1 en dollar pour voir si le pb est originaire du calcul (RECUPERER LE MONTANT PAYE POUR CHAQUE (pas les crédits mais l'amount divisé en 4) mais la répartition de la somme de la dépense et voir si c'est correct après chaque dépense et modif de de dépesne)`
            - `Bug si je clique sur le backtolistecount de la page currency ça m'envoie toujours vers "Nouveau tricount".`
            - `Bug : sur la page modifyspending il faut mettre les valeurs de la dépense pour chaque partiicpant en placeholder.  spending.receivers.participant ne marche pas en tag django, solution ultime : passer la valeur via JS ou les mettre dans le contexte. Essayer avaec items pour voir si ça marche`
            - `modifier modifycount de views en mettant des value au lieu des placeholder dans le bon template pour enlever les if = "".`
            - `Attetntion je dois avoir le même bug pour addcount et addspending : si je ne clique pas sur currency, il ne doit sûrement y avoir aucune valeur de monnaie renvoyée (il faudra dire que si vide, renvoyer valeur par défaut dans views). Ca semble fonctionner voir si j'ai une différence de programmation.`
            - `faire le JS des checkbox de modifyspending puis éventuellement la fonction modifyspending de userexperience (partie où on clique sur la toggle box pour mettre tout le monde à checked : il faudra distinguer le cas où tous sont déjà cochées).`
            - `Verif : test spendingcreation`.
            - `test fonc : pour que les montants soient corrects, il va falloir non slt faire le JS de la toggle box de modifyspending et aussi modifier la fonction modifyspending de userexperience.`
            - `attention si je valide direct une modif de dépense sans rien changer ça bugge. Si rien n'a changé, il faudrait geler le bouton validation OU alors il faut enregistrer les valeurs qui sont dans placeholder.` 
    - `factorisation`
            - `factor : améliorer utils.py en créant une classe de méthodes appliquées à un tricount (structuration).`
            - `factoriser les modifyspending pour que ce soit plus clair. Utiliser createDictionaryReceivers et voir si je peux la mettre aussi dans addspending. Finir docstring de cette fonction.`
            - `Debug addspending.`
            - `faut-il factoriser pour modifier une dépense et un tricount et créer des fonctions userexperience pour ça. (oui fonction qui a pour arg, une dictionnaire avec les noms des classes des éléments à modifier et la valeur qu'on veut lui associer).`
            - `JS pour la suppression de dépense` 
            - `vue pour la suppression de la dépense + test unitaire associé`
            - `test fonctionnel : suppression de cette dépense vérification`
    - factorisation
            - `reprendre une page en scss après l'avoir installé en path.`
            - `factoriser : voir si je ne peux pas créer une fonction pour les findelements avec un nombre indéterminé d'élts à chercher.`
            - `fonc click on successive links (arrivé à MultiUsers), et aussi utiliser find multiple dans user experience.` 
            - `factoriser createspend et clickoncreate`
            - `effacer bdd pour la tester et notamment le JS de spending`
            - `remettre le dossier count/migrations qui a disparu et notamment le fichier init`
            - `bug à comprendre : pourquoi le amountbox qui fonctionnait avant ne fonctionne plus`
            - `bug repéré : quand on modifie le tricount, il faut effacer ce qu'il y a dans titre et description si on les modifie.`
            - `voir comment avoir ls dans cmd`
    - `créer un fichier de requirements.txt pour installer l'environnement tricount et installer avec ce fichier. Suppremier countenv et le recréer.`
    - `coupler avec une API de date pour entrer la date de la dépense : utiliser timezone plutôt`
    - `créer un fichier de lancement de tous les tests fonctionnels avec subprocess (voir run.py pour le chat). Faire en sorte qu'il compile automatiquement tous les scss avant le lancement.`
        - `bug voir pourquoi rien ne se passe`
        - `bug : pb avec process il ne semble pas trouver le fichier scss lorsque j'exécute ma commande`
        - `comprendre pourquoi tous les tests ne sont pas lancés`
        - `comprendre comment régler le bug stderr.decode`
        - `tests fonctionnels à débugger : voir chatgpt, stackoverflow, afficher page source pour voir si je le vois, essayer de le mettre plus haut dans la vue pour voir si on arrive à le cliquer. Créer un autre élément du même type pour voir ce qu'on arrive à cliquer. Voir docu selenium, comment cliquer un input radio, les autres tests bloquent où?`
            `bug lié à la classe newtricountcategory (soit pb css, soit js)`
        - `il faudra peut-être utiliser await pour bien attendre que les tests précédents se finissent avant qu'un autre ne se lance.`
        - `voir ce que propose django pour lancer tous les tests car il doit y avoir qqch.`
    - `faire disparaître le module JSONField et utiliser celui de django`
    - `réécrire les url pour qu'on ait une page d'accueil directement à l'url du liveserver.` 
        `enlever les user des url et utiliser le request.user.` 
        ` modifier le css des boutons a de la page welcome et login et des forms` 
        `changer les adresses welcome/qqch en qqch`
        `rediriger register et login vers la page des comptes si ça a marché`
        `modifier les tests pr qu'ils passent` 
        `tags url pour remplacer les grosses url en html`
        `reverse pour éviter d'écrire les url dans views`
        `raccourcir les noms de certaines url pour éviter les url à rallonge, exemple count/logout`
        `éviter de passer au maximum user dans les contexts si inutiles (si ce n'était utile que pour les url)`
        `currency.html : href à compléter : je crois que c'est le JS qui la complète, pas sûr`
    - `améliorer le login`
        `quand on s'enregistre, on tombe sur son compte et pas sur login`
        `css moche et peu visible`
        `améliorer le css des éléments boutons style loupe, le + du newtricount, les différences de polices quand clic sur +, le padding des messages d'erreurs, le CSS de confirmer supprimer le tricount..., pointeur de logout`
        `si échec d'authenfication, on devrait avoir des messages d'erreurs`
    - `bug : le compteur lorsqu'on ajoute des participants (/50) est-il correct? et quand on enlève celui qui possèdê, une croix reste à droite.`
        `autre bugs : relancer les tests et débugger`
            - `functional_tests.tests.JSTest.test_JS_of_listecount_page : pourquoi pas de participant principal lors de la création du tricount`
            - `testthepageofsomespendings`
            - `testcurrency bar`
    - `comment enlever l'autocomplétion lors de la création de tricount`
    - `reprendre mes fichiers html, écrire un layout avec des blocs comme dans mes projets edX (si c'est possible)`
    - `ans les block body enlever les gros conteneurs quitte à modifier le css`
    - `faire un css pour le container et modifier en conséquences les petits bugs de css`
    - `mettre des titres aux pages html`
    - modifier mes tests unitaires en créant un setup permettant d'enregistrer et logger systématiquement qqun (tests unitaires et peut-être aussi fonctionnels)
    - c`omprendre pourquoi si je suis loggé mais que je relance la page de log on me redemande mes identifiants: changer cela en redirection automatique à mon compte si je suis loggé`
    - `CSS des messages d'erreurs : mettre les messages à droite de la boite les concernant et pas en dessous et en + petits caractères.`
    - `factorisation des JS : créer un fichier de handler qu'on importe (des handlers sont réécrits plusieurs fois) quitte à leur ajouter des arguments. On pourrait faire un code par classe avec les handlers click, les handlers input etc.`
        `améliorer le js avec query selector pour plus de lisibilité (reste newspding modifycount.js)`
        `modifycount : obliger à la présence de deux participants, d'un titre et d'une description.`
        `remplacer alert par une confirmation pour empêcher tout autre event de se déclencher`
            `lier le oui à l'url pour la suppression du tricount`
            `supprimer la div hidden de deleteconfirmation du js, du html`
        `ajouter l'event domcontentloaded`
        `bien documenter`
    - `pour le clonage de tricount, autoriser qu'on mette une minuscule en première lettre du titre du tricount`
    - `l'affichage en pound a trop de chiffres après la virgule`
    - `pourquoi le clic sur un tricount déjà créé est si lent? `
    - `modifier newspending.js, addspending pour que la gestion des champs non remplis soient faits en JS et pas dans la vue.`
    - `modifier la confirmation de suppression de dépense par une alerte`
    - `modifier models pour que spending ait une foreignkey tricount`
    - `bugs`
        - `quand je supprime l'admin des tricounts, il n'est plus possible de cliquer sur le tricount url /tricount/1 ne marche plus`
        - `clic newcount quand je supprime le participant principal ça me supprime ce que j'ai entré et me met un message d'erreur pour le titre ou pwd (ce que je n'ai pas rempli).`
        - `pb avec le JS de newspending : Avancé et aussi le calcul des montants qui ne semble plus fonctionner, relancer les tests fonctionnels (pb que ce soit lié au fait que j'ai touché au html via des blocks et au CSS)`
        - `bug : j'ai rentré une unique dépense mais dans spending-details j'ai un bouton précédent!`
        - `depuis l'introduction de la loupe dans currency.html, la barre de recherche n'apparait plus (JS pb)`
        - `newcount : je peux enlever tous les participants (en commençant par enlever l'admin puis en enlevant les autres) et quand je clique sur valider il me remet l'admin.`
        - `On devrait en JS empêcher toutes les suppressions déjà (garantir toujours au - 1 ptcpt mais ajouter un message "Il faut au - un participant" qu'il faudra enlever de views). `
        - `quand clic sur valider alors que non rempli des messages apparaissent mais les participants sont réinitialisés : faire en sorte qu'ils soient conservés.`
            - `ajouter un event sur submittricount`
            - `supprimer de views.addcount pctpt`
            - `faire apparaître les messages d'erreurs via JS.`
            - `ajout d'une erreur si on tente de supprimer le dernier participant`
            - `supprimer les tests unitaires où tout nest pas rempli`
            - `modifier les tests fonctionnels`
            - `nettoyer newcount.js`
        - `je ne peux pas supprimer deux participants de suite : au deuxième il bascule sur l'url addcount comme s'il essayait de valider le tricount.`
        - `Sol : il faut enlever l'obligation de garder l'admin.`
        - `newcount : si je mets un ptcpt, je supprime l'admin et je change de monnaie, l'admin que j'ai supprimé revient alors que je voudrais le garder supprimé.`
        - `on peut mettre deux fois le même ptcpt`
        - `pb on ne peut faire de tricount sans l'admin`
        - `si je supprime l'admin et que je reviens de currency, l'admin est remis : JS pour ne remettre que les elts de list_participants et pas l'admin s'il a été supprimé avant`
    - `si le titre et le pwd pr cloner ne correspondent à rien, ajouter un message l'indiquant.`
        - `le faire en JS (avec une vue JS pour éviter le chargement de la page)`
        - `récrire la vue clonecount en rendant une JSON response.`
            - `modifier la requête pour récupérer le body`
        - `écrire le JS dans index.js faisant la requête`
            - `ne pas oublier le tokenv`
            `si les credentials sont faux, afficher un message d'erreur`
           ` sinon windowslocationhref vers l'url listecount (on ne recharge la page que si les credentials sont corrects)`
        - `enlever le form et le remplacer par un div`
        - `test unitaire puis fonctionnel`
        - `qd ça fonctionne enlever la div pwdcount qui ne sert plus et adapter css et js`
        - `indices sur le bug : `
            - `fetch quand il est mis dans parameters marche quand je clic sur les boutons mais pas sur a`
            - `semble être lié à un comportement avec les différents event de click`
            - `quand je clic direct sur envoyer le fecth marche, qd je clique en remplissant les deux champs ça ne marche plus et si après je reclic en ne remplissant rien, ça ne marche plus!!!!!!`
            - `Essayer d'enlever tous les comportements JS et voir si ça fonctionne.`
        - `après le débug, remettre les event listener et voir ceux qui font disparaitre le div de clonecount`
        - `voir ensuite si le tricount est bien cloné.`
    - `mettre aussi le msg d'erreur Remplissez mdp en rouge.`
    - bugs
        - modifyspending : quand je modifie la monnaie de la dépense déjà enregistrée, j'ai un bug
        - newspending et modifyspending ne permettent pas de conserver les données entrées avant d'avoir cliqué sur currency (utiliser localstorage comme dans newcount).
        - quand on supprime un participant et qu'on le remet, son ancien passif n'est pas conservé s'il avait fait des dépenses avant.
    - branche pour le chat (suite)
            - `copier l'html et voir si ça marche`
            - `copie de app et templates`
            - `créer un modèle qui conserve les messages`
            - `écrire une vue de type JS qui reçoit de manière asynchrone un message, l'enregistre en bdd et le renvoit avec la date et l'envoyeur.`
                - `ce renvoi doit s'adresser à tous les participants au tricount.`
                - modifier la vue pour que quand un participant se déconnecte, il revoit tous les messages précédents.
                - test unitaire pour voir si les messages précédents sont bien transmis par la vue
            - écrire dans chat.js :
                - `quand on charge le contenu on crée une ws`
                - `quand on clique sur submit, event envoyer un message`
                - `event ws.receive (un message): création d'un élément en bas de page affichant le message et ses infos`  
                - event ws.receive (création d'un indicateur rouge sur le tricount dans listecount ainsi que sur la cloche dans la liste des dépenses). 
            - écriture d'une vue JS qui renvoit un message particulier si quelqu'un est en train d'écrire (peut-être dans la même vue JS).
            - dans chat.js : 
                - si ws.receive un message de type "qqun écrit", écriture quelque part de "Untel est en train d'écrire". 
            - une vue (ptet encore la même pour l'envoi de likes)
            - dans chat.js :
                - enlever les likes de la bdd et vues, c'est du gadget j'ajouterai plus tard si nécessaire
                - si clic sur coeur, envoi d'un message avec like
                - affichage automatique au receive du nombre de likes à côté du coeur
            - `ajout au html : d'un message avec le jour avant la liste des messages lui correspondant`
            - `css de la page chat`
            - besoin de déclencher un serveur redis pour que ça fonctionne : voir si je peux donner un fichier yaml qui s'exécute automatiquement pour qqun qui voudrait lancer mon code.
            - faut il faire de l'asynchrone auquel cas il faut faire attention à ne pas accéder aux modèles en asynchrone
            - `voir comment remplir l'url dans routing.py et l'adresse ws dans le JS windonws.location.host?`
            - `test unitaire : voir comment vérifier que Chat a bien créé un message, comment intégrer une websocket en test unitaire.`
            - passer non plus la date complète mais juste le jour pour daydate et l'heure pour les posts
            - débug test fonctionnel en enlevant la bdd de test (en écrasant la base classique)
    - pour le projet edX:
        `** voir pour mettre des branches accessibles uniquement via login (@auth_login)`
        `regarder mon code et appli pour voir les axes d'amélioration clairs issus de la formation.`
        `faire les factorisations ci-dessus pour améliorer mon appli`
        ** apprivoiser les django channels pour intégrer le chat
        ** réfléchir bien au readme et à complexité (appli de calculation, chat websockets (si intégré), taille de l'appli, couplage avec API extérieures, tests unitaires, tests fonctionnels)
        - améliorer pour la pep8 : noms de fonctions en minuscule et _
        - réfléchir à utiliser le django cache framework : quelles parties pourraient s'améliorer en termes de performance? Lesquelles je ne voudrais pas recharger?
        * sécurité : mettre ma clé d'API non pas dans le code source mais dans une variable d'environnement ou la sécuriser.
        * sécurité : introduire le hachage des pwd dans mon application
        ** vérifier toutes les spécifications.
        ** vérifier le côté responsive du site : pas parfait exemple newspending
            - newcount: si écran > longueur max du titre, le titre est mdp sur la même ligne, les participants sur la même ligne au max avec des petites croix à côté et la bouton ajouter pas trop loin de Autre participant ET le formulaire de clonage en hauteur si écran < l
            - newspending, modifycount, modifyspending : idem montant et monnaie sur même ligne que titre
        - Optionnel : recherche dans les dépenses avec la loupe
        ** Nettoyer momentanément les boutons qui ne servent à rien en les commentant
        - créer variable de temps pour time.sleep dans tests fonctionnels : essayer de diminuer le temps
        - voir si des vues sont à passer en JS : se demander quand il est inutile de perdre du temps à recharger la page (exemple: pour clonecount, inutile de recharger quand les credentials sont faux).
        - CSS des ajouter pour que le ajouter soit mieux placé qqs taille écran - parfois on a l'affichage de la flèche retour en très grand (exe modifycount)
            centrer le Bonjour Tony de la page logout
        ** remettre l'API si ça marche après tous les tests effectués
        - faire des sous dossiers dans templates pour chaque application?
        * créer une docker image permettant aux examinateurs de créer facilement le conteneur associé à mon application
        * créer un fichier yaml permettant facilement de lancer mon application et un pour lancer les tests unitaires, fonctionnels.
        ** faire un yaml pour l'intégration continue de mon projet, voir si je peux aussi utiliser yaml non pas pour lancer des tests sur des dépôts distants mais pour programmer mes tests en local.
        - voir pour créer deux bdd dbsqlite différentes afin d'éviter son écrasement à chaque lancement des tests channels
        
    
    -modification des dépenses déjà entrées :
    -`pb à résoudre : quand j'écris un titre et que j'entre un participant, le titre n'est pas conservé : voir comment garder ça : (devrait être résolu en passant en JS : plus de chgt d'url)`
    -quand on clique sur la loupe dans la page de dépenses, on a une barre de recherche qui apparaît. 
    Tests JS : voir comment en faire facilement sans selenium.
    

# Bug non résolu : 



# Bugs intéressants 
    - Environnement et selenium : ne pas oublier d'installer un driver du navigateur utilisé pour les tests (geckodriver pour Firefox) et d'ajouter son chemin dans le path. Il faut aussi passer en option le chemin vers Firefox dans les tests.
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
    -TAGS DJANGO EN JS : dans un fichier JS qui crée un html contenant un tag django, il faut spécifier l'adresse d'un fichier static (ne pas utiliser les tags mais "/static/...). Il ne reconnaît pas les tags DJANGO côté client seulement côté serveur.
    -JSONfield : Attention pour stocker des chaînes JSON, mieux vaut utiliser models.Textfield que JsonField car celui-ci rend un objet JsonStr qui est différent d'un str et si on veut utiliser json.loads pour recréer un dico python, cela peut bugger du fait du type de l'objet. 
    -NOSUCHTABLE : pb de bdd, supprimer la base, vérifier que le dossier migrations et init existent bien et refaire les migrations.
    -JS PREVENTDEFAULT : quand je cliquais sur un input submit avec un event click qui m'affichait 1, il n'affichait pas 1 car le comportement par défaut était de soumettre le formulaire.
    -JS PREVENTDEFAULT 2 : quand on empêche l'event par défaut de submit, les inputs ne sont pas remis à 0 : cela implique que le texte précédemment tapé est toujours là.
    -HIDDEN FLEX INLINE : attention certains types de display empêchent le paramètre hidden de fonctionner. Le display = none est un bon remplaçant.
    - A VERSUS INPUT : Les <a> ne sont pas prévus pour encapsuler des input : quand je mets un input dans un <a>, si je mets une value par défaut, lorsque je soumets le formulaire, cette valeur n'est pas envoyée à la soumission.
    - JS LOCAL VARIABLES IN IF : les éléments définis dans un if n'existent que dans ce if. En particulier, s'il y a des handlers qui les utilisent, il faut les mettre dans le if.
    - SASS EXTEND : Attention il semble que si on utilise extend dans un élement, sass copie les attributs des enfants aussi. Cela peut mener à des absurdités : sélecteur avec des parents n'ayant pas l'enfant qui leur est associé. Pour parer à ça, on peut créer un élément fictif qui n'est pas dans le html et qui n'aura pas d'enfant et utiliser @extend de cet élément.
    - FETCH EVENT PREVENT DEFAULT: Si je mets un event click sur un input submit ou a ou sur un bouton dans un formulaire (qui du coup est assimilé à un input submit) et que je mets un fecth dedans, il faut veiller à bien empêcher le comportement par défaut sinon le fetch n'aboutit pas.
    - WEBSOCKET CONNECT : Dans settings, il y a un paramètre ALLOWED_HOSTS qui permet d'autoriser la connection à une websocket dans le protocolrouter de asgi avec AllowedHostsOriginValidator. Pour que les tests s'exécutent il faut autoriser l'host des tests ou plus simplement ALLOWED_HOSTS = ["*"]
    - TEST FONCTIONNELS CHANNELS : il faut ajouter les lignes "TEST": {
            "NAME": BASE_DIR / "db.sqlite3",
        } au dictionnaire DATABASES pour ces tests et seulement pour eux (pas les unitaires) car ces tests ne fonctionnent pas sur une bdd créée en mémoire comme c'est le cas pour STATICLIVESERVERTESTCASE.

# Mes difficultés principales


# Des enseignements intéressants :
    -pour rendre les tests lisibles : créer des fonctions sans tests avec des noms équivoques et mettre les tests en dehors. L'idée est que quand je lis le test fonctionnel, je comprenne ce qu'on fait. J'ai créé un module avec une classe de fonctions élémentaires sans tests. Chaque fonction idéalement doit avoir une action. 