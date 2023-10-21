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
    
    def money_transfer(self,payer, forwho):
        """
        Function which transfer money from the owner to the receiver
        """ 
    
        for spender in payer.keys():
            for receiver in forwho.keys():
                if receiver != spender: 
                    self.dict_participants[spender].credits[receiver] -= forwho[receiver]
                    self.dict_participants[receiver].credits[spender] += forwho[receiver]

        return self 
    
    def calculate_total_credit(self):
        """
        Function which calculates for each participant the total credit/debt

        Output : dict {name:total credit}. total credit can be negative.
        """

        total_credit = {}
        
        for payer in self.dict_participants.keys():
            total_credit[payer] = 0
            for receiver in self.dict_participants[payer].credits.keys():
                total_credit[payer] -= self.dict_participants[payer].credits[receiver]

        return total_credit
    

    def reimburse_one_creditor(self,creditor, debitors,transferts_to_equilibrium):
        """
        Function which offers a repartition to reimburse ONE debitor. It completes transferts_to_equilibrium.

        Input : tuple creditor := (name,amount)
                dict debitors : the debitors as keys and the amount to credit as values
                dict transferts_to_equilibrium :  dict {name debitor : {name1 creditor : amount, name2:amount,...}}. Dictionary whose values are dictionaries.
        
        Output : dict transferts_to_equilibrium completed.
        """

        #We create a dictionary for the creditor whose values give people who have to reimbuse him plus the amount.
        transferts_to_equilibrium[creditor[0]] = {}
        amount_reimbursed = 0

        for debitor in debitors.keys():
            #soit on n'a pas encore complètement remboursé le débiteur
            if amount_reimbursed + debitors[debitor] <= creditor[1]:
                transferts_to_equilibrium[creditor[0]][debitor] = debitors[debitor]
                amount_reimbursed += debitors[debitor]
                debitors[debitor] = 0
            else:
                transferts_to_equilibrium[creditor[0]][debitor] = creditor[1] - amount_reimbursed 
                debitors[debitor] -= creditor[1] - amount_reimbursed 
                break
        
        return transferts_to_equilibrium

    def resolve_solution(self,total_credit):
        """
        Function which propose a solution of payment to get perfect equilibrium.

        Input : dict {name:total credit}
        Output transferts_to_equilibrium : dict {name debitor : {name1 creditor : amount, name2:amount,...}}. Dictionary whose values are dictionaries. It gives the solution to reach the equilibrium.

        The principle: a debitor receives money from creditors while he is not reimbursed completely. 
        A dictionnary transferts_to_equilibrium is fulled with the name of the debitor and the names of the creditor with the amount they must give to him. 
        After, the algorithm continues on the second most important debitor and so on.  
        """
        transferts_to_equilibrium = {}

        #creation of two dictionnaries for creditors and debitors :
        creditors = {}
        debitors = {}
        for key, value in total_credit.items():
            if value > 0:
                debitors[key] = value
            elif value < 0 :
                creditors[key] = -value

        for creditor in creditors.items():
            transferts_to_equilibrium = self.reimburse_one_creditor(creditor,debitors,transferts_to_equilibrium) 

        return transferts_to_equilibrium

    def update_process(self, payer, forwho, transfert = 'spend'):
        """
        Function which combines the previous functions to update after a spending : to get a solution for getting the equilibrium.
        """
        if transfert == 'spend':
            self.spending_update(payer,forwho)
        elif transfert == 'receive':
            self.receiving_update(payer,forwho)
        else:
            self.money_transfer(payer,forwho)

        total_credit = self.calculate_total_credit()
        transfert_to_equilibrium = self.resolve_solution(total_credit)
        
        return total_credit,transfert_to_equilibrium 

    