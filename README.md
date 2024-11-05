# Description of the project

The aim of the project was to create a tricount like application. Tricount is an application which allow to manage counts of groups of users in order to guarantee that everyone is spending the same amount of money. This application stores the spendings data but also offers a solution of payment to reach the equilibrium state where there is no credit any more. In its original version, this application contains chat rooms associated with tricounts. In this project, I have implemented the back-end mechanics with django to store data, the API to calculate the solution reaching the equilibrium in python, the chat application with django channels, the front-end to link the user experience in html, css, JS.

# Distinctiveness and Complexity

- **Calculation API**: The tricount application stores the information of tricounts, its participants, its associated spendings and amounts paid by each participant. But it also includes a calculation process which is treating these data to give to the participant the amount he already spent, how much he will have to pay to the others if the tricount was closed when he looks to the application, and how to get a spending solution to equilibrate the costs between all participants. This implies to create an application able to do this calculations after each spending or modification of a spending and to link this application with the django server (when a tricount, a spending is created : count/views.py). The application is written in calculation.py.

- **Use of an exterior API for currency conversion** : I have used in my code an external API to get the updated currency rate change between to given currencies. The API url is "https://api.freecurrencyapi.com/v1/latest". I use it in utils.py in the class CurrencyConversion which is called in count/views.py. I had to understand how to make a request with such an API to get the information needed.

- **Django channels for chat** : I have integrated a chat application inside the tricount application. For this purpose, I had to learn websocket protocol manipulation different from http one, how to handle it with django, how to modify my environment configuration to autorize the creation of channel layers with redis and to install the daphne server. I had to learn what is a channel, a channel layer, how to handle the messages sent and received with consumers/routing files in the server side and how to do the same with JS on the user side. I had also to learn how to make unitary tests for websockets thanks to WebsocketCommunicator and how to adapt my functional tests too.

- **Unitary and functional tests** : I have developped for this application an important series of unitary tests for server-side and functional tests for user side to verify each part of the application is working well. This was not requested for previous projects. This involves the learning of selenium for functional_tests and the use of different django adaptations of TestCase : StaticLiveServerTestCase and ChannelsLiveServerTestCase. This involves also the creation of frequently used methods to factorize these tests and make them more readable.

- **Test launcher** : I have also written a run_tests.py to launch my unitary tests and to choose what functional tests shoud be launched. To choose, you have to write the test classes names. To do so, I used Typer module to write prompts and create a command to run tests and subprocess modules to launch commands running the tests.

- **Size of the project** : This project has necessitated to write much more code than it was done in the other projects. This can be seen with the size of the project, its number of files. It contains two apps (count and chat) and two API (currency API and own-written calculation API).

# What is contained in each created file

- **chat folder** : 
    - consumers.py : Consumer handling the behaviour of the websocket server for receivung and sending messages in the chat app
    - models.py : model Chat to register every chat message
    - routing.py : the websocket url patterns authorizing connections the websocket server
    - tests.py : unitary tests for the chat app
    - urls.py : url for rendering the chat app
    - views.py : view associated with the url to render the chat.html page
- **count folder** :
    - calculation.py : contains the calculation application. This creates participants when a new tricount is created. It calculates total_cost of each participants, credits of participants towards others, credits of each participant to reach the equilibrium when a spending is registered. It also suggests a solution of payment in order to reach this equilibrium.
    - methods_for_tests.py : classes of methods to improve the readability of the code of tests.py.
    - tests.py : unitary tests for the count application
    - models.py : models to register counts and spending in the database
    - urls.py : urls for the count app
    - utils.py : classes of methods used in views.py. It allows currency conversions when the user choose different currencies of payment. It allows also to modify a tricount when a new spending happens or when participants are added to a tricount.
    - views.py : views for the count app
- **functional_tests** :
    - tests.py : functional_tests for Count and Chat app made with selenium
    - user_experience.py : two classes of methods useful in functional tests to improve readibility
- **templates, css, scss, js**:
    - Each html file is associated with its css style sheet and its JS file to handle the page behaviour.
    - chat.html/.css/.js : chat app page
    - layout.html : basic html for all pages
    - common.css : common css used in the majority of html pages
    - welcome.html/.js, login.css : page to welcome a new user and invite him to register
    - login.html/.css, welcome.js : page to login a registered user
    - logout.html/.css : page to log out a user
    - index.html/.css/.js : page listing the tricounts involving the user and allowing him to create tricounts or clone existing ones
    - newcount.html/.css/.js : page to create a new tricount
    - spending.html/.css : page listing the spendings created in a given tricount
    - newspending.html/.css/.scss/.js : page to create a newspending
    - spending-details.html/.css/.js : page to see the informations of a given spending
    - spending-equilibria.html/.css/.js : page to see the credits of each participant and a solution to reach the equilibrium between participants
    - currency.html/.css.js : page listing all available currencies     
    - modifycount.html/.css/.js : page to modify a given tricount, to add participants, change informations
    - modifyspending.html/.css/ newspending.js : page to modify a given spending, the amounts paid by each participant, informations.
- **images**: some logo used in the application
- **json**: contains currency.json listing all currencies and their acronym
- **.gitignore**: all files which are not included in the git repository
- **requirements.txt** : the configuration to be able to run the application
- **run_tests.py** : program to run unitary tests and to choose which functional_tests have to be run
- **steps.md** : personal todo file   

# How to run this application

## Install the application

You must have an environment with a Python >= 3.10
You must then install all packages of requirement.txt : `pip install requirements.txt`
This can be done after installing miniconda to create a python environment

`conda create --n nameenv python=3.10` 
`conda activate nameenv`
`pip install requirements.txt`

To handle websockets protocol, you must start a redis server which can be done installing docker.

## Run the servers

To lauch the redis server : `docker run -p 6379:6379 -d redis:5`

Once your environment is configured you must launch :

`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py runserver`

If python is installed in a conda environment : 

`conda activate nameenv`
`python manage.py makemigrations`
`python manage.py migrate`
`python manage.py runserver`

## Launch unitary tests

To launch count app unitary tests: `python manage.py test count`.
To launch chat app unitary tests: `python manage.py test chat`.

## Launch unitary tests and chosen functional tests

Run : `python run_tests.py`. You will be asked which classes of tests you want to include.

# Improvement et perspectives thanks to the EdX formation

I had begun this project before beginning your formation but your formation helped to improve the code in the following points:

- creation of html blocks to get a common html structure
- improvement of the JS code quality using more document.querySelector to avoid to create too many variable names, structuration of a JS file inspired from yours. 
- use of django url tags to avoid plain urls writting in files.

To see the improvement of the code, you can compare the actual code to the commit 09ac9ded132ddc7bc4d1e6480025236b5c7cb261

I also noticed future improvements I want to include in the project thanks to the formation:

- analysis of when a view shoud be a JS view not to load the entire page itself
- improve the security of the application by hashing passwords and put API keys in hidden variables
- integrate continuous integration process with a yaml file
- create a docker image to install this application 