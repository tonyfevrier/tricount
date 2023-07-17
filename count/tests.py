from django.test import TestCase
from django.urls import resolve
from count.views import listecount
from bs4 import BeautifulSoup
from count.models import Counts, Participants
from count.calculation import tricount

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
        count = tricount(*participants)
        
        self.assertEqual(count.credits.shape,(4,4))
        self.assertEqual(len(count.participants_expense.keys()),4)
        self.assertEqual(len(count.correspondance.keys()),4)

    def test_nullity(self):
        """
        Function which test a spending of amount 0. Nothing changes
        """
        participants = ['Tony', 'Marine', 'Henri', 'Yann']
        count = tricount(*participants)
        old_expense = count.participants_expense 
        count.spending_update({'Tony':0.}, {'Marine':0., 'Tony':0.})
        
        self.assertEqual(old_expense,count.participants_expense)
        self.assertEqual(old_spent, count.participants_spent)
        
        #for participant in participants:
        #    self.assertEqual(old_expense[participant],count.participants_expense[participant])
        #    self.assertEqual(old_spent[participant],count.participants_spent[participant])


    def test_two_participants(self):
        """
        We test a spending between two participants from a group of four to verify that the amount is correct and
        that the others credits are not modified.
        """
        count = tricount('Tony', 'Marine', 'Henri', 'Yann')
        old_expense = count.participants_expense
        old_spent = count.participants_spent
        count.spending_update({'Tony':100.}, {'Marine':50., 'Tony':50})
        
        for participant in ['Yann', 'Henri']:
            self.assertEqual(old_expense[participant],count.participants_expense[participant])
            self.assertEqual(old_spent[participant],count.participants_spent[participant])

        self.assertEqual(count.participants_spent['Tony'], old_spent['Tony'] + 100.)
        self.assertEqual(count.participants_expense['Tony'], old_expense['Tony'] + 50.)


    def test_participants(self):
        """
        We test a spending between all participants from a group of four to verify that the amount is correct.
        """
        pass

    
    def test_moneytransfer(self):
        pass


    