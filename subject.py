"""
Filename: subject.py
Author: Efrain Gomez Fajardo
Purpose: Definition of the Subject class
"""

from question import *

class Subject:
    """
    A topic that wants to be mastered
    """
    __name: str
    __summary: str
    __questions: list
    __score: int

    def __init__(self, response:dict):
        """
        Create a Subject based on the information 
        returned by the OpenAI API.
        """
        self.__questions = list()
        self.__name = input("What topic are you studying for? ")
        self.__summary = response["summary"]
        self.__score = 0
        for question in response["questions"]:
            self.__questions.append(MultipleChoice(question))

    def take_quiz(self) -> None:
        """
        Iterate through all the questions, allowing
        the user to answer and increase their score
        """
        if self.__score == len(self.__questions):
            print("You have answered all the questions correctly!")
            print("Would you like to retake the quiz? Y/N")
            choice = input("> ")
            if choice.upper() == "Y":
                self._reset()
        for question in self.__questions:
            question.answer()
        self._compute_score()

    def display_summary(self) -> None:
        """
        Shows the summary of the Subject
        """
        print(self.__summary)

    def _compute_score(self) -> None:
        """
        Calculates the total score by adding together
        all the questions that are correct.
        """
        score = 0
        for question in self.__questions:
            if question.get_result():
                score += 1
        self.__score = score

    def _reset(self) -> None:
        """
        Make the class back to the original stats
        """
        self.__score = 0
        for question in self.__questions:
            question.reset()

    # ---------------------------
    # OVERRIDING METHODS
    # ---------------------------
    def __str__(self) -> str:
        return f"Name: {self.__name}  Score: {self.__score}/{len(self.__questions)}"
