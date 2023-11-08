from django.test import TestCase
from django.urls import resolve
from count.views import listecount 
from count.models import Counts, Spending
from count.calculation import Tricount 
from copy import deepcopy
from count.tests_functions import UnitaryTestMethods
from datetime import date
import json

# Create your tests here.

class resolveUrl(TestCase):
    
    def test_resolve(self):
        """
        On crée d'abord l'url de la page en question et on vérifie que l'url est associée à la bonne fonction de views.
        """
        found = resolve('/count/')

        self.assertEqual(found.func,listecount) 

class HomepageTest(TestCase):
    def test_title(self):
        response = self.client.get('/count/') 

        self.assertIn(b'Tricount',response.content)
        self.assertTemplateUsed(response,'index.html')

class NewcountTest(UnitaryTestMethods):
    def test_newcount(self):
        """
        Fonction qui à partir de la page de la liste des tricount clique sur "créer un nouveau tricount" et vérifie qu'on utilise le bon template
        """ 
        response = self.client.get('/count/')
        link = self.extract_and_click_on_link(response.content , 'id_newcount')
        response2 = self.client.get(link)

        self.assertTemplateUsed(response2, 'newcount.html') 

    def test_newcount_inputs(self):
        """
        Fonction qui teste si les données entrées par l'utilisateur sont bien récupérées et si la redirection vers la page d'origine est effective.
        """
        response = self.create_a_tricount("tricount 1","description 1","Voyage",'Jean','Henri')
        count = Counts.objects.first()

        self.assertEqual("Tricount 1",count.title)
        self.assertEqual("Description 1", count.description)
        self.assertEqual("Voyage", count.category)
        self.assertRedirects(response, '/count/tricount/1')  

    def test_lack_title_newcountinputs(self):
        """
        Fonction qui regarde si lorsqu'on tente de créer un tricount sans titre, il n'y a pas de nouvel objet dans la bdd
        et on a dans la réponse html un message en rouge indiquant que le titre et la catégorie doivent être remplis.
        """    
        one = Counts.objects.count()
        response = self.create_a_tricount("","description 1","Voyage",'Jean') 
        two = Counts.objects.count() 

        self.assertEqual(one,two)
        self.assertTemplateUsed(response,"newcount.html")
        self.assertContains(response,"Le titre doit comporter au moins un caractère.")

    def test_lack_participant_newcountinputs(self):
        """
        Fonction qui regarde si lorsqu'on tente de créer un tricount sans participant, il n'y a pas de nouvel objet dans la bdd
        et on a dans la réponse html un message en rouge indiquant qu'il faut un participant.
        """    
        one = Counts.objects.count()
        response = self.create_a_tricount("Tricount sans participant", "description 1", "Voyage")
        two = Counts.objects.count() 

        self.assertEqual(one,two)
        self.assertTemplateUsed(response,"newcount.html")
        self.assertContains(response,"Il faut au moins un participant")


    def test_bdd_when_tricounts_created(self):
        """
        Fonction qui teste, si lorsqu'on ajoute un participant, la bdd des participants est bien incrémentée.
        Elle teste ensuite lorsqu'on poste un titre, une description, une catégorie, que les participants sont bien associés au tricount.
        Enfin elle crée un second tricount et vérifie que la bdd associe bien le bon nombre de participants au tricount et qu'elle n'associe par des noms du premier tricount au second.
        """  
        self.create_a_tricount("tricount 1","description 1","Voyage","Jean","Henri")

        count = Counts.objects.first() 

        self.assertEqual('Jean', count.participants[0])
        self.assertEqual('Henri',count.participants[1]) 
        self.assertEqual(2,len(count.participants))
        self.assertIsNotNone(count.data)

        #Verification of the object Tricount after deserialization.
        data = json.loads(count.data) 

        self.assertListEqual(data['participants'], ['Jean', 'Henri'])
        self.assertEqual(data['total_cost'],0)  
        self.assertDictEqual(data['dict_participants']["Jean"], {'owner' : 'Jean', 'expense': 0, 'credits':{'Henri':0}, 'receivers' : ['Henri']})
        self.assertDictEqual(data['dict_participants']["Henri"], {'owner' : 'Henri', 'expense': 0, 'credits':{'Jean':0}, 'receivers' : ['Jean']})
                                          
        self.create_a_tricount("tricount 2","description 2","Voyage","Henri","Henriette","Tony")
        count2 = Counts.objects.get(pk=2) 
        self.assertEqual(3,len(count2.participants))

        self.assertNotIn('Jean', count2.participants)

    def test_click_on_count(self):
        """
        Function checking if we go on the good link after clicking on a tricount.
        """ 
        #We create two tricounts
        self.create_a_tricount("tricount 1", "description 1", "Voyage", "Henri", "Jean")
        self.create_a_tricount("tricount 2", "description 2", "Coloc", "Roberto",'Alfredo')
        
        #We go on the list of the tricounts
        response = self.client.get('/count/')
        link = self.extract_and_click_on_link(response.content , 'link-tricount-2') 

        self.assertEqual(link,'/count/tricount/2')

        link = self.extract_and_click_on_link(response.content , 'link-tricount-1')  

        self.assertEqual(link,'/count/tricount/1')

        response = self.client.get(link)

        self.assertIn(b'Henri',response.content)

class TestCalculator(TestCase):

    def test_class_creation(self):
        """
        Testing if data are well created.
        """
        participants = ['Tony', 'Marine', 'Henri', 'Yann']
        count = Tricount(*participants)
        
        self.assertEqual(len(count.dict_participants.keys()),4)  
        self.assertEqual(count.dict_participants['Tony'].credits,{'Marine':0, 'Henri':0, 'Yann':0})

    def test_nullity(self):
        """
        Function which test a spending of amount 0. Nothing changes
        """
        
        participants = ['Tony', 'Marine', 'Henri', 'Yann']
        count = Tricount(*participants)
        old_dict_participants = count.dict_participants
        count.spending_update({'Tony':0.}, {'Marine':0., 'Tony':0.})

        self.assertEqual(old_dict_participants,count.dict_participants) 
         
    def test_spending_update_first(self):
        """
        We test a spending between two participants from a group of four to verify that the amount is correct and
        that the others credits are not modified.
        """
        count = Tricount('Tony', 'Marine', 'Henri', 'Yann')
        old_dict_participants = deepcopy(count.dict_participants)   
        count.spending_update({'Tony':100.}, {'Marine':50., 'Tony':50}) 

        #Change for Tony expense and for Tony and Marine credits but no changes for others.
        self.assertEqual(old_dict_participants['Tony'].expense + 100,count.dict_participants['Tony'].expense)
        self.assertEqual(old_dict_participants['Tony'].credits['Marine'] - 50, count.dict_participants['Tony'].credits['Marine'])
        self.assertEqual(old_dict_participants['Marine'].credits['Tony'] + 50, count.dict_participants['Marine'].credits['Tony'])
        self.assertDictEqual(old_dict_participants['Yann'].credits, count.dict_participants['Yann'].credits)
        self.assertDictEqual(old_dict_participants['Henri'].credits, count.dict_participants['Henri'].credits)

    def test_spending_update_second(self):
        """
        We test a spending between all participants from a group of four to verify that the amount is correct.
        """
        count = Tricount('Tony', 'Marine', 'Henri', 'Yann')
        old_total_cost = count.total_cost
        old_dict_participants = deepcopy(count.dict_participants)  
        count.spending_update({'Tony':100.}, {'Marine':25., 'Yann':50, 'Henri':25})

        self.assertEqual(old_total_cost + 100,count.total_cost)
        self.assertEqual(old_dict_participants['Tony'].expense + 100,count.dict_participants['Tony'].expense)
        self.assertEqual(old_dict_participants['Tony'].credits['Marine'] - 25, count.dict_participants['Tony'].credits['Marine'])
        self.assertEqual(old_dict_participants['Marine'].credits['Tony'] + 25, count.dict_participants['Marine'].credits['Tony'])
        self.assertEqual(old_dict_participants['Tony'].credits['Yann'] - 50, count.dict_participants['Tony'].credits['Yann'])
        self.assertEqual(old_dict_participants['Yann'].credits['Tony'] + 50, count.dict_participants['Yann'].credits['Tony'])
        self.assertEqual(old_dict_participants['Tony'].credits['Henri'] - 25, count.dict_participants['Tony'].credits['Henri'])
        self.assertEqual(old_dict_participants['Henri'].credits['Tony'] + 25, count.dict_participants['Henri'].credits['Tony'])
        
        for firstparticipant in ['Marine', 'Henri', 'Yann']: 
            self.assertEqual(old_dict_participants[firstparticipant].expense,count.dict_participants[firstparticipant].expense)
            for secondparticipant in ['Marine', 'Henri', 'Yann']:
                if secondparticipant != firstparticipant:
                    self.assertEqual(old_dict_participants[firstparticipant].credits[secondparticipant], count.dict_participants[firstparticipant].credits[secondparticipant])
                    self.assertEqual(old_dict_participants[secondparticipant].credits[firstparticipant], count.dict_participants[secondparticipant].credits[firstparticipant])
                
    def test_receiving_update(self):
        """
        We test a money input between all participants from a group of four to verify that the amount is correct.
        """
        count = Tricount('Tony', 'Marine', 'Henri', 'Yann')
        old_dict_participants = deepcopy(count.dict_participants)  
        count.receiving_update({'Tony':100.}, {'Marine':25., 'Yann':50, 'Henri':25})

        self.assertEqual(old_dict_participants['Tony'].expense - 100,count.dict_participants['Tony'].expense)
        self.assertEqual(old_dict_participants['Tony'].credits['Marine'] + 25, count.dict_participants['Tony'].credits['Marine'])
        self.assertEqual(old_dict_participants['Marine'].credits['Tony'] - 25, count.dict_participants['Marine'].credits['Tony'])
        self.assertEqual(old_dict_participants['Tony'].credits['Yann'] + 50, count.dict_participants['Tony'].credits['Yann'])
        self.assertEqual(old_dict_participants['Yann'].credits['Tony'] - 50, count.dict_participants['Yann'].credits['Tony'])
        self.assertEqual(old_dict_participants['Tony'].credits['Henri'] + 25, count.dict_participants['Tony'].credits['Henri'])
        self.assertEqual(old_dict_participants['Henri'].credits['Tony'] - 25, count.dict_participants['Henri'].credits['Tony'])
        
        for firstparticipant in ['Marine', 'Henri', 'Yann']: 
            self.assertEqual(old_dict_participants[firstparticipant].expense,count.dict_participants[firstparticipant].expense)
            for secondparticipant in ['Marine', 'Henri', 'Yann']:
                if secondparticipant != firstparticipant:
                    self.assertEqual(old_dict_participants[firstparticipant].credits[secondparticipant], count.dict_participants[firstparticipant].credits[secondparticipant])
                    self.assertEqual(old_dict_participants[secondparticipant].credits[firstparticipant], count.dict_participants[secondparticipant].credits[firstparticipant])
       
    def test_calculate_total_credit(self):
        """
        Function which tests if the total credit of each participant is correct.
        """
        count = Tricount('Tony', 'Marine', 'Henri', 'Yann') 
        count.spending_update({'Tony':100.}, {'Marine':25., 'Yann':50, 'Henri':25})
        count.spending_update({'Marine':200.}, {'Marine':150., 'Tony':50})
        count.spending_update({'Henri':150.}, {'Marine':25., 'Yann':50, 'Tony':25,'Henri':50})
        
        total_credit = count.calculate_total_credit()

        self.assertEqual(total_credit['Tony'], 25)
        self.assertEqual(total_credit['Marine'], 0)
        self.assertEqual(total_credit['Yann'],-100)
        self.assertEqual(total_credit['Henri'],75)

    def test_resolve_solution(self):
        count = Tricount('Tony', 'Marine', 'Henri', 'Yann') 
        count.spending_update({'Tony':100.}, {'Marine':25., 'Yann':50, 'Henri':25})
        count.spending_update({'Marine':200.}, {'Marine':150., 'Tony':50})
        count.spending_update({'Henri':150.}, {'Marine':25., 'Yann':50, 'Tony':25,'Henri':50})
        count.spending_update({'Yann':180.}, {'Marine':50., 'Yann':50, 'Tony':50,'Henri':30})
        
        total_credit = count.calculate_total_credit()
        transfert_to_equilibrium = count.resolve_solution(total_credit)

        self.assertEqual(sum(transfert_to_equilibrium['Tony'].values()),25)
        self.assertEqual(sum(transfert_to_equilibrium['Marine'].values()),50)

    def test_moneytransfer(self):
        count = Tricount('Tony', 'Marine', 'Henri', 'Yann')
        old_total_cost = count.total_cost
        old_dict_participants = deepcopy(count.dict_participants)   
        count.money_transfer({'Tony':100.}, {'Marine':100.}) 

        #Change for Tony expense and for Tony and Marine credits but no changes for others.
        self.assertEqual(old_total_cost,count.total_cost)
        self.assertEqual(old_dict_participants['Tony'].expense,count.dict_participants['Tony'].expense)
        self.assertEqual(old_dict_participants['Tony'].credits['Marine'] - 100, count.dict_participants['Tony'].credits['Marine'])
        self.assertEqual(old_dict_participants['Marine'].credits['Tony'] + 100, count.dict_participants['Marine'].credits['Tony'])
        self.assertDictEqual(old_dict_participants['Yann'].credits, count.dict_participants['Yann'].credits)
        self.assertDictEqual(old_dict_participants['Henri'].credits, count.dict_participants['Henri'].credits)

class TestSpending(UnitaryTestMethods):

    def test_redirect_after_newspending_inputs(self):
        """
        We enter a newspending and we see if data are integrated into the database.
        """
        self.create_a_tricount('tricount1', 'description', "Voyage", "Henri", "Jean")
        response = self.create_a_spending('dépense1', 100, 'Jean', ['Henri','Jean'], [50,50])  

        self.assertRedirects(response,'/count/tricount/1') 
    
    def test_bdd_newspending_inputs(self):
        self.create_a_tricount('tricount1', 'description', "Voyage", "Henri", "Jean")

        number = Spending.objects.count()
        self.create_a_spending('dépense1', 100, 'Jean', ['Henri','Jean'], [50,50])  
        spending = Spending.objects.get(pk = 1)
        
        self.assertEqual(number+1, Spending.objects.count())
        self.assertEqual(spending.title, 'dépense1')
        self.assertEqual(spending.amount, 100)
        self.assertEqual(spending.payer, 'Jean')
        self.assertDictEqual(spending.receivers, {'Henri':50,'Jean':50})
        self.assertEqual(spending.number, 1)
        self.assertEqual(spending.date, date.today())
    
    def test_goback_bdd_unchanged(self):
        """
        test : we begin to create a spending and go back. No new spend must appear in the bdd.
        """
        self.create_a_tricount('tricount1', 'description', "Voyage", "Henri", "Yann")
        response = self.client.get('/count/tricount/1/spending') 
        nb_spending = Spending.objects.count()
        self.extract_and_click_on_link(response.content , 'backtospending')  

        self.assertEqual(nb_spending,Spending.objects.count()) 

    def test_notitle_bdd_unchanged(self):
        """
        test : we create a spending, we forget the title. No new spend must appear in the bdd and we stay on the same template.
        """
        self.create_a_tricount('tricount1', 'description', "Voyage", "Henri", "Jean")     
        nb_spending = Spending.objects.count()
        response = self.create_a_spending('', 100, 'Jean', ['Henri','Jean'],[50,50])   
        
        self.assertEqual(nb_spending,Spending.objects.count()) 
        self.assertTemplateUsed(response,'newspending.html')
        
    def test_noamount_nullspending(self):
        """
        test : we create a spending with no amount. A new spend must appear in the bdd with amount 0 and we must be redirected.
        """
        self.create_a_tricount('tricount1', 'description', "Voyage", "Henri", "Jean")
        nb_spending = Spending.objects.count()
        self.create_a_spending('dépense1', '', 'Jean', ['Henri','Jean'],[0,0])  
        spending = Spending.objects.get(pk = 1)

        self.assertEqual(nb_spending + 1,Spending.objects.count()) 
        self.assertEqual(spending.amount, 0)
 
    def test_multiple_spendings_gives_good_credits_in_bdd(self):
        self.create_a_tricount('tricount1', 'description', "Voyage", "Henri", "Yann", "Marine", "Tony")
        self.create_a_spending('dépense1', 100, 'Tony', ['Henri','Yann','Marine','Tony'], [25,50,25,0]) 
        self.create_a_spending('dépense2', 200, 'Marine', ['Henri','Yann','Marine','Tony'], [0,0,150,50]) 
        self.create_a_spending('dépense3', 150, 'Henri', ['Henri','Yann','Marine','Tony'], [50,50,25,25]) 
        self.create_a_spending('dépense4', 180, 'Yann', ['Henri','Yann','Marine','Tony'], [30,50,50,50]) 

        #Deserialization of the bdd 
        data = Counts.objects.first().data
        count = Tricount.from_json(data)
 
        self.assertEqual(count.dict_participants["Tony"].expense, 100)
        self.assertEqual(count.dict_participants["Marine"].expense, 200)
        self.assertEqual(count.dict_participants["Henri"].expense, 150)
        self.assertEqual(count.dict_participants["Yann"].expense, 180)
        
        self.assertDictEqual(count.dict_participants["Tony"].credits, {'Marine': 25.0, 'Henri': 0, 'Yann': 0})
        self.assertEqual(count.dict_participants["Marine"].credits, {'Tony': -25.0, 'Henri': 25.0, 'Yann': 50.0})
        self.assertEqual(count.dict_participants["Henri"].credits, {'Tony': 0, 'Marine': -25.0, 'Yann': -20})
        self.assertEqual(count.dict_participants["Yann"].credits, {'Tony': 0, 'Marine': -50.0, 'Henri': 20})
       
 
    