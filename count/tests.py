from django.test import TestCase
from django.urls import resolve
from count.views import listecount
from bs4 import BeautifulSoup

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

    def test_newcount(self):
        """
        Fonction qui à partir de la page de la liste des tricount clique sur "créer un nouveau tricount" et vérifie qu'on utilise le bon template
        """
        response = self.client.get('/count/')
        soup = BeautifulSoup(response.content,'html.parser')
        link = soup.select_one('a#id_newcount')['href'] 
        response2 = self.client.get(link)

        self.assertTemplateUsed(response2, 'newcount.html')
        #self.assertRedirects(response2, '/count/newcount/') 
    
