# Etapes élémentaires de construction

Je tente la méthodo suivante : test unitaire puis fonction associée puis compléter le test fonctionnel.

**Création d'une première page avec la liste des tricount sur laquelle on peut créer un tricount et cela incrémente la liste.**
    -`Ecrire mon test fonctionnel : l'utilisateur voit le titre, voit la liste des tricount disponibles.`
    -`Ouvrir une première page avec marqué tricount en titre.`
    - `Ajouter un bouton Créer un nouveau tricount qui envoie vers une autre page.`
    - `Débugger le test unitaire vérifiant qu'on passe sur la bonne url en cliquant (car ça marche bien)`
    - `Compléter le test fonctionnel et voir s'il passe. Débugger ce test`
    -Créer cette page remplissage qui contient en input Titre, Description, devise en liste déroulante, catégorie en liste déroulante.
    - Faire en sorte qu'une fois remplie on retourne à la page des tricount avec le tricount qui apparaît.
    - Test fonctionnel
    - Modifier pour que les infos rentrent dans une bdd et que ces infos soient affichées.
    - Test fonctionnel marche toujours?
    - Modifier la page remplissage pour qu'on puisse y intégrer des participants.



# Bugs intéressants 
    - TIME SEND KEYS : Après send_Keys, il faut laisser du temps pour que la page se charge.


# Mes difficultés principales
    - Non connaissance des syntaxes du client django pour faire des tests unitaires. Idem pour les fonctionnels.