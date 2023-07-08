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
    -Modifier le lien lors de la création du tricount : on va vers la page des dépenses et pas vers la liste des tricounts.
    -Modifier le code pour mettre les fichiers css dans un dossier nommé css.

    -Ajouter le nombre de caractère écrit sous le titre et la description et le limiter à 50 (resp 500). (Javascript nécessaire pour récupérer des données en temps réel.
    -Ajouter la possibilité de supprimer les participants qu'on vient d'ajouter via la petite croix. Pour le moment quand je clique sur les croix, ça ajoute des participants. (Je pense que j'ai besoin de JS aussi).
    -Ajouter dans devise.html la recherche de currency (JS sûrement nécessaire).
    -Ajouter dans newcount.html, le select de la devise qui mène à currency.html : il semble que JS soit nécessaire pour revenir.
    - Test fonctionnel. 
    -Ajouter à l'html les devises via le json.
    -Faire le css de l'html
    -Test fonctionnel pour voir si tout est affiché et si on va vers la bonne url.


# Bugs intéressants 
    - TIME SEND KEYS : Après send_Keys, il faut laisser du temps pour que la page se charge.
    - URL : Faire bien attention à respecter le fait qu'il y ait ou non / dans les adresses (faire pareil que dans le path : si j'ai mis count/ dans le path il faut le mettre après dans les redirections) sinon on aura une réponse inappropriée ( 404 ou autre).
    - URL SELECTONE : la méthode selectone de BeautifoulSoup donne l'url sans / à la fin. Attention à ne pas oublier de le rajouter si nécessaire.
    - FAUX BUG de redirect : quand on utilise la fonction post du client et que cela mène à une redirection, la réponse n'a pas de contenu c'est juste une redirection même si on redirige vers une autre fonction de view qui elle a un contenu.
    - CSS NON CHARGE : quand je mets à jour un css et que je lance le serveur, le css n'est pas forcément appliqué. Le navigateur utilise en fait l'ancien css gardé dans la mémoire cache. Il suffit de supprimer le cache dans l'historique récent.
    - STATICLIVESERVER : Attention avec Liveservertestcase, les tests fonctionnels ne parviennent pas à charger les fichiers css. Il faut utiliser le serveur de test Staticliveservertestcase.
    - GET(Pk=1) différent de first() : first() ne correspond pas forcément à pk=1 quand on veut récupérer un objet. Il se peut qu'on ait créé des objets avant comme pour ma classe participants par exemple. 
    - FORM SUBMIT : Il semble que si on remplace le input ayant la classe submit par un button avec la même classe, l'envoie des données se fasse alors que si on choisit un a cela n'envoie plus les données.
    

# Mes difficultés principales
    - Non connaissance des syntaxes du client django pour faire des tests unitaires. Idem pour les fonctionnels.