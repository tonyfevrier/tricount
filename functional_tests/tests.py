#from django.test import LiveServerTestCase

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db import connections
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

from count.models import Counts
from functional_tests import user_experience 

class NewVisitorTest(StaticLiveServerTestCase): 
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self): 
        self.browser.quit()

    def test_tricount_creation_and_delation(self):
        #Le visiteur arrive sur la page, il se crée un compte et se logge et est redirigé vers la page de login
        url = self.live_server_url  
        click = user_experience.Click(self.browser, url)
        self.browser.get(url + "/welcome/")

        click.register_someone("Tony","tony.fevrier62@gmail.com", "password")
        self.assertEqual(self.browser.current_url, url + "/login/")

        #Il se connecte et atterrit sur la liste des tricounts
        click.login_someone("Tony", "password")
        self.assertEqual(self.browser.current_url, url + "/count/Tony")

        #Il va dans paramètres, constate que ses données sont bien présentes et se délogge directement
        click.click_on_a_link(By.CLASS_NAME,"parameters")
        click.click_on_a_link(By.CLASS_NAME,"myparameters")

        firstletter = self.browser.find_element(By.CLASS_NAME,"firstletter")
        name = self.browser.find_element(By.CLASS_NAME,"hello")
        mail = self.browser.find_element(By.CLASS_NAME,"mail")

        self.assertEqual(firstletter.text, "T")
        self.assertEqual(name.text, "Bonjour Tony")
        self.assertEqual(mail.text, "tony.fevrier62@gmail.com")

        logout = self.browser.find_element(By.CLASS_NAME, "logout")
        logout.send_keys(Keys.ENTER)
        time.sleep(2)

        self.assertEqual(self.browser.current_url, url + "/welcome/")

        #Il tente d'enregistrer un nouveau compte avec le même username puis avec le même mail mais est refusé
        click.register_someone("Tony", "tony@gmail.com","pwd")
        self.assertEqual(self.browser.current_url, url + "/welcome/")

        click.register_someone("Dulcinée", "tony.fevrier62@gmail.com","pwd")
        self.assertEqual(self.browser.current_url, url + "/welcome/") 
        #Il tente d'envoyer le formulaire sans username puis sans email et password, le formulaire n'est pas envoyé et des éléments apparaissent
        
        click.register_someone("", "tony.fevrier6@gmail.com","pwd")
        userlacking = self.browser.find_element(By.CLASS_NAME,"userlacking")

        self.assertEqual(userlacking.text, "A username is needed") 

        click.clear_registration_inputs(self.browser.find_element(By.NAME, "username"),self.browser.find_element(By.NAME, "email"),self.browser.find_element(By.NAME, "password"))
        
        click.register_someone("Dulcinée", "", "") 
        
        emaillacking = self.browser.find_element(By.CLASS_NAME,"emaillacking")
        pwdlacking = self.browser.find_element(By.CLASS_NAME,"pwdlacking")

        self.assertEqual(emaillacking.text, "An email is needed")
        self.assertEqual(pwdlacking.text, "A password is needed")  

        #Il va sur la page pour se reconnecter, il tente de se connecter sans username puis sans mot de passe
        click.login_someone("","password")
        userlacking = self.browser.find_element(By.CLASS_NAME,"userlacking")

        self.assertEqual(userlacking.text, "A username is needed") 
        self.assertEqual(self.browser.current_url, url + "/login/")
        
        click.clear_registration_inputs(self.browser.find_element(By.NAME, "username"),self.browser.find_element(By.NAME, "password"))
        click.login_someone("Tony", "")
        pwdlacking = self.browser.find_element(By.CLASS_NAME,"pwdlacking")

        self.assertEqual(pwdlacking.text, "A password is needed") 

        #Il met enfin ses bons identifiants.
        click.login_someone("Tony", "password") 

        #Le visiteur arrive sur la page il voit le titre.
        self.assertIn('Tricount',self.browser.title)

        #Il voit la liste des tricount présents ou absents et clique sur le lien pour créer un nouveau tricount
        click.click_on_a_link(By.ID,'id_newcount')
        click.click_on_a_link(By.ID, 'countfromzero')
        
        self.assertEqual(self.browser.current_url, url + '/count/Tony/newcount') 
    
        #Il choisit une monnaie et vérifie qu'elle a bien été prise en compte :
        click.click_on_a_link(By.CLASS_NAME, "choose-currency")
        click.click_on_a_link(By.CLASS_NAME,"AFN")

        currency = self.browser.find_element(By.CLASS_NAME, "newtricount_currency")
        self.assertEqual(currency.get_attribute("value"), "AFN")

        #Il commence par remplir les différents participants à son premier tricount : les participants apparaissent sur la page du tricount ainsi que le nombre de participants qui s'incrémente.
        #Il en met deux puis se ravise, l'enlève puis le remet.
        click.add_participants('Jean')
        click.add_participants('Henri')
        click.click_on_a_link(By.CSS_SELECTOR,".closeparticipant[name = 'Henri']")
        time.sleep(2)

        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/Tony/newcount?currency=AFN")
        
        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        number_participants = self.browser.find_element(By.CLASS_NAME,"nb_participants") 

        self.assertIn('Tony', [participant.get_attribute("value") for participant in participants])
        self.assertIn('Jean', [participant.get_attribute("value") for participant in participants])
        self.assertEqual(number_participants.text,"Participants (2/50)") 

        click.add_participants('Heeeeeenri')

        #He changes of currency before validating the tricount
        click.click_on_a_link(By.CLASS_NAME, "choose-currency")
        click.click_on_a_link(By.CLASS_NAME,"EUR")

        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        number_participants = self.browser.find_element(By.CLASS_NAME,"nb_participants")

        self.assertIn('Heeeeeenri', [participant.get_attribute("value") for participant in participants])
        self.assertEqual(number_participants.text,"Participants (3/50)")

        #Il remplit les données d'un nouveau tricount et les envoie et voit ses données apparaître sur la page recensant la liste des tricount.
        click.add_tricount_characteristics('Tricount 1', 'pwd1', 'Description 1',"EUR", 'trip')

        #He arrives on the good url 
        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/Tony/tricount/1')

        click.click_on_a_link(By.CLASS_NAME,'backtolistecount')

        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/Tony')
        self.assertIn('Tricount',self.browser.title)

        #Il est alors renvoyé vers la page recensant la liste des tricount : son tricount est apparu.
        title = self.browser.find_elements(By.CLASS_NAME,'tricount_title')
        description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')

        self.assertIn('Tricount 1',[titre.text for titre in title]) 
        self.assertIn('Description 1',[desc.text for desc in description])

        #Il reclique pour recréer un second tricount. 
        click.click_on_a_link(By.ID,'id_newcount')
        click.click_on_a_link(By.ID, 'countfromzero')
        
        self.assertEqual(self.browser.current_url, url + '/count/Tony/newcount') 
        
        #Il remplit les différents participants d'un second tricount : les participants apparaissent sur la page du tricount mais pas ceux du tricount précédemment créé.
        click.add_participants('Tony','Dulcinée','Annie')
        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")

        self.assertNotIn('Jean', [participant.text for participant in participants])
        self.assertNotIn('Heeeeeenri', [participant.text for participant in participants])

        #Il remplit les données d'un nouveau tricount et les envoie et voit ses données apparaître sur la page recensant la liste des tricount.
        click.add_tricount_characteristics('Tricount 2', 'pwd2', 'Description 2',"EUR", 'project')

        #He arrives on the good url 
        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/Tony/tricount/2' )
 
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount')

        #Il est alors renvoyé vers la page recensant la liste des tricount : son tricount est apparu.
        title = self.browser.find_elements(By.CLASS_NAME,'tricount_title')
        description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')

        self.assertIn('Tricount 2',[titre.text for titre in title]) 
        self.assertIn('Description 2',[desc.text for desc in description])

        #Il reclique pour recréer un tricount 
        click.click_on_a_link(By.ID,'id_newcount')        
        click.click_on_a_link(By.ID, 'countfromzero')

        # Il remplit les données d'un nouveau tricount mais oublie de mettre un titre
        # Il est renvoyé vers l'url de remplissagedu tricount avec un message d'erreur affiché en rouge 
        click.add_tricount_characteristics('', 'pwd3', 'description 3',"EUR", 'project')

        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/Tony/newcount/addcount')

        msg = self.browser.find_element(By.CLASS_NAME,'error')

        self.assertIn('Le titre doit comporter au moins un caractère.',msg.text)
 
        #Du coup, il rajoute un titre mais oublie de mettre des participants:    
        click.add_tricount_characteristics('Tricount 3','pwd3', '',"EUR", 'project')
        participant_error = self.browser.find_element(By.CLASS_NAME,'participant-error')

        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/Tony/newcount/addcount')
        self.assertIn("Il faut au moins un participant",participant_error.text) 

        #Il oublie maintenant le mot de passe :
        click.add_tricount_characteristics('Tricount 3','', 'description3',"EUR", 'project')
        pwd_error = self.browser.find_element(By.CLASS_NAME, 'pwd-error')

        self.assertEqual(pwd_error.text, 'Il faut un mot de passe')

        #Il met des participants puis crée son tricount. 
        click.add_participants('Totolitoto','Biloute','Anne')
        click.add_tricount_characteristics('Tricount 3','pwd3', '',"EUR", 'project')

        click.click_on_a_link(By.CLASS_NAME,'backtolistecount')
        description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')

        self.assertIn('Pas de description',[desc.text for desc in description])

        #Il veut créer un nouveau tricount mais change d'avis et après avoir rentré un participant appuie sur le bouton retour en arrière
        #Il atterrit à nouveau sur la liste des tricount. 
        click.click_on_a_link(By.ID,'id_newcount') 
        click.click_on_a_link(By.ID, 'countfromzero')

        click.add_participants('Jeanine') 
        click.click_on_a_link(By.CLASS_NAME,'backtotricount')

        self.assertEqual(self.browser.current_url, url + '/count/Tony')

        #Il clique pour créer un nouveau tricount et voit que les participants précédemment entrés ne sont pas sur la page
        click.click_on_a_link(By.ID,'id_newcount')
        click.click_on_a_link(By.ID, 'countfromzero')
        
        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")

        self.assertNotIn('Jeanine',[participant.text for participant in participants])

        click.click_on_a_link(By.CLASS_NAME,'backtotricount')

        #Il clique maintenant sur les tricounts existant pour vérifier que les informations du tricount sont correctes. 
        click.click_on_an_existing_tricount(1)

        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/Tony/tricount/1")

        tricount_title = self.browser.find_element(By.CLASS_NAME,"tricount-title")
        tricount_participants = self.browser.find_elements(By.CLASS_NAME,"tricount-participants")
        count = Counts.objects.get(id=1)
        
        self.assertEqual(tricount_title.text, count.title)
        self.assertIn('Jean', [name.text for name in tricount_participants])  
        
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount') 
        click.click_on_an_existing_tricount(2)

        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/Tony/tricount/2")

        tricount_title = self.browser.find_element(By.CLASS_NAME,"tricount-title")
        tricount_participants = self.browser.find_elements(By.CLASS_NAME,"tricount-participants")
        count = Counts.objects.get(id=2)
        
        self.assertEqual(tricount_title.text, count.title)
        self.assertIn('Dulcinée', [name.text for name in tricount_participants]) 
        self.assertIn('Annie', [name.text for name in tricount_participants]) 

        #Il va ensuite supprimer ce second tricount mais clique sur non lorsqu'on lui demande confirmation.
        click.click_on_a_link(By.CLASS_NAME,"tricount-characteristics")
        click.click_on_a_link(By.CLASS_NAME, "delete-tricount")

        click.click_on_a_link(By.ID, "no")

        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/Tony/tricount/2/modifycount')

        #Il recommence en cliquant sur oui et voit que sa liste n'en contient plus que deux tricounts.
        click.click_on_a_link(By.CLASS_NAME, "delete-tricount")

        click.click_on_a_link(By.ID, "yes")

        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/Tony')

        counts = self.browser.find_elements(By.CLASS_NAME, "link-tricount")
        
        self.assertEqual(len(counts),2)
        self.assertListEqual(["link-tricount-1", "link-tricount-3"], [count.get_attribute("id") for count in counts])

class MultiUsersTricount(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(1)
        self.browser2 = webdriver.Firefox()
        self.browser2.implicitly_wait(1)
    
    def tearDown(self): 
        self.browser.quit()
        self.browser2.quit()

    def test_clone_creation(self):
        #Deux utilisateurs s'enregistrent sur deux browser différents et se loggent
        click = user_experience.Click(self.browser, self.live_server_url)
        click2 = user_experience.Click(self.browser2, self.live_server_url)
        click.register_and_login_someone("Tony", "tony.fevrier@gmail.com","hello")
        click2.register_and_login_someone("Dulcinee", "dul.cinee@gmail.com","hello2")

        #L'utilisateur 1 crée un tricount.
        click.create_a_tricount("Tricount1", "rightpassword","description","EUR", 'project',"Tony","Dulcinee")
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount')

        #L'utilisateur 2 arrive sur sa liste de tricount et cherche à clôner le tricount qui a été créé par l'utilisateur 1. Il se trompe de mot de passe, il est renvoyé sur cette même page
        click2.clone_a_tricount("Tricount1", "falsepassword") 
        self.assertEqual(self.live_server_url + "/count/Dulcinee" , self.browser2.current_url)

        #Il oublie de mettre un mot de passe : un message apparaît.
        
        click2.clone_a_tricount("Tricount1","")
        error = self.browser2.find_element(By.CLASS_NAME, "error")
        
        self.assertEqual(error.text, "Remplissez le titre et le mot de passe")

        #Il recommence et tape le bon mot de passe, il est envoyé vers la liste de ses tricount et le tricount de l'utilisateur 1 est apparu.
        click2.click_on_a_link(By.CLASS_NAME, "id_newcount")
        click2.clone_a_tricount("Tricount1", "rightpassword")
  
        tricount = self.browser.find_element(By.CLASS_NAME, 'tricount_title') 
        self.assertEqual(tricount.text, "Tricount1")
        
        #Le second utilisateur crée une dépense et celle-ci apparait bien sur les deux comptes d'utilisateur.
        click2.click_on_an_existing_tricount(1)
        click2.click_on_create_spending()
        click2.create_a_spending('Dépense1',10,'Dulcinee',['Dulcinee','Tony'],'EUR')

        spending_title = self.browser2.find_elements(By.CLASS_NAME,"spending-title") 
        self.assertIn('Dépense1',[name.text for name in spending_title]) 

        click.click_on_an_existing_tricount(1)
        spending_title = self.browser.find_elements(By.CLASS_NAME,"spending-title") 
        self.assertIn('Dépense1',[name.text for name in spending_title]) 

        



class RegisterSpending(StaticLiveServerTestCase,user_experience.Check):
    
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def test_spending_creation(self): 
        
        click = user_experience.Click(self.browser, self.live_server_url)
        #MODIFIER check IN : normalement pas besoin de modifier create spending : devrait créer un dico 

        #The user register and log in
        click.register_and_login_someone("Dulciny","dulciny@dulciny.fr", "dulciny")

        #A tricount is created et come back to the listecount page 
        click.create_a_tricount('Tricount1',"pwd","Je décris", "EUR", "project","Jean","Henri","Dulciny")
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount') 

        #He creates a second tricount in an other currency : 
        click.create_a_tricount('Tricount1bis',"pwdbis","Je décris", "USD", "project","Jean","Henri","Dulciny")
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount') 

        #The user clicks on an existing tricount 
        click.click_on_an_existing_tricount(1)

        #The user clicks to add a new spending, he has the choice between the participants previously created
        click.click_on_create_spending()

        self.assertEqual(self.browser.current_url,self.live_server_url + '/count/Dulciny/tricount/1/spending')
        
        spender_participant = self.browser.find_elements(By.CLASS_NAME, "spender-participant")
        receiver_participants = self.browser.find_elements(By.CLASS_NAME, "receiver-participant")

        self.assertIn("Jean",[name.text for name in spender_participant])
        self.assertIn("Henri",[name.text for name in spender_participant])
        self.assertIn("Jean",[name.text for name in receiver_participants])
        self.assertIn("Henri",[name.text for name in receiver_participants])

        #He enters the title, amount the payer and for who the payer paid
        click.create_a_spending('Dépense1', 100., 'Jean', ['Henri','Jean'],'EUR')

        #He is then redirected to the spending list where the name, the amount, the payer appears
        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/Dulciny/tricount/1')
        
        spending_title = self.browser.find_elements(By.CLASS_NAME,"spending-title")
        spending_amount = self.browser.find_elements(By.CLASS_NAME,"spending-amount")
        spending_payer = self.browser.find_elements(By.CLASS_NAME,"spending-payer")
         
        self.assertIn('Dépense1',[name.text for name in spending_title])
        self.assertIn(100.,[float(name.text) for name in spending_amount])
        self.assertIn('Jean',[name.text for name in spending_payer])

        #He tries to create a second spending. He forgets to put a title, a message of error appears and he stays on the page.
        click.click_on_create_spending()
        click.create_a_spending('', 100., 'Jean', ['Henri','Jean'],'EUR')

        notitle = self.browser.find_element(By.CLASS_NAME,"notitle")

        self.assertEqual(notitle.text, "Titre non valable")
        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/Dulciny/tricount/1/addspending")

        #He forgets to put the amount, a spending is created with amount 0.
        click.create_a_spending('Dépense2', '', 'Jean', ['Henri','Jean'],'EUR')

        amounts = self.browser.find_elements(By.CLASS_NAME,"spending-amount")
        
        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/Dulciny/tricount/1")
        self.assertIn('0.0',[amount.text for amount in amounts])

        #He wants to check the current equilibria
        click.click_on_a_link(By.CLASS_NAME,"gotoequilibria")
        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/Dulciny/tricount/1/equilibria")

        #He clicks back
        click.click_on_a_link(By.CLASS_NAME,"gotospending")
        self.assertEqual(self.browser.current_url,  self.live_server_url + "/count/Dulciny/tricount/1")

        #He creates a second spending in USD for the second tricount.
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount')
        click.click_on_an_existing_tricount(2)

        click.click_on_create_spending()
        click.create_a_spending('Dépense en dollars', 100., 'Jean', ['Henri','Jean'],'USD')
        spendings = self.browser.find_elements(By.CLASS_NAME,'spending')

        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/Dulciny/tricount/2')
        self.assertEqual(len(spendings), 1)

        #He modifies the spending of the first tricount and is redirected to the page of the spending he modifies, the informations of the spending are written
        click.click_on_a_link(By.CLASS_NAME, "backtolistecount")
        click.click_on_an_existing_tricount(1)
        click.click_on_an_existing_spending(1)
        click.click_on_a_link(By.CLASS_NAME, "modify-spending")

        title = self.browser.find_element(By.CLASS_NAME, "title")
        amount = self.browser.find_element(By.CLASS_NAME, "amount")

        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/Dulciny/tricount/1/spending/1/modifyspending')
        self.assertEqual(title.get_attribute("value"), "Dépense1")
        self.assertEqual(amount.get_attribute("value"), '100.0')

        click.modify_a_spending({'amount':100},"Dulciny", "Henri")

        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/Dulciny/tricount/1/spending/1')

        #He also notes that the amounts have been correctly modified
        self.check_informations_of_a_spending('dépense1','100.0', 'Payé par Jean', ['Dulciny','Henri'],['50.0', '50.0'])

        #He makes an other modification : he modifies the spender         
        click.click_on_a_link(By.CLASS_NAME, "modify-spending")
        click.modify_a_spending({'title': 'spending','spender': "Henri"},"Dulciny", "Henri")

        self.check_informations_of_a_spending('spending','100.0', 'Payé par Henri', ['Dulciny','Henri'],['50.0', '50.0'])

        #He then click to modify a spending but do not change anything and validate : he is redirected correctly to the spending details.
        click.click_on_a_link(By.CLASS_NAME, "modify-spending")
        click.click_on_a_link(By.CLASS_NAME, "submit-spending")

        self.assertEqual(self.browser.current_url, self.live_server_url + '/count/Dulciny/tricount/1/spending/1')


    def test_the_page_of_some_spendings(self):
        
        click = user_experience.Click(self.browser, self.live_server_url) 
        #The user register and log in
        click.register_and_login_someone("Dulciny","dulciny@dulciny.fr", "dulciny")

        #L'utilisateur crée une dépense et clique dessus
        click.create_a_tricount('Tricount1',"pwd","Je décris", "EUR", "project","Jean","Henri") 

        click.click_on_create_spending()
        click.create_a_spending('Depense1', 120., 'Jean', ['Henri','Jean','Dulciny'],'EUR')
 
        click.click_on_an_existing_spending(1)
        time.sleep(3)

        #Il arrive sur la page et il y voit toutes les données qu'il a enregistrées.
        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/Dulciny/tricount/1/spending/1")
        self.check_informations_of_a_spending('depense1', '120.0', 'Payé par Jean', ['Dulciny','Henri','Jean'],['40.0', '40.0', '40.0'])

        #Il revient en arrière et crée trois autres dépenses
        click.click_on_a_link(By.CLASS_NAME,"backtospending")
 
        click.click_on_create_spending()
        click.create_a_spending('Depense2', 12., 'Henri', ['Henri','Jean','Dulciny'],'EUR') 
        click.click_on_create_spending()
        click.create_a_spending('Depense3', 3., 'Henri', ['Henri','Jean','Dulciny'],'EUR')

        #Il clique à nouveau sur la première dépense puis sur suivant
        click.click_on_an_existing_spending(1)
        click.click_on_a_link(By.CLASS_NAME,"following")

        #Il voit alors les infos de la seconde dépense et le bouton précédent apparaître
        self.check_informations_of_a_spending('depense2', '12.0', 'Payé par Henri', ['Dulciny','Henri','Jean'],['4.0', '4.0', '4.0'])
        self.assertIsNotNone(self.browser.find_element(By.CLASS_NAME,'previous'))

        #Il clique sur suivant une fois et voit le bouton suivant disparaître
        click.click_on_a_link(By.CLASS_NAME,"following") 
        self.check_informations_of_a_spending('depense3', '3.0', 'Payé par Henri', ['Dulciny','Henri','Jean'],['1.0', '1.0', '1.0'])
        #self.assertIsNone(self.browser.find_element(By.CLASS_NAME,'following'))

        #Il clique sur précédent trois fois et revient à la liste des dépenses
        click.click_on_a_link(By.CLASS_NAME,"previous")
        click.click_on_a_link(By.CLASS_NAME,"previous")
        click.click_on_a_link(By.CLASS_NAME,"backtospending")

        #Il clique sur le titre du tricount et voit les bonnes informations préremplies
        click.click_on_a_link(By.CLASS_NAME,"tricount-characteristics")

        title = self.browser.find_element(By.CLASS_NAME, "tricount_title")
        description = self.browser.find_element(By.CLASS_NAME, "tricount_description")
        participants = self.browser.find_elements(By.CLASS_NAME, "nameparticipant") 

        self.assertEqual(title.get_attribute("value"), "Tricount1")
        self.assertEqual(description.get_attribute("value"), "Je décris")
        self.assertIn("Jean", [participant.get_attribute("value") for participant in participants])
        self.assertIn("Henri", [participant.get_attribute("value") for participant in participants])
        
        #Il modifie le titre et la description puis valide. Il voit les nouvelles informations modifiées.
        click.modify_a_tricount({'tricount_title':'Tricount2','tricount_description':'autre'}) 

        #Il reclique sur le titre du tricount et ajoute un nouveau participant tout en supprimant un autre
        click.click_on_a_link(By.CLASS_NAME,"tricount-characteristics")
        click.modify_a_tricount(participants_to_add = ["Robert"], participants_to_delete = ["Jean"]) 

        participants = self.browser.find_elements(By.CLASS_NAME, "tricount-participants")
        self.assertIn("Robert", [participant.text for participant in participants])
        self.assertNotIn("Jean", [participant.text for participant in participants])

        #Il crée une nouvelle dépense et observe que les participants mis à jour sont présents.
        click.click_on_create_spending()
        click.create_a_spending('Depense2', 100., 'Robert', ['Henri','Dulciny'],'EUR') 
        click.click_on_create_spending()
        click.create_a_spending('Depense2', 50., 'Robert', ['Henri'],'EUR')  

        #Il clique sur les équilibres et observe que même le participant supprimé est toujours présent.
        click.click_on_a_link(By.CLASS_NAME, "gotoequilibria")

        credits = self.browser.find_elements(By.CLASS_NAME,"credits")
        for credit in credits:
            participant = credit.find_element(By.CLASS_NAME,"participant")
            amount = credit.find_element(By.CLASS_NAME,"amount")
            self.assertIn([participant.text,amount.text], [["Robert","150.0 EUR"],["Henri","-130.0 EUR"],["Dulciny","-95.0 EUR"],["Jean","75.0 EUR"]])

    def test_equilibria_with_multiple_spendings(self):
        
        click = user_experience.Click(self.browser, self.live_server_url) 
        
        #The user register and log in
        click.register_and_login_someone("Marine","dulciny@dulciny.fr", "dulciny")

        click.create_a_tricount('Tricount1',"pwd","Je décris", "EUR", "project","Henri", "Yann", "Marine", "Tony") 

        click.click_on_create_spending() 
        click.create_a_spending('dépense1', 100, 'Tony', ['Henri','Yann','Marine','Tony'],'EUR') 
        click.click_on_create_spending()
        click.create_a_spending('dépense2', 200, 'Marine', ['Henri','Yann','Marine','Tony'],'EUR') 
        click.click_on_create_spending()
        click.create_a_spending('dépense3', 150, 'Henri', ['Henri','Yann','Marine','Tony'],'EUR') 
        click.click_on_create_spending()
        click.create_a_spending('dépense4', 180, 'Yann', ['Henri','Yann','Marine','Tony'],'EUR') 
        click.click_on_a_link(By.CLASS_NAME, "gotoequilibria")
        time.sleep(4)

        #Vérification des crédits totaux des participants
        credits = self.browser.find_elements(By.CLASS_NAME,"credits")
        for credit in credits:
            participant = credit.find_element(By.CLASS_NAME,"participant")
            amount = credit.find_element(By.CLASS_NAME,"amount")
            self.assertIn([participant.text,amount.text], [["Tony","-57.5 EUR"],["Henri","-7.5 EUR"],["Yann","22.5 EUR"],["Marine","42.5 EUR"]])
        
        #Les crédits dettes du propriétaire sont présentées d'abord, celles des autres dans la section suivante
        usersolutions = self.browser.find_elements(By.NAME, "userinclude") 
        for usersolution in usersolutions:
            self.assertIn('Marine',[elt.text for elt in usersolution.find_elements(By.CLASS_NAME, 'who')])
        othersolutions = self.browser.find_elements(By.NAME, "nouserinclude")
        for othersolution in othersolutions:
            self.assertNotIn('Marine',[elt.text for elt in othersolution.find_elements(By.CLASS_NAME, 'who')]) 

    def test_modify_a_created_spending(self):
        pass

class JSTest(StaticLiveServerTestCase,user_experience.Check):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def test_JS_of_listecount_page(self):
        click = user_experience.Click(self.browser, self.live_server_url)

        #The user arrives on listecount page, no popup is opened :
        self.browser.get(self.live_server_url+ '/count/Toto')
        popup_children = self.browser.find_elements(By.CSS_SELECTOR, "[data-div = hidden] > *")

        for elt in popup_children:
            self.assertEqual(elt.is_displayed(),False) 

        #He creates a tricount and come back.
        click.create_a_tricount('Tricount1',"pwd","Je décris", "EUR", "project","Jean","Henri")
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount')  

        # he clicks on parameters, a popup appears
        click.click_on_a_link(By.CLASS_NAME,"parameters")
        self.check_if_popup_displayed("parameters-options",True) 
        
        #He clicks on a JS button of the popup, an other popup replaces the previous one.
        click.click_on_a_link(By.CLASS_NAME, "conditions") 
        self.check_if_popup_displayed("parameters-options",False)
        self.check_if_popup_displayed("conditions-options",True)

        #He clicks on the link of the tricount and no popup is visible and he stays on the same page.
        click.click_on_a_link(By.CLASS_NAME,"link-tricount")

        popup_children = self.browser.find_elements(By.CSS_SELECTOR, "[data-div = hidden] > *")

        for elt in popup_children:
            self.assertEqual(elt.is_displayed(),False)
        self.assertEqual(self.browser.current_url, self.live_server_url + "/count/Toto")

    def test_JS_of_newcount_page(self):
        click = user_experience.Click(self.browser, self.live_server_url)

        #The client goes to the creation of a new count
        self.browser.get(self.live_server_url+ '/count/Toto')
        click.click_on_a_link(By.CLASS_NAME,'id_newcount')
        click.click_on_a_link(By.ID,'countfromzero')

        #He enters a title and a description, a counter appears and the number of letters corresponds to the length of the word.
        titlebox = self.browser.find_element(By.NAME,"newtricount_title")
        descriptionbox = self.browser.find_element(By.NAME,"newtricount_description")  
        
        titlebox.click()
        counter = self.browser.find_element(By.CLASS_NAME, "compteur")
        
        self.assertEqual(counter.text, '0/50')
        self.assertEqual(counter.is_displayed(),True) 

        #He tries to put a more than fifty letters title but he is blocked 
        titlebox.send_keys('t'*51)
        time.sleep(2)
        self.assertEqual(counter.text, '50/50')
        titlebox.clear()

        #So he writes a shorter title
        titlebox.send_keys('titre')
        time.sleep(2)
        self.assertEqual(counter.text, '5/50')

        descriptionbox.send_keys('description')
        self.assertEqual(counter.text, '11/500')
        time.sleep(2)

    def test_JS_currency_research_bar(self):
        click = user_experience.Click(self.browser, self.live_server_url)

        #The client creates a new count and begins to create a tricount.
        self.browser.get(self.live_server_url+ '/count/Toto')
        click.click_on_a_link(By.CLASS_NAME,'id_newcount')
        click.click_on_a_link(By.ID,'countfromzero')

        click.click_on_a_link(By.CLASS_NAME, "choose-currency")
        loupe = self.browser.find_element(By.CLASS_NAME, "currencyresearch") 
        self.assertEqual(loupe.is_displayed(),True) 

        #He clicks on the loop and the research bar appears.
        click.click_on_a_link(By.CLASS_NAME, "currencyresearch")
        research = self.browser.find_element(By.CLASS_NAME, "research") 
        self.assertEqual(research.is_displayed(),True) 
        self.assertEqual(loupe.is_displayed(),False) 

        #He puts Euro and only one currency is suggested. 
        research.send_keys('euro')
        time.sleep(2)
        currencies = self.browser.find_elements(By.NAME,"link-newcount")
        displayed_currencies = 0
        for currency in currencies:
            if currency.is_displayed():
                displayed_currencies += 1
        self.assertEqual(displayed_currencies,3)

        #He then chooses to delete the research bar by pressing the backtonewcount arrow and it stays on the same page
        click.click_on_a_link(By.CLASS_NAME, "backtonewcount")
        self.assertEqual(self.browser.current_url, self.live_server_url+ '/count/Toto/newcount/currency')

        #He clicks an other time to go back to newcount page.
        click.click_on_a_link(By.CLASS_NAME, "backtonewcount")
        self.assertEqual(self.browser.current_url, self.live_server_url+ '/count/Toto/newcount')



        
        




