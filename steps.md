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
    - Débug : quelle est cette erreur quand j'intègre mes fichiers static? avec runserver le css apparaît, avec les tests fonctionnels le css n'apparaît pas et il y a l'erreur qui est signalée. Peut-être lire le bouquin pour comprendre cette erreur bizarre mais il semble que ce soit lié au test fonctionnel. Premier élt de réponse : le traceback qui n'est pas une erreur de test apparaît dès que je fais un retour à la page count qui contient le css. Il n'affiche pas le css d'ailleurs (contrairement avec runserver) : tout se passe comme s'il ne pouvait pas lire le css en passant par le test fonctionnel : est-ce lié à LiveTestServer? Selenium? Pas de pb si on met le css dans index.html. C'est donc le lien vers le css qui pose pb lors du test fonctionnel.Il est possible que ça soit l'url différente de celle de runserver qui n'arrive pas à se lier au css. Essayer de remettre l'adresse classique (voir test fonctionnel de tdd) sinon voir le livre. Voir réponse chatgpt. Tester en revenant à unittest et en remettant l'adresse 8000 : ça doit fonctionner.
    -faire le css de la page de la liste des tricount.
    -Empêcher l'entrée en base de données si on ne met pas titre ou catégorie: si pas de description, on met pas de description.
    -Ajouter des majuscules dans l'affichage des titres et description.
    -Ajouter un lien vers un choix de devise qui mène à une autre page html.
    - Test fonctionnel 
    - Modifier la page remplissage pour qu'on puisse y intégrer des participants.
    -Modifier le lien lors de la création du tricount : on va vers la page des dépenses et pas vers la liste des tricounts.



# Bugs intéressants 
    - TIME SEND KEYS : Après send_Keys, il faut laisser du temps pour que la page se charge.
    - URL : Faire bien attention à respecter le fait qu'il y ait ou non / dans les adresses (faire pareil que dans le path : si j'ai mis count/ dans le path il faut le mettre après dans les redirections) sinon on aura une réponse inappropriée ( 404 ou autre).
    - FAUX BUG de redirect : quand on utilise la fonction post du client et que cela mène à une redirection, la réponse n'a pas de contenu c'est juste une redirection même si on redirige vers une autre fonction de view qui elle a un contenu.
    - CSS NON CHARGE : quand je mets à jour un css et que je lance le serveur, le css n'est pas forcément appliqué. Le navigateur utilise en fait l'ancien css gardé dans la mémoire cache. Il suffit de supprimer le cache dans l'historique récent.
    - 



# Mes difficultés principales
    - Non connaissance des syntaxes du client django pour faire des tests unitaires. Idem pour les fonctionnels.