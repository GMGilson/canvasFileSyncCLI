# builtins
from os import path, makedirs
import json
from pprint import pprint
# externs
import inquirer
from pyfiglet import Figlet
from inquirer.themes import GreenPassion

# src
from src import manifest


def run():
    welcomePrompt = Figlet(font="slant")
    print(welcomePrompt.renderText("Canvas File Sync"))

    if not path.exists("config/userConfig.json"):
        firstTimeSetUp()

    while mainMenue():
        pass

    exit(0)


def firstTimeSetUp():
    """
    Generate a user config file for first-time setup
    """
    print("No user config found. Running first time setup")
    
    questions = [
        inquirer.Path(
            name="rootLocation",
            message="Where would you like canvas sync's root store location to be? (Absolute Paths Please)",
            normalize_to_absolute_path=True
        )
    ]

    answers = inquirer.prompt(questions, theme=GreenPassion())
    
    if not path.exists(filePath := answers["rootLocation"]):
        makedirs(filePath)

    with open("config/userConfig.json", 'w') as config:
        json.dump(answers, config)

def mainMenue() -> int:
    questions = [
        inquirer.List(
            name="Menue Select",
            message="I want to:",
            choices=[
                "1) Select courses/files to be tracked",
                "2) Exit"
            ]
        )
    ]

    answer = inquirer.prompt(questions, theme=GreenPassion())["Menue Select"]

    if "1" in answer:
        editTracking()
        return 1

    if "2" in answer:
        print("Bye!")
        return 0
    
    

def editTracking():

    client = manifest.Client()
    tracking = client.loadManifest("config/manifest.json")
    pprint("Updating file indices from Canvas. (This may take some time)")
    latest = client.generateManifest()

    courses = ["Exit"]
    courses.extend([f"{latest[courseId]['courseName']} ({courseId})" for courseId in latest.keys()])

    while True:
        questions = [
            inquirer.Checkbox(
                name='courses',
                message="Select courses you would like to modify. Space to select, Enter to confirm selections",
                choices= courses
            )
        ]
        selections = inquirer.prompt(questions, theme=GreenPassion())

        if "Exit" in selections["courses"]:
            break


def editCourseTracking(course: str, tracking, manifest):
    pass