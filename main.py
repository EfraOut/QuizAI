"""
Filename: main.py
Author: Efrain Gomez Fajardo
Purpose: Where all the happy things come true
"""

from subject import *
from speech_to_text import *
from text_to_quiz import *
import json

#OpenAI API Key for GPT-3.5-turbo
API_KEY = """REPLACE WITH API KEY"""

class Program:
    __topics: list = list()
    __running = True

    def _display_menu(self) -> None:
        """
        Show to the user what they can do
        """
        print("Welcome to QuizAI!")
        print("Please select an option:")
        print("1. Review a subject")
        print("2. Add a subject")
        print("3. Remove a subject")
        print("4. Quit")

    def _get_option(self) -> str:
        """
        Get a proper answer from the user
        """
        return input("> ")

    def _perform_action(self, option: str) -> None:
        """
        Make the appropriate decision depending 
        on what the user specified.
        """
        match option:
            case "1":
                if len(self.__topics) != 0:

                    # Getting the correct subject from the user.
                    print("What do you want to study?")
                    for i in range(len(self.__topics)):
                        print(f"{i + 1} {self.__topics[i]}")
                    choice = int(input("> "))

                    # Making a decision on what to do
                    # with the selected subject.
                    subject = self.__topics[choice - 1]
                    print("Would you like to review the topic? Y/N")
                    choice = input("> ")
                    if choice.upper() == "Y":
                        subject.display_summary()
                    subject.take_quiz()
                else:
                    print("You don't have anything to review!")
                    print("Please add a subject first")

            case "2":
                print("You will be asked to record an audio")

                # Getting the input from the microphone
                # and sending it to the API.
                text = start_listening()
                print("Done recording...")
                print("Starting to communicate with OpenAI...")
                response = process_answer_api(get_openai_response(API_KEY, text))

                # Create an object based on the API response.
                subject = Subject(response)
                self.__topics.append(subject)

                # Storing to a JSON
                json_object = json.dumps(response, indent=4)
                with open(subject.__name, "w") as f:
                    f.write(json_object)

            case "3":
                pass

            case "4":
                self.__running = False
                print("Hope to see you again soon!")

            case _:
                print("Please select a valid option")

    def run(self) -> None:
        """
        Run the main program
        """
        while self.__running:
            self._display_menu()
            option = self._get_option()
            self._perform_action(option)


# Execute the program
if __name__ == "__main__":
    Program().run()
