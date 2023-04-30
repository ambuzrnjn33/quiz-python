from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Connect to the MongoDB database
client = MongoClient()
db = client.devops_quiz

# Define the home page route
@app.route('/')
def index():
    return render_template('index.html')

# Define the quiz page route
@app.route('/quiz')
def quiz():
    questions = db.questions.find()
    return render_template('quiz.html', questions=questions)

# Define the quiz results route
@app.route('/results', methods=['POST'])
def results():
    # Get the user's answers from the request data
    user_answers = request.get_json()

    # Calculate the user's score and proficiency level
    num_questions = db.questions.count_documents({})
    num_correct = 0
    results = {}
    for question, answer in user_answers.items():
        correct_answer = db.questions.find_one({'question': question})['answer']
        if answer == correct_answer:
            num_correct += 1
            results[question] = 'Correct'
        else:
            results[question] = 'Incorrect'
    score = num_correct / num_questions * 100
    if score >= 90:
        proficiency = 'Expert'
    elif score >= 70:
        proficiency = 'Proficient'
    elif score >= 50:
        proficiency = 'Intermediate'
    else:
        proficiency = 'Novice'

    # Return the quiz results as a JSON response
    return jsonify({
        'score': score,
        'num_questions': num_questions,
        'proficiency': proficiency,
        'results': results
    })

if __name__ == '__main__':
    app.run(debug=True)
