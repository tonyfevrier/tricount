from django.test import TestCase
from django.urls import resolve
from count.views import listecount
from bs4 import BeautifulSoup
from count.models import Counts, Participants, Spending
from count.calculation import Tricount
import numpy
from copy import deepcopy

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

class NewcountTest(TestCase):
    def test_newcount(self):
        """
        Fonction qui à partir de la page de la liste des tricount clique sur "créer un nouveau tricount" et vérifie qu'on utilise le bon template
        """ 
        response = self.client.get('/count/')
        soup = BeautifulSoup(response.content,'html.parser')
        link = soup.select_one('a#id_newcount')['href'] #on clique sur le + : sorte de send_keys
        response2 = self.client.get(link)

        self.assertTemplateUsed(response2, 'newcount.html') 

    def test_newcount_inputs(self):
        """
        Fonction qui teste si les données entrées par l'utilisateur sont bien récupérées et si la redirection vers la page d'origine est effective.
        """

        self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Jean"})
        response = self.client.post("/count/newcount/addcount",data = {"newtricount_title":"tricount 1", "newtricount_description":"description 1", "newtricount_category":"Voyage"})
        
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
        self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Jean"})
        response = self.client.post("/count/newcount/addcount",data = {"newtricount_title":"", "newtricount_description":"description 1", "newtricount_category":"Voyage"})
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
        response = self.client.post("/count/newcount/addcount",data = {"newtricount_title":"Tricount sans participant", "newtricount_description":"description 1", "newtricount_category":"Voyage"})
        two = Counts.objects.count() 

        self.assertEqual(one,two)
        self.assertTemplateUsed(response,"newcount.html")
        self.assertContains(response,"Il faut au moins un participant")

    def test_redirection_when_add_participants(self):
        """
        Fonction qui teste, si lorsqu'on ajoute un participant, on est bien redirigé vers la page newcount.
        """
        response = self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Jean"})
        self.assertRedirects(response,'/count/newcount')

    def test_bdd_when_add_participants(self):
        """
        Fonction qui teste, si lorsqu'on ajoute un participant, la bdd des participants est bien incrémentée.
        Elle teste ensuite lorsqu'on poste un titre, une description, une catégorie, que les participants sont bien associés au tricount.
        Enfin elle crée un second tricount et vérifie que la bdd associe bien le bon nombre de participants au tricount et qu'elle n'associe par des noms du premier tricount au second.
        """
        self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Jean"})
        participant = Participants.objects.first()

        self.assertEqual(participant.name,'Jean') 

        self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Henri"})

        self.client.post("/count/newcount/addcount",data = {"newtricount_title":"tricount1", "newtricount_description":"description 1", "newtricount_category":"Voyage"})
        count = Counts.objects.first() 

        self.assertIn('Jean', count.participants.first().name)
        self.assertIn('Henri',count.participants.get(pk=2).name)
        self.assertEqual(1,count.participants.first().number)
        self.assertEqual(2,count.participants.count())

        self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Henri"})
        self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Henriette"})
        self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Tony"})

        self.client.post("/count/newcount/addcount",data = {"newtricount_title":"tricount2", "newtricount_description":"description 2", "newtricount_category":"Voyage"})
        count2 = Counts.objects.get(pk=2) 
        self.assertEqual(3,count2.participants.count())

        self.assertNotIn('Jean', [count2.participants.get(pk=i+3).name for i in range(count2.participants.count())])

    def test_back_to_listecount_page(self):
        """
        Fonction qui lance la création d'un tricount, ne valide pas le tricount et revient en arrière.
        Vérifie si les participants créés dans la bdd sont bien supprimés.
        """
        number = Participants.objects.count()
        self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Henri"})
        self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Jean"})
        response = self.client.get('/count/newcount') 

        soup = BeautifulSoup(response.content,'html.parser')
        link = soup.select_one('a#backtotricount')['href'] #on clique sur le + : sorte de send_keys 
        response2 = self.client.get(link)
        self.assertEqual(number,Participants.objects.count())

    def test_click_on_count(self):
        """
        Function checking if we go on the good link after clicking on a tricount.
        """ 
        #We create two tricounts
        self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Henri"})
        self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Jean"})
        self.client.post('/count/newcount/addcount',data = {"newtricount_title":"tricount 1", "newtricount_description":"description 1", "newtricount_category":"Voyage"})
       
        self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":"Roberto"})
        self.client.post('/count/newcount/addcount',data = {"newtricount_title":"tricount 2", "newtricount_description":"description 2", "newtricount_category":"Coloc"})
    
        #We go on the list of the tricounts
        response = self.client.get('/count/')

        soup = BeautifulSoup(response.content, 'html.parser')
        link = soup.select_one('a#link-tricount-2')['href'] 

        self.assertEqual(link,'/count/tricount/2')

        soup = BeautifulSoup(response.content, 'html.parser')
        link = soup.select_one('a#link-tricount-1')['href'] 

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
        count.receiving_update({'Tony':100.}, {'Marine':25., 'Yann':50, 'Henri':25})
        count.receiving_update({'Marine':200.}, {'Marine':150., 'Tony':50})
        count.receiving_update({'Henri':150.}, {'Marine':25., 'Yann':50, 'Tony':25,'Henri':50})
        
        total_credit = count.calculate_total_credit()

        self.assertEqual(total_credit['Tony'], 25)
        self.assertEqual(total_credit['Marine'], 0)
        self.assertEqual(total_credit['Yann'],-100)
        self.assertEqual(total_credit['Henri'],75)

    def test_resolve_solution(self):
        count = Tricount('Tony', 'Marine', 'Henri', 'Yann') 
        count.receiving_update({'Tony':100.}, {'Marine':25., 'Yann':50, 'Henri':25})
        count.receiving_update({'Marine':200.}, {'Marine':150., 'Tony':50})
        count.receiving_update({'Henri':150.}, {'Marine':25., 'Yann':50, 'Tony':25,'Henri':50})
        count.receiving_update({'Yann':180.}, {'Marine':50., 'Yann':50, 'Tony':50,'Henri':30})
        

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

class TestSpending(TestCase):

    def create_a_tricount(self,titre,description,category,*participants):
        
        for participant in participants:
            self.client.post("/count/newcount/addcount/addparticipant",data = {"new_participant":participant}) 
        
        self.client.post('/count/newcount/addcount',data = {"newtricount_title":titre, "newtricount_description":description, "newtricount_category":category})

    def test_redirect_after_newspending_inputs(self):
        """
        We enter a newspending and we see if data are integrated into the database.
        """
        self.create_a_tricount('tricount1', 'description', "Voyage", "Henri", "Yann")

        response = self.client.post('/count/tricount/1/addspending', data = {'title': 'dépense1', 'amount': 100, 'spender': 'Jean',  'receiver': ['Henri','Jean']})
        
        self.assertRedirects(response,'/count/tricount/1') 
    
    def test_bdd_newspending_inputs(self):
        self.create_a_tricount('tricount1', 'description', "Voyage", "Henri", "Yann")

        number = Spending.objects.count()
        self.client.post('/count/tricount/1/addspending', data = {'title': 'dépense1', 'amount': 100, 'spender': 'Jean',  'receiver': ['Henri','Jean']})
        
        self.assertEqual(number+1, Spending.objects.count())

        spending = Spending.objects.get(pk = 1)

        self.assertEqual(spending.title, 'dépense1')
        self.assertEqual(spending.amount, 100)
        self.assertEqual(spending.payer, 'Jean')
        self.assertListEqual(spending.receivers, ['Henri','Jean'])
        self.assertEqual(spending.number, 1)
    
    def test_goback_bdd_unchanged(self):
        """
        test : we begin to create a spending and go back. No new spend must appear in the bdd.
        """
        self.create_a_tricount('tricount1', 'description', "Voyage", "Henri", "Yann")
        response = self.client.get('/count/tricount/1/spending') 

        nb_spending = Spending.objects.count()
        soup = BeautifulSoup(response.content,'html.parser')
        soup.select_one('a#backtospending')['href']

        self.assertEqual(nb_spending,Spending.objects.count()) 

        

    def test_notitle_bdd_unchanged(self):
        """
        test : we create a spending, we forget the title. No new spend must appear in the bdd and we stay on the same template.
        """
        self.create_a_tricount('tricount1', 'description', "Voyage", "Henri", "Yann")
        
        nb_spending = Spending.objects.count()
        response = self.client.post('/count/tricount/1/addspending', data = {'title': '', 'amount': 100, 'spender': 'Jean',  'receiver': ['Henri','Jean']}) 
 
        self.assertEqual(nb_spending,Spending.objects.count()) 
        self.assertTemplateUsed(response,'newspending.html')
        

    def test_noamount_nullspending(self):
        """
        test : we create a spending with no amount. A new spend must appear in the bdd with amount 0 and we must be redirected.
        """
        self.create_a_tricount('tricount1', 'description', "Voyage", "Henri", "Yann")
        
        nb_spending = Spending.objects.count()
        self.client.post('/count/tricount/1/addspending', data = {'title': 'dépense1', 'amount': '', 'spender': 'Jean',  'receiver': ['Henri','Jean']}) 

        spending = Spending.objects.get(pk = 1)
        self.assertEqual(nb_spending + 1,Spending.objects.count()) 
        self.assertEqual(spending.amount, 0)
 
    