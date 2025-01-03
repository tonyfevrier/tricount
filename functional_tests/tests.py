#from django.test import LiveServerTestCase

from channels.testing import ChannelsLiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.options import Options 
import time

from count.models import Counts
from functional_tests import user_experience 

options = Options() 
options.binary_location = "/usr/bin/firefox-esr" #"C:\\Program Files\\Mozilla Firefox\\firefox.exe" si on exécute sur la machine hôte

# Partie à n'utiliser que si on exécute le test dans docker sans interface graphique
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

class NewVisitorTest(StaticLiveServerTestCase): 
    
    def setUp(self):
        self.browser = webdriver.Firefox(options=options)
        self.browser.implicitly_wait(3)
    
    def tearDown(self): 
        self.browser.quit()

    def test_tricount_creation_and_delation(self):
        # Le visiteur arrive sur la page, il se crée un compte et se logge et est redirigé vers la page de son compte
        url = self.live_server_url  
        click = user_experience.Click(self.browser, url)
        self.browser.get(url)

        click.register_someone("Tony","tony.fevrier62@gmail.com", "password")
        self.assertEqual(self.browser.current_url, url + "/count")

        # Il se déconnecte puis se connecte et atterrit sur la liste des tricounts
        click.logout_someone_from_listecount_page()
        click.login_someone("Tony", "password")
        self.assertEqual(self.browser.current_url, url + "/count")

        #Il va dans paramètres, constate que ses données sont bien présentes et se délogge directement 
        #click.click_on_successive_links(By.CLASS_NAME,"parameters","myparameters")
        click.click_on_a_link(By.CLASS_NAME, "logout")
        firstletter,name,mail = click.find_multiple_elements(By.CLASS_NAME,"firstletter","hello","mail")
        self.assertEqual(firstletter.text, "T")
        self.assertEqual(name.text, "Hello Tony")
        self.assertEqual(mail.text, "tony.fevrier62@gmail.com")

        click.click_on_a_link(By.CLASS_NAME, "logout")
        self.assertEqual(self.browser.current_url, url + "/log")

        #Il tente d'enregistrer un nouveau compte avec le même username puis avec le même mail mais est refusé
        click.click_on_a_link(By.CLASS_NAME, "welcome")
        click.register_someone("Tony", "tony@gmail.com","pwd")
        self.assertEqual(self.browser.current_url, url + "/")

        click.register_someone("Dulcinée", "tony.fevrier62@gmail.com","pwd")
        self.assertEqual(self.browser.current_url, url + "/") 

        #Il tente d'envoyer le formulaire sans username puis sans email et password, le formulaire n'est pas envoyé et des éléments apparaissent
        click.register_someone("", "tony.fevrier6@gmail.com","pwd")
        userlacking = self.browser.find_element(By.CLASS_NAME,"lack")
        self.assertEqual(userlacking.text, "A username is needed") 

        click.clear_registration_inputs(self.browser.find_element(By.NAME, "username"),
                                        self.browser.find_element(By.NAME, "email"),
                                        self.browser.find_element(By.NAME, "password"))
        click.register_someone("Dulcinée", "", "") 
        elements = self.browser.find_elements(By.CLASS_NAME, "lack")
        #emaillacking,pwdlacking = click.find_multiple_elements(By.CLASS_NAME,"emaillacking","pwdlacking")
        self.assertIn("An email is needed", [element.text for element in elements])
        self.assertIn("A password is needed", [element.text for element in elements])  

        #Il va sur la page pour se reconnecter, il tente de se connecter sans username puis sans mot de passe
        click.login_someone("","password")
        userlacking = self.browser.find_element(By.CLASS_NAME,"lack")

        self.assertEqual(userlacking.text, "A username is needed") 
        self.assertEqual(self.browser.current_url, url + "/log")
        
        click.clear_registration_inputs(self.browser.find_element(By.NAME, "username"),self.browser.find_element(By.NAME, "password"))
        click.login_someone("Tony", "")
        pwdlacking = self.browser.find_element(By.CLASS_NAME,"lack")
        self.assertEqual(pwdlacking.text, "A password is needed") 

        # Il tente de s'identifier avec de faux identifiants
        click.login_someone("Jean","password")
        message = self.browser.find_element(By.CLASS_NAME, "messages")
        self.assertEqual(message.text, 'Invalid credentials')

        #Il met enfin ses bons identifiants.
        click.clear_registration_inputs(self.browser.find_element(By.NAME, "username"),self.browser.find_element(By.NAME, "password"))
        click.login_someone("Tony", "password") 

        #Le visiteur arrive sur la page il voit le titre.
        self.assertIn('Tricount',self.browser.title)

        #Il voit la liste des tricount présents ou absents et clique sur le lien pour créer un nouveau tricount  
        click.click_on_successive_links(By.ID,'id_newcount','countfromzero')     
        self.assertEqual(self.browser.current_url, url + '/newcount') 
    
        #Il choisit une monnaie et vérifie qu'elle a bien été prise en compte : 
        click.click_on_successive_links(By.CLASS_NAME,"choose-currency","AFN")
        currency = self.browser.find_element(By.CLASS_NAME, "newtricount_currency")
        self.assertEqual(currency.get_attribute("value"), "AFN")

        #Il commence par remplir les différents participants à son premier tricount : les participants apparaissent sur la page du tricount ainsi que le nombre de participants qui s'incrémente.
        #Il en met deux puis se ravise, l'enlève puis le remet.
        click.add_participants('Jean','Henri') 
        click.click_on_a_link(By.CSS_SELECTOR,".closeparticipant[name = 'Henri']")
        self.assertEqual(self.browser.current_url, self.live_server_url + "/newcount?currency=AFN")
        
        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        number_participants = self.browser.find_element(By.CLASS_NAME,"nb_participants") 
        self.assertIn('Tony', [participant.get_attribute("value") for participant in participants])
        self.assertIn('Jean', [participant.get_attribute("value") for participant in participants])
        self.assertEqual(number_participants.text,"Participants (2/50)") 

        click.add_participants('Heeeeeenri')

        #He changes of currency before validating the tricount 
        click.click_on_successive_links(By.CLASS_NAME,"choose-currency","EUR")
        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        number_participants = self.browser.find_element(By.CLASS_NAME,"nb_participants")
        self.assertIn('Heeeeeenri', [participant.get_attribute("value") for participant in participants])
        self.assertEqual(number_participants.text,"Participants (3/50)")

        #Il remplit les données d'un nouveau tricount et les envoie et voit ses données apparaître sur la page recensant la liste des tricount.
        click.add_tricount_characteristics('Tricount 1', 'pwd1', 'Description 1',"EUR", 'trip')

        #He arrives on the good url 
        self.assertEqual(self.browser.current_url, self.live_server_url + '/tricount/1')

        click.click_on_a_link(By.CLASS_NAME,'backtolistecount')
        self.assertEqual(self.browser.current_url, self.live_server_url + '/count')
        self.assertIn('Tricount',self.browser.title)

        #Il est alors renvoyé vers la page recensant la liste des tricount : son tricount est apparu.
        title = self.browser.find_elements(By.CLASS_NAME,'tricount_title')
        description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')
        self.assertIn('Tricount 1',[titre.text for titre in title]) 
        self.assertIn('Description 1',[desc.text for desc in description])

        # Il tente de créer un tricount en se supprimant des participants
        click.click_on_successive_links(By.ID,'id_newcount','countfromzero')
        click.add_participants('Jean','Heeeeeenri')
        click.click_on_a_link(By.CSS_SELECTOR, "button[name='Tony']")
        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        self.assertNotIn('Tony', [participant.text for participant in participants])
        click.add_tricount_characteristics('Tricount 2', 'pwd2', 'Description 2',"EUR", 'project')
        self.assertEqual(self.browser.current_url, self.live_server_url + '/tricount/2' )

        #Il reclique pour recréer un troisième tricount.  
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount')
        click.click_on_successive_links(By.ID,'id_newcount','countfromzero')
        self.assertEqual(self.browser.current_url, url + '/newcount') 
        
        #Il remplit les différents participants d'un troisième tricount : les participants apparaissent sur la page du tricount mais pas ceux du tricount précédemment créé.
        click.add_participants('Tony','Dulcinée','Annie')
        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        self.assertNotIn('Jean', [participant.text for participant in participants])
        self.assertNotIn('Heeeeeenri', [participant.text for participant in participants])

        #Il remplit les données d'un nouveau tricount et les envoie et voit ses données apparaître sur la page recensant la liste des tricount.
        click.add_tricount_characteristics('Tricount 3', 'pwd3', 'Description 3',"EUR", 'project')

        #He arrives on the good url 
        self.assertEqual(self.browser.current_url, self.live_server_url + '/tricount/3' )

        #Il est alors renvoyé vers la page recensant la liste des tricount : son tricount est apparu.
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount')
        title = self.browser.find_elements(By.CLASS_NAME,'tricount_title')
        description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')
        self.assertIn('Tricount 3',[titre.text for titre in title]) 
        self.assertIn('Description 3',[desc.text for desc in description])

        #Il reclique pour recréer un tricount  
        click.click_on_successive_links(By.ID,'id_newcount','countfromzero')

        # Il remplit les données d'un nouveau tricount mais oublie de mettre un titre
        # Il est renvoyé vers l'url de remplissagedu tricount avec un message d'erreur affiché en rouge 
        click.add_tricount_characteristics('', 'pwd3', 'description 3',"EUR", 'project')
        #self.assertEqual(self.browser.current_url, self.live_server_url + '/addcount')

        msg = self.browser.find_element(By.CLASS_NAME,'error')
        self.assertIn('Title must contain at least one letter.',msg.text)
 
        #Du coup, il rajoute un titre mais oublie de mettre des participants:    
        click.add_tricount_characteristics('Tricount 3','pwd3', '',"EUR", 'project')
        participant_error = self.browser.find_element(By.CLASS_NAME,'participant-error') 
        self.assertIn("You need at least one participant.",participant_error.text) 

        #Il oublie maintenant le mot de passe :
        click.clear_registration_inputs(self.browser.find_element(By.NAME, "newtricount_title"),
                                        self.browser.find_element(By.NAME, "newtricount_pwd"),
                                        self.browser.find_element(By.NAME, "newtricount_description"),
                                        )
        click.add_tricount_characteristics('Tricount 3','', 'description3',"EUR", 'project')
        pwd_error = self.browser.find_element(By.ID, 'pwd-error')
        self.assertEqual(pwd_error.text, 'Enter a password')

        #Il met des participants puis crée son tricount. 
        click.add_participants('Totolitoto','Biloute','Anne')
        click.clear_registration_inputs(self.browser.find_element(By.NAME, "newtricount_title"),
                                        self.browser.find_element(By.NAME, "newtricount_description"))
        click.add_tricount_characteristics('Tricount 4','pwd4', '',"EUR", 'project')
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount')
        description = self.browser.find_elements(By.CLASS_NAME,'tricount_description')
        self.assertIn('Pas de description',[desc.text for desc in description])

        #Il veut créer un nouveau tricount mais change d'avis et après avoir rentré un participant appuie sur le bouton retour en arrière
        #Il atterrit à nouveau sur la liste des tricount.  
        click.click_on_successive_links(By.ID,'id_newcount','countfromzero')
        click.add_participants('Jeanine') 
        click.click_on_a_link(By.CLASS_NAME,'backtotricount')
        self.assertEqual(self.browser.current_url, url + '/count')

        #Il clique pour créer un nouveau tricount et voit que les participants précédemment entrés ne sont pas sur la page 
        click.click_on_successive_links(By.ID,'id_newcount','countfromzero')
        participants = self.browser.find_elements(By.CLASS_NAME,"nameparticipant")
        self.assertNotIn('Jeanine',[participant.text for participant in participants])

        #Il clique maintenant sur les tricounts existant pour vérifier que les informations du tricount sont correctes. 
        click.click_on_a_link(By.CLASS_NAME,'backtotricount')
        click.click_on_an_existing_tricount(1)
        self.assertEqual(self.browser.current_url, self.live_server_url + "/tricount/1")

        tricount_title = self.browser.find_element(By.CLASS_NAME,"tricount-title")
        tricount_participants = self.browser.find_elements(By.CLASS_NAME,"tricount-participants")
        count = Counts.objects.get(id=1)
        
        self.assertEqual(tricount_title.text, count.title)
        self.assertIn('Jean', [name.text for name in tricount_participants])  
        
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount') 
        click.click_on_an_existing_tricount(3)
        self.assertEqual(self.browser.current_url, self.live_server_url + "/tricount/3")

        tricount_title = self.browser.find_element(By.CLASS_NAME,"tricount-title")
        tricount_participants = self.browser.find_elements(By.CLASS_NAME,"tricount-participants")
        count = Counts.objects.get(id=3)       
        self.assertEqual(tricount_title.text, count.title)
        self.assertIn('Dulcinée', [name.text for name in tricount_participants]) 
        self.assertIn('Annie', [name.text for name in tricount_participants]) 

        #Il va ensuite supprimer ce second tricount mais clique sur non lorsqu'on lui demande confirmation. 
        click.click_on_successive_links(By.CLASS_NAME,"tricount-characteristics","delete-tricount")
        alert = self.browser.switch_to.alert
        alert.dismiss() 
        self.assertEqual(self.browser.current_url, self.live_server_url + '/modifycount/3')

        #Il recommence en cliquant sur oui et voit que sa liste n'en contient plus que deux tricounts.
        click.click_on_a_link(By.CLASS_NAME, "delete-tricount")
        alert = self.browser.switch_to.alert
        alert.accept()
        time.sleep(2)
        self.assertEqual(self.browser.current_url, self.live_server_url + '/count')

        counts = self.browser.find_elements(By.CLASS_NAME, "link-tricount")
        self.assertEqual(len(counts),3)
        self.assertListEqual(["link-tricount-1", "link-tricount-2", "link-tricount-4"], [count.get_attribute("id") for count in counts])

class MultiUsersTricount(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox(options=options)
        self.browser.implicitly_wait(1)
        self.browser2 = webdriver.Firefox(options=options)
        self.browser2.implicitly_wait(1)
    
    def tearDown(self): 
        self.browser.quit()
        self.browser2.quit()

    def test_clone_creation(self):
        #Deux utilisateurs s'enregistrent sur deux browser différents et se loggent
        click = user_experience.Click(self.browser, self.live_server_url)
        click2 = user_experience.Click(self.browser2, self.live_server_url)
        click.register_and_login_someone("Tony", "tony.fevrier@gmail.com","hello")
        click2.register_and_login_someone("Dulcinee", "dulcinee@gmail.com","hello2")

        #L'utilisateur 1 crée un tricount.
        click.create_a_tricount("Tricount1", "rightpassword","description","EUR", 'project',"Tony","Dulcinee")
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount')

        #L'utilisateur 2 arrive sur sa liste de tricount et cherche à clôner le tricount qui a été créé par l'utilisateur 1. Il se trompe de mot de passe, il est renvoyé sur cette même page
        click2.click_on_a_link(By.ID,'id_newcount')  
        click2.click_on_a_link(By.CLASS_NAME,"clonecount") 
        click2.clone_a_tricount("Tricount1", "falsepassword") 
        error = self.browser2.find_element(By.ID, "Invalid")
        self.assertEqual(error.text, "Invalid credentials")
        self.assertEqual(self.live_server_url + "/count" , self.browser2.current_url)

        #Il oublie de mettre un mot de passe : un message apparaît. 
        click2.clear_registration_inputs(self.browser2.find_element(By.CLASS_NAME, "tricount-title"),
                                         self.browser2.find_element(By.CLASS_NAME, "password"),)
        click2.clone_a_tricount("Tricount1","")
        error = self.browser2.find_element(By.CLASS_NAME, "error")
        self.assertEqual(error.text, "Fill the title and password")

        #Il recommence et tape le bon mot de passe, il est envoyé vers la liste de ses tricount et le tricount de l'utilisateur 1 est apparu.
        click2.clear_registration_inputs(self.browser2.find_element(By.CLASS_NAME, "tricount-title"),
                                         self.browser2.find_element(By.CLASS_NAME, "password"),)
        click2.clone_a_tricount("tricount1", "rightpassword")
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
        self.browser = webdriver.Firefox(options=options)
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

        self.assertEqual(self.browser.current_url,self.live_server_url + '/newspending/1')
        
        spender_participant = self.browser.find_elements(By.CLASS_NAME, "spender-participant")
        receiver_participants = self.browser.find_elements(By.CLASS_NAME, "receiver-participant")
        self.assertIn("Jean",[name.text for name in spender_participant])
        self.assertIn("Henri",[name.text for name in spender_participant])
        self.assertIn("Jean",[name.text for name in receiver_participants])
        self.assertIn("Henri",[name.text for name in receiver_participants])

        #He enters the title, amount the payer and for who the payer paid
        click.create_a_spending('Dépense1', '100.', 'Jean', ['Henri','Jean'],'EUR')

        #He is then redirected to the spending list where the name, the amount, the payer appears
        self.assertEqual(self.browser.current_url, self.live_server_url + '/tricount/1')
        
        spending_title = self.browser.find_elements(By.CLASS_NAME,"spending-title")
        spending_amount = self.browser.find_elements(By.CLASS_NAME,"spending-amount")
        spending_payer = self.browser.find_elements(By.CLASS_NAME,"spending-payer")
        self.assertIn('Dépense1',[name.text for name in spending_title])
        self.assertIn(100.,[float(name.text) for name in spending_amount])
        self.assertIn('Jean',[name.text for name in spending_payer])

        #He tries to create a second spending. He forgets to put a title, a message of error appears and he stays on the page.
        click.click_and_create_a_spending('', '100.', 'Jean', ['Henri','Jean'],'EUR')
        notitle = self.browser.find_element(By.CLASS_NAME,"notitle")
        self.assertEqual(notitle.text, "Enter a title") 

        #He forgets to put the amount, a spending is created with amount 0.
        click.clear_registration_inputs(self.browser.find_element(By.ID, "amount"))
        click.create_a_spending('Dépense2', '', 'Jean', ['Henri','Jean'],'EUR')
        amounts = self.browser.find_elements(By.CLASS_NAME,"spending-amount") 
        self.assertEqual(self.browser.current_url, self.live_server_url + "/tricount/1")
        self.assertIn('0.00',[amount.text for amount in amounts])

        #He wants to check the current equilibria
        click.click_on_a_link(By.CLASS_NAME,"gotoequilibria")
        self.assertEqual(self.browser.current_url, self.live_server_url + "/equilibria/1")

        #He clicks back
        click.click_on_a_link(By.CLASS_NAME,"gotospending")
        self.assertEqual(self.browser.current_url,  self.live_server_url + "/tricount/1")

        #He creates a second spending in USD for the second tricount.
        click.click_on_a_link(By.CLASS_NAME,'backtolistecount')
        click.click_on_an_existing_tricount(2) 
        click.click_and_create_a_spending('Dépense en dollars', '100.', 'Jean', ['Henri','Jean'],'USD')
        spendings = self.browser.find_elements(By.CLASS_NAME,'spending')
        self.assertEqual(self.browser.current_url, self.live_server_url + '/tricount/2')
        self.assertEqual(len(spendings), 1)

        #He modifies the spending of the first tricount and is redirected to the page of the spending he modifies, the informations of the spending are written
        click.click_on_a_link(By.CLASS_NAME, "backtolistecount")
        click.click_on_an_existing_tricount(1)
        click.click_on_an_existing_spending(1)
        click.click_on_a_link(By.CLASS_NAME, "modify-spending")
        title = self.browser.find_element(By.CLASS_NAME, "title")
        amount = self.browser.find_element(By.CLASS_NAME, "amount")
        self.assertEqual(self.browser.current_url, self.live_server_url + '/modifyspending/1/1')
        self.assertEqual(title.get_attribute("value"), "Dépense1")
        self.assertEqual(amount.get_attribute("value"), '100.00')

        click.modify_a_spending({'amount':100},"Dulciny", "Henri")
        self.assertEqual(self.browser.current_url, self.live_server_url + '/spending-details/1/1')

        #He also notes that the amounts have been correctly modified
        self.check_informations_of_a_spending('dépense1','100.00', 'Paid by Jean', ['Dulciny','Henri'],['50.00', '50.00'])

        #He makes an other modification : he modifies the spender         
        click.click_on_a_link(By.CLASS_NAME, "modify-spending")
        click.modify_a_spending({'title': 'spending','spender': "Henri"},"Dulciny", "Henri")
        self.check_informations_of_a_spending('spending','100.00', 'Paid by Henri', ['Dulciny','Henri'],['50.00', '50.00'])

        #He then click to modify a spending but do not change anything and validate : he is redirected correctly to the spending details.
        click.click_on_successive_links(By.CLASS_NAME, "modify-spending","submit-spending")
        self.assertEqual(self.browser.current_url, self.live_server_url + '/spending-details/1/1')

        #He now decides to supress the last spending and is correctly redirected to the spendings which contains the good number of spendings
        click.click_on_successive_links(By.CLASS_NAME, "modify-spending","delete-spending")
        alert = self.browser.switch_to.alert
        alert.dismiss() 
        self.assertEqual(self.browser.current_url, self.live_server_url + '/modifyspending/1/1')

        click.click_on_a_link(By.CLASS_NAME, "delete-spending")
        alert = self.browser.switch_to.alert
        alert.accept()
        time.sleep(2)
        spendings = self.browser.find_elements(By.CLASS_NAME,'spending')
        self.assertEqual(self.browser.current_url, self.live_server_url + '/tricount/1')
        self.assertEqual(len(spendings), 1)

    def test_the_page_of_some_spendings(self):
        
        click = user_experience.Click(self.browser, self.live_server_url) 
        #The user register and log in
        click.register_and_login_someone("Dulciny","dulciny@dulciny.fr", "dulciny")

        #L'utilisateur crée une dépense et clique dessus0
        click.create_a_tricount('Tricount1',"pwd","Je décris", "EUR", "project","Jean","Henri") 
        click.click_and_create_a_spending('Depense1', '120.', 'Jean', ['Henri','Jean','Dulciny'],'EUR')
        click.click_on_an_existing_spending(1) 

        #Il arrive sur la page et il y voit toutes les données qu'il a enregistrées.
        self.assertEqual(self.browser.current_url, self.live_server_url + "/spending-details/1/1")
        self.check_informations_of_a_spending('depense1', '120.00', 'Paid by Jean', ['Dulciny','Henri','Jean'],['40.00', '40.00', '40.00'])

        #Il revient en arrière et crée trois autres dépenses
        click.click_on_a_link(By.CLASS_NAME,"backtospending")
        click.click_and_create_a_spending('Depense2', '12.', 'Henri', ['Henri','Jean','Dulciny'],'EUR') 
        click.click_and_create_a_spending('Depense3', '3.', 'Henri', ['Henri','Jean','Dulciny'],'EUR')

        #Il clique à nouveau sur la première dépense puis sur suivant
        click.click_on_an_existing_spending(1)
        click.click_on_a_link(By.CLASS_NAME,"following")

        #Il voit alors les infos de la seconde dépense et le bouton précédent apparaître
        self.check_informations_of_a_spending('depense2', '12.00', 'Paid by Henri', ['Dulciny','Henri','Jean'],['4.00', '4.00', '4.00'])
        self.assertIsNotNone(self.browser.find_element(By.CLASS_NAME,'previous'))

        #Il clique sur suivant une fois et voit le bouton suivant disparaître
        click.click_on_a_link(By.CLASS_NAME,"following") 
        self.check_informations_of_a_spending('depense3', '3.00', 'Paid by Henri', ['Dulciny','Henri','Jean'],['1.00', '1.00', '1.00']) 

        #Il clique sur précédent trois fois et revient à la liste des dépenses 
        click.click_on_successive_links(By.CLASS_NAME,"previous","previous","backtospending")

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
        click.click_and_create_a_spending('Depense2', '100.', 'Robert', ['Henri','Dulciny'],'EUR') 
        click.click_and_create_a_spending('Depense2', '50.', 'Robert', ['Henri'],'EUR')  

        #Il clique sur les équilibres et observe que même le participant supprimé est toujours présent.
        click.click_on_a_link(By.CLASS_NAME, "gotoequilibria")

        credits = self.browser.find_elements(By.CLASS_NAME,"credits")
        for credit in credits:
            participant = credit.find_element(By.CLASS_NAME,"participant")
            amount = credit.find_element(By.CLASS_NAME,"amount")
            self.assertIn([participant.text,amount.text], [["Robert","150.00 EUR"],
                                                           ["Henri","-130.00 EUR"],
                                                           ["Dulciny","-95.00 EUR"],
                                                           ["Jean","75.00 EUR"]])

    def test_equilibria_with_multiple_spendings(self):
        
        click = user_experience.Click(self.browser, self.live_server_url) 
        
        #The user register and log in
        click.register_and_login_someone("Marine","dulciny@dulciny.fr", "dulciny")
        click.create_a_tricount('Tricount1',"pwd","Je décris", "EUR", "project","Henri", "Yann", "Marine", "Tony") 
        click.click_on_create_spending() 
        click.create_a_spending('dépense1', '100', 'Tony', ['Henri','Yann','Marine','Tony'],'EUR') 
        click.click_on_create_spending()
        click.create_a_spending('dépense2', '200', 'Marine', ['Henri','Yann','Marine','Tony'],'EUR') 
        click.click_on_create_spending()
        click.create_a_spending('dépense3', '150', 'Henri', ['Henri','Yann','Marine','Tony'],'EUR') 
        click.click_on_create_spending()
        click.create_a_spending('dépense4', '180', 'Yann', ['Henri','Yann','Marine','Tony'],'EUR') 
        click.click_on_a_link(By.CLASS_NAME, "gotoequilibria")
        time.sleep(4)

        #Vérification des crédits totaux des participants
        credits = self.browser.find_elements(By.CLASS_NAME,"credits")
        for credit in credits:
            participant = credit.find_element(By.CLASS_NAME,"participant")
            amount = credit.find_element(By.CLASS_NAME,"amount")
            self.assertIn([participant.text,amount.text], [["Tony","-57.50 EUR"],["Henri","-7.50 EUR"],["Yann","22.50 EUR"],["Marine","42.50 EUR"]])
        
        #Les crédits dettes du propriétaire sont présentées d'abord, celles des autres dans la section suivante
        usersolutions = self.browser.find_elements(By.NAME, "userinclude") 
        for usersolution in usersolutions:
            self.assertIn('Marine',[elt.text for elt in usersolution.find_elements(By.CLASS_NAME, 'who')])
        othersolutions = self.browser.find_elements(By.NAME, "nouserinclude")
        for othersolution in othersolutions:
            self.assertNotIn('Marine',[elt.text for elt in othersolution.find_elements(By.CLASS_NAME, 'who')]) 


class JSTest(StaticLiveServerTestCase,user_experience.Check):
    def setUp(self):
        self.browser = webdriver.Firefox(options=options)
        self.browser.implicitly_wait(3)
        click = user_experience.Click(self.browser, self.live_server_url)
        click.register_and_login_someone('tony', 't@gmail.com', '1234')
        self.click = click
    
    def tearDown(self):
        self.browser.quit()

    # def test_JS_of_listecount_page(self):

    #     #The user arrives on listecount page, no popup is opened :
    #     self.browser.get(self.live_server_url+ '/count')
    #     popup_children = self.browser.find_elements(By.CSS_SELECTOR, "[data-div = hidden] > *")

    #     for elt in popup_children:
    #         self.assertEqual(elt.is_displayed(),False) 

    #     #He creates a tricount and come back.
    #     self.click.create_a_tricount('Tricount1',"pwd","Je décris", "EUR", "project","Jean","Henri")
    #     self.click.click_on_a_link(By.CLASS_NAME,'backtolistecount')  

    #     # he clicks on parameters, a popup appears
    #     self.click.click_on_a_link(By.CLASS_NAME,"parameters")
    #     self.check_if_popup_displayed("parameters-options",True) 
        
    #     #He clicks on a JS button of the popup, an other popup replaces the previous one.
    #     self.click.click_on_a_link(By.CLASS_NAME, "conditions") 
    #     self.check_if_popup_displayed("parameters-options",False)
    #     self.check_if_popup_displayed("conditions-options",True)

    #     #He clicks on the link of the tricount and no popup is visible and he stays on the same page.
    #     self.click.click_on_a_link(By.CLASS_NAME,"link-tricount")

    #     popup_children = self.browser.find_elements(By.CSS_SELECTOR, "[data-div = hidden] > *")

    #     for elt in popup_children:
    #         self.assertEqual(elt.is_displayed(),False)
    #     self.assertEqual(self.browser.current_url, self.live_server_url + "/count")

    def test_JS_of_newcount_page(self): 

        #The client goes to the creation of a new count
        self.browser.get(self.live_server_url+ '/count')
        self.click.click_on_a_link(By.CLASS_NAME,'id_newcount')
        self.click.click_on_a_link(By.ID,'countfromzero')

        #He enters a title and a description, a counter appears and the number of letters corresponds to the length of the word.   
        titlebox,descriptionbox = self.click.find_multiple_elements(By.NAME,"newtricount_title","newtricount_description")
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

    def test_JS_currency_research_bar(self): 

        #The client creates a new count and begins to create a tricount.
        self.browser.get(self.live_server_url+ '/count')
        self.click.click_on_a_link(By.CLASS_NAME,'id_newcount')
        self.click.click_on_a_link(By.ID,'countfromzero')

        self.click.click_on_a_link(By.CLASS_NAME, "choose-currency")
        loupe = self.browser.find_element(By.CLASS_NAME, "currencyresearch") 
        self.assertEqual(loupe.is_displayed(),True) 

        #He clicks on the loop and the research bar appears.
        self.click.click_on_a_link(By.CLASS_NAME, "currencyresearch")
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
        self.click.click_on_a_link(By.CLASS_NAME, "backtonewcount")
        self.assertEqual(self.browser.current_url, self.live_server_url+ '/choosecurrency?referer=/newcount')

        #He clicks an other time to go back to newcount page.
        self.click.click_on_a_link(By.CLASS_NAME, "backtonewcount")
        self.assertEqual(self.browser.current_url, self.live_server_url+ '/newcount')


class TestChat(ChannelsLiveServerTestCase):

    def setUp(self):
        # Create a first user experience
        self.browser = webdriver.Firefox(options=options)
        self.browser.implicitly_wait(3)  
        click = user_experience.Click(self.browser, self.live_server_url)
        click.register_and_login_someone('toto', 'toto@gmail.com', '1234')
        click.create_a_tricount('tricount', '1234', 'description', 'EUR', 'trip', 'toto', 'marine')
        self.click = click
 
        # Create a second user experience and clone the previous tricount to access the same chat
        self.browser2 = webdriver.Firefox(options=options)
        self.browser2.implicitly_wait(3)  
        click2 = user_experience.Click(self.browser2, self.live_server_url)
        click2.register_and_login_someone('marine', 'm@gmail.com', '1234')
        click2.click_on_a_link(By.ID,'id_newcount')  
        click2.click_on_a_link(By.CLASS_NAME,"clonecount") 
        click2.clone_a_tricount('tricount', '1234')
        self.click2 = click2
    
    def tearDown(self):
        self.browser.quit()
        self.browser2.quit()

    def test_chat(self):
        # The user go to the chat application 
        self.click.click_on_a_link(By.CLASS_NAME, 'chat') 

        # The second user go to the tricount and see the message on the chat
        self.click2.click_on_an_existing_tricount(1)
        self.click2.click_on_a_link(By.CLASS_NAME, 'chat') 

        # The first user sends a message and sees it and the date
        self.click.post_chat_message('Ceci est mon premier message')
        message = self.browser.find_element(By.CSS_SELECTOR, ".owner-popup .text")
        dates = self.browser.find_elements(By.CLASS_NAME, 'daydate')
        self.assertEqual(message.text, 'Ceci est mon premier message')
        self.assertEqual(len(dates), 1)

        # The second user also sees it and the date
        message = self.browser2.find_element(By.CSS_SELECTOR, ".popup .text")
        dates = self.browser2.find_elements(By.CLASS_NAME, 'daydate')
        self.assertEqual(message.text, 'Ceci est mon premier message')
        self.assertEqual(len(dates), 1)

        # The second user sends an answer and sees his message. There is no new print of the date 
        self.click2.post_chat_message('Voici ma réponse.')
        message = self.browser2.find_element(By.CSS_SELECTOR, ".owner-popup .text")
        dates = self.browser2.find_elements(By.CLASS_NAME, 'daydate')
        self.assertEqual(message.text, 'Voici ma réponse.')
        self.assertEqual(len(dates), 1)

        # The first user also sees it
        message = self.browser.find_element(By.CSS_SELECTOR, ".popup .text")
        self.assertEqual(message.text, 'Voici ma réponse.')

        # He go back to the tricount informations and returns on the chat. Old messages are still there
        self.click.click_on_a_link(By.CLASS_NAME, 'backtospending')
        self.click.click_on_a_link(By.CLASS_NAME, 'chat')
        message1 = self.browser.find_element(By.CSS_SELECTOR, ".popup .text")
        message2 = self.browser.find_element(By.CSS_SELECTOR, ".owner-popup .text")
        self.assertEqual(message1.text, 'Voici ma réponse.')
        self.assertEqual(message2.text, 'Ceci est mon premier message')








    
        

         
        
        




