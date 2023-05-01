from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
import logging
from random import shuffle

app = Flask(__name__)
load_dotenv()

app.config['MONGO_URI'] = os.getenv('MONGODB_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
mongo = PyMongo(app)

logging.basicConfig(level=logging.DEBUG)

def get_correct_answers():
    correct_answers = {}
    for question in mongo.db.questions.find():
        correct_answers[question['question']] = question['answer']
    return correct_answers

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    questions = list(mongo.db.questions.find())
    shuffle(questions)
    for question in questions:
        shuffle(question['options'])
    return render_template('quiz.html', questions=questions)
#def quiz():
#    questions = list(mongo.db.questions.find())
#    return render_template('quiz.html', questions=questions)

@app.route('/results', methods=['POST'])
def results():
    quiz_response = request.get_json()
    correct_answers = get_correct_answers()

    if len(quiz_response) == 0:
        return "Error: No quiz responses received."

    num_questions = len(quiz_response)
    num_correct = 0
    results = {}

    for question, answer in quiz_response.items():
        if answer == correct_answers.get(question):
            num_correct += 1
            results[question] = "Correct"
        else:
            results[question] = "Incorrect"

    score = float(num_correct) / num_questions * 3.0
    proficiency_levels = {
        (0.0, 1.0): "Novice",
        (1.0, 2.0): "Intermediate",
        (2.0, 3.0): "Expert"
    }
    proficiency = ""
    for level, description in proficiency_levels.items():
        if score >= level[0] and score < level[1]:
            proficiency = description

    response = {
        "num_questions": num_questions,
        "score": score,
        "proficiency": proficiency,
        "results": results
    }

    logging.info(f"Quiz response: {quiz_response}")
    logging.info(f"Correct answers: {correct_answers}")
    logging.info(f"Num questions: {num_questions}")
    logging.info(f"Num correct: {num_correct}")
    logging.info(f"Results: {results}")
    logging.info(f"Score: {score}")
    logging.info(f"Proficiency: {proficiency}")
    logging.info(f"Response: {response}")

    return render_template('results.html', **response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

