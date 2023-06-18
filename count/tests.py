from django.test import TestCase
from django.urls import resolve
from count.views import listecount
from bs4 import BeautifulSoup
from count.models import Counts

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
        response = self.client.post("/count/newcount/addcount",data = {"newtricount_title":"tricount 1", "newtricount_description":"description 1", "newtricount_category":"Voyage"})
        count = Counts.objects.first()

        self.assertEqual("Tricount 1",count.title)
        self.assertEqual("Description 1", count.description)
        self.assertEqual("Voyage", count.category)
        self.assertRedirects(response, '/count/')  

    def test_lack_title_newcountinputs(self):
        """
        Fonction qui regarde si lorsqu'on tente de créer un tricount sans titre ou sans catégorie, il n'y a pas de nouvel objet dans la bdd
        et on a dans la réponse html un message en rouge indiquant que le titre et la catégorie doivent être remplis.
        """    
        one = Counts.objects.count()
        response = self.client.post("/count/newcount/addcount",data = {"newtricount_title":"", "newtricount_description":"description 1", "newtricount_category":"Voyage"})
        two = Counts.objects.count() 

        self.assertEqual(one,two)
        self.assertTemplateUsed(response,"newcount.html")
        self.assertContains(response,"Le titre doit comporter au moins un caractère.")

    
        