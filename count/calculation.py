import numpy 

class tricount():
    def __init__(self,*participants) -> None:
        """
        Function recovering the participants name and creating a dictionnary with the expense of each participant
        (his total amount to spend) and an other associating each participant with a number.

        participants : sequence of str giving the name of participants to the count.
        self.correspondance : dict associating participant with number
        self.participants_expense : dict  (key : number of the participant, value : expense of the participant).

        """
        self.correspondance = {}
        self.participants_expense = {}
        number = 1
        for participant in participants:
            self.correspondance[participant] = number
            self.participants_expense[number] = 0
            number += 1

        self.total_cost = 0
        self.participants_number = len(participants)
        self.credits = numpy.zeros((self.participants_number,self.participants_number))
         
    #def spending_shared_repartition(self, payer, forwho):
    #    """
    #    Function taking a payer and an amount of spending and creating a dictionary whose keys are the participants
    #    and the values are the amount to add to their personal expense on an equal manner.
    #    
    #    payer : list [participant:str, amount:float]
    #    forwho : list of participants involved in the shared spending.
    #    """
    #    pass



    def spending_update(self, payer, forwho):
        """
        Function updating after a spending the two dictionnaries.
        
        payer : dictionary {participant:str: amount:float}
        forwho : dictionary of participants involved in the shared spending and their amount .
        """
        pass

    def credit_update(self):
        """
        Function which calculates the difference to equilibrium for each participant.
        """
        pass
    
    def resolve_solution(self):
        """
        Function which propose a solution of payment to get perfect equilibrium.
        """
        pass

    def update_process(self):
        """
        Function which combines the previous functions to update after a spending.
        """
        pass

    def money_transfer(self):
        """
        Function which transfer money 
        """
        pass