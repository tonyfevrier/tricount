#File to run functional tests after executing scss compiler
import subprocess
import typer
import re
import os
import django
import ast 
 
from django.core.files.storage import default_storage

PATH_SCSS = "/Users/LCI/Documents/Developpement info/code python/tricount/static/scss"
  

# out of manage.py, we have to tell django where are the settings in order to use django specificities
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tricount.settings')
django.setup()

#CLASSES = get_classes_names('functional_tests/tests.py') #list of classes names in functional tests.
app = typer.Typer()
commands = []
filename = "functional_tests/tests.py"  


@app.command()
def run():
    """
    Command launching functional tests
    """
    classnames = askArgumentUntilNone()

    #if the user does not enter a classname, he wants to test all classes
    if not classnames:
        classnames = get_classes_names(filename)
     
    commands = compile_scss()
    commands = commands_for_unit_tests()
    commands = commands_for_functionals_tests(*classnames) 
    execute_process(commands)
 


def compile_scss():
    """
    Function creating commands to compile all scss files into css ones
    """ 
    folder = "static/scss"
    _,filenames = default_storage.listdir(PATH_SCSS) 
    for filename in filenames:
        # Compile with sass all scss files 
        if re.findall(r'.+\.scss$', filename):  
            commands.append(['C:\Programs\dart-sass\sass.BAT',f"{folder}/{filename}", re.sub("scss", "css", f"{folder}") + re.sub(".scss",".css",f"/{filename}")])
    return commands
    

def get_classes_names(filename):
    """
    Given a file, this function gets all names of classes in this file

    Input : 
        - filename(str)

    Output : 
        - class_names(list(str))
    """
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)

    class_names = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    return class_names


def get_methods_names(filename,*classnames):
    """
    Given a file and a name class, this function gets all names of methods in this file.

    Inputs:
        - filename(str)
        - classnames(list[str])

    Output:
        - methods_names(dict): dictionary whose keys are classnames and values are
            corresponding method names.
    """
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)
    
    methods_names = {}
    for classname in classnames:
        #get all methods nodes children of the parent class node
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == classname:
                methods_names[classname] = [subnode.name for subnode in ast.iter_child_nodes(node) if isinstance(subnode,ast.FunctionDef)]
                methods_names[classname].remove('setUp')
                methods_names[classname].remove('tearDown')
                break
    return methods_names

def commands_for_unit_tests():
    commands.append(['python', 'manage.py','test', 'count'])
    return commands

def commands_for_functionals_tests(*classnames):
    """
    Function creating commands to launch functional tests

    Input: 
        - classnames(list[str])
    """ 
    methods_names = get_methods_names(filename,*classnames)
    for classname in methods_names.keys():
        for method_name in methods_names[classname]:
            commands.append(['python','manage.py','test',f'functional_tests.tests.{classname}.{method_name}'])
    return commands


def askArgumentUntilNone():
    """
    Function asking the user to enter the classes names whose tests should be launched. 

    Output:
        - classnames (list[str]). 
    """ 
    classnames = []
    argument = typer.prompt('Enter a name of a test class you want to launch. To launch all the tests, press Enter',default = "")
    while argument: 
        classnames.append(argument)
        argument = typer.prompt('Enter a name of an other class you want to launch or press Enter',default = "")
    return classnames


def execute_process(commands):
    # Liste pour stocker les objets Popen de chaque sous-processus
    processus = []
 
    # Création des sous-processus pour chaque commande
    for command in commands: 
        print(" ".join(command))
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processus.append(process)
        stdout, stderr = process.communicate() 
        print("STDOUT:", stdout.decode())
        print("STDERR:", stderr.decode())

    # Attente de l'interruption du clavier (Ctrl+C)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        # Fermeture des processus
        for p in processus:
            p.terminate()

 
if __name__ == "__main__": 
    app()
 



