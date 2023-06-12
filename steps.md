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
    - Test fonctionnel
    - Faire en sorte que le nouveau tricount  apparaîsse dans la page.
    -Ajouter un lien vers un choix de devise qui mène à une autre page html.
    - Test fonctionnel
    - Modifier pour que les infos rentrent dans une bdd et que ces infos soient affichées.
    - Test fonctionnel marche toujours?
    - Modifier la page remplissage pour qu'on puisse y intégrer des participants.



# Bugs intéressants 
    - TIME SEND KEYS : Après send_Keys, il faut laisser du temps pour que la page se charge.
    - URL : Faire bien attention à respecter le fait qu'il y ait ou non / dans les adresses (faire pareil que dans le path : si j'ai mis count/ dans le path il faut le mettre après dans les redirections) sinon on aura une réponse inappropriée ( 404 ou autre).
    - FAUX BUG de redirect : quand on utilise la fonction post du client et que cela mène à une redirection, la réponse n'a pas de contenu c'est juste une redirection même si on redirige vers une autre fonction de view qui elle a un contenu.



# Mes difficultés principales
    - Non connaissance des syntaxes du client django pour faire des tests unitaires. Idem pour les fonctionnels.