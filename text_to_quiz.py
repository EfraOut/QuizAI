"""
Filename: text_to_quiz.py
Author: Efrain Gomez Fajardo and Juan Zurita
Purpose: Functions that interact with the OpenAI API
"""

import openai

def get_openai_response(API_KEY:str, prompt:str) -> str:
  """
  Function which returns the Summary, Quiz and Answers to the Quiz
  Parameters: API_KEY, prompt which is the topic to summarize and quiz about
  Both need to be a string
  """
  
  openai.api_key = API_KEY
  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "The structure to follow is: Summary, Quiz, Answers to the Quiz. Make a bullet points summary of the text. Then make a 10 questions quiz with 4 options. Separate these 3 sections by '-----'. Also, never include the header for the different sections, just use the specified way of separating the 3 sections."
    },
    {
      "role": "user",
      "content": prompt
    }
  ],
  temperature=0,
  max_tokens=1024,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
  )
  return response.choices[0].message.content


def process_answer_api(response:str) -> dict:
    """
    Transform the information received from the API.
    The response looks like this:
    (Note: The normal response gives back 10 questions, this
    is an example that only uses 2 for simplicity)

    #############################################
    summary text
    -----
    question 1: question?
    a)
    b)
    c)
    d)
    \\n
    \\n
    question 2: question?
    a)
    b)
    c)
    d)
    \\n
    \\n
    -----
    1. answer question 1
    2. answer question 2
    ############################################ 

    The transformation will make it look like this:

    {
      summary: summary text,
      questions:
      [
        {
          question: question 1
          options: [a), b), c), d)]
          answer: answer question 1
        },
        {
          question: question 2
          options: [a), b), c), d)]
          answer: answer question 2
        },
      ],
    }
    """
    # Create the dictionary that is going to encompass everything.
    main_dict = dict()
    main_dict["questions"] = list()

    # This split results in the following:
    # parts = [
    #   [0]     summary text,
    #   [1]     question? a) b) c) d)\n\nquestion? a) b) c) d)\n\n
    #   [2]     1. answer1\n2. answer2\n
    #         ]
    parts = response.split("-----")
    summary = parts[0]
    questions = parts[1]
    answers = parts[2]

    # With this split, now we have:
    # answers = [1. n)answer1, 2. n)answer2]
    #      i =     0        1
    answers = answers.strip().split("\n")

    # This loop sanitizes the answers so the final results looks like:
    # answers = [n, n]
    #       i =  0  1
    for i in range(len(answers)):
      parts = answers[i].split(".")  # Remove the numeric part
      answer = parts[1]              # Get the answer part only
      answers[i] = answer[1]         # Add again to the list just the letter

    # Storing the summary to the dictionary
    main_dict["summary"] = summary

    # After this split, we have:
    # questions_and_answers = [
    #        [0]                question? a) b) c) d),
    #        [1]                question? a) b) c) d),
    #                         ]
    question_and_answer = questions.strip().split("\n\n")

    assert len(question_and_answer) == len(answers), "There is an unbalance between questions and answers"

    # Index loop through the new create list because
    # questions_and_answers[i] == answer[i]
    for i in range(0, len(question_and_answer)):

      # The new dictionary that will be added to the list on main_dict["questions"]
      question_dict = dict()

      # This split results in the following:
      # parts = [question?, a) b) c) d)]
      #     i =      0           1
      parts = question_and_answer[i].split("?")

      # Separate the question from the answers
      question = parts[0]
      options = parts[1]

      # Populating the newly created dictionary
      question_dict["question"] = question
      question_dict["options"]  = options
      question_dict["answer"]   = answers[i]

      # Add the new dictionary to the main dictionary
      main_dict["questions"].append(question_dict)
    
    # The new dictionary is now created
    return main_dict
