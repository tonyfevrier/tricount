#from django.test import LiveServerTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class NewVisitorTest(StaticLiveServerTestCase): 

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()
        
    def check_inputs_appear_on_listecount_Page(self,inputs):
        """
        Fonction qui entre un nouveau tricount et vérifie si les données apparaissent sur la page recensant les tricount.
        """

        #Il remplit les données d'un nouveau tricount et les envoie
        
        titlebox = self.browser.find_element(By.NAME,"newtricount_title")
        descriptionbox = self.browser.find_element(By.NAME,"newtricount_description")
        categorybox = self.browser.find_element(By.NAME,"newtricount_category")
        submitbox = self.browser.find_element(By.NAME,"submit")
        
        titlebox.send_keys(inputs[0])
        descriptionbox.send_keys(inputs[1])
        categorybox.send_keys(inputs[2])
        
        submitbox.send_keys(Keys.ENTER)
        
        
        time.sleep(3)
        
        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/')   
        self.assertIn('Tricount',self.browser.title)

        
        #Il est alors renvoyé vers la page recensant la liste des tricount : son tricount est apparu.
        title = self.browser.find_elements(By.CLASS_NAME,'tricount_title')
        description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')
        self.assertIn(inputs[0],[titre.text for titre in title]) 
        self.assertIn(inputs[1],[desc.text for desc in description])
        
    
    def test_listecount_Page(self):
        
        #Le visiteur arrive sur la page il voit le titre. 
        url = self.live_server_url  
        self.browser.get(url + '/count')  
        
        time.sleep(2) 
        self.assertIn('Tricount',self.browser.title)
        
        #Il voit la liste des tricount présents ou absents et clique sur le lien pour créer un nouveau tricount
        link = self.browser.find_element(By.ID,'id_newcount') 
        link.send_keys(Keys.ENTER)
        time.sleep(2)  

        self.assertEqual(self.browser.current_url, url + '/count/newcount') 
    
        #Il remplit les données d'un nouveau tricount et les envoie et voit ses données apparaître sur la page recensant la liste des tricount.
        self.check_inputs_appear_on_listecount_Page(['tricount 1','description 1','Voyage'])
       
        #Il reclique pour recréer un second tricount.
        link = self.browser.find_element(By.ID,'id_newcount') 
        link.send_keys(Keys.ENTER)
        time.sleep(2)  
        
        self.assertEqual(self.browser.current_url, url + '/count/newcount') 
        
        #Il remplit les données d'un nouveau tricount et les envoie et voit ses données apparaître sur la page recensant la liste des tricount.
        self.check_inputs_appear_on_listecount_Page(['tricount 2','description 2','Projet'])
    

        