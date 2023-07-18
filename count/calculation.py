import numpy 
 

class Participant():
    def __init__(self,owner,receivers) -> None:
        """
        Participant owner : the first element of the list.
        expense : what he has to pay
        credits : dictionnary containing debts or credits towards other participants : what they have to spend for each participant (key)
        """
        self.name = owner
        self.expense = 0
        self.credits = {}

        for participant in receivers:
            self.credits[participant] = 0


class Tricount():
    def __init__(self,*participants) -> None:
        """
        Function creating the participants to the tricount as instanciations of the class Participant.

        dict_participants : dict (keys : name of the participant, values : the object associated to the name).
        """

        self.number = len(participants)

        self.dict_participants = {}
        self.dict_participants[participants[0]] = Participant(participants[0],participants[1:])
        self.dict_participants[participants[self.number-1]] = Participant(participants[self.number-1],participants[0:self.number])
        for i in range(1,len(participants)-1):
            owner = participants[i]
            receivers = participants[0:i]+participants[i+1:]
            self.dict_participants[owner] = Participant(owner,receivers)

        self.total_cost = 0

    def spending_update(self, payer, forwho):
        """
        Function updating after a spending the two dictionnaries.
        
        payer : dictionary {participant:str: amount:float}
        forwho : dictionary of participants involved in the shared spending and the positive amount which was paid for them.
        """

        #The payer expense and credits change.
        for spender in payer.keys():
            self.total_cost += payer[spender]
            self.dict_participants[spender].expense += payer[spender]

            for receiver in forwho.keys():
                if receiver != spender:
                    self.dict_participants[spender].credits[receiver] -= forwho[receiver]
                    self.dict_participants[receiver].credits[spender] += forwho[receiver]

        return self 
    
    def receiving_update(self,payer,forwho):
        """
        Function updating after an arrival of money the two dictionnaries. It's like a negative spending.
        
        receiver : dictionary {participant:str: amount:float}
        forwho : dictionary of participants involved in the shared spending and the positive amount which was paid for them.
        """
 
        for spender in payer:
            payer[spender] = - payer[spender]
        
        for receiver in forwho:
            forwho[receiver] = - forwho[receiver] 

        return self.spending_update(payer,forwho)
    
    def calculate_total_credit(self):
        """
        Function which calculates for each participant the total credit/debt
        """
        total_credit = {}
        
        for payer in self.dict_participants.keys():
            total_credit[payer] = 0
            for receiver in self.dict_participants[payer].credits.keys():
                total_credit[payer] += self.dict_participants[payer].credits[receiver]

        return total_credit
    
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