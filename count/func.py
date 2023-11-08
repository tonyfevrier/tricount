from count.models import Counts
from count.calculation import Tricount

def majuscule(chaine):
    """
    Function which puts the first letter in majuscule
    """
    return chaine[0].upper() + chaine[1:]

def update_tricount_after_new_spending(id_count, spender, dico_receivers):
    """
    Fonction qui permet de modifier les crédits de chacun dans le tricount après une dépense puis d'enregistrer dans la bdd

    Inputs : 
        id_count (int) : number of tricount
        spender (dict) : {payer (str): amount(float)}
        dico_receivers (dict) : keys are participants and values are the amount they have to reimburse to the payer.  
    """

    count = Counts.objects.get(id = id_count)
    tricount = Tricount.from_json(count.data)
    tricount.spending_update(spender, dico_receivers)
    count.data = tricount.to_json()
    count.save()


    