from flask import Blueprint, jsonify, request
from .database import *
main = Blueprint('main', __name__)

@main.before_app_request
def setup():
    setupDatabase()

@main.route("/", methods=['GET'])
def home():
    data = {
        "title": "Hello World, from Flask!" 
    }
    return jsonify(data)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = userLogin(email, password)
        if user:
            message = {
                "status": "200",
                "Message": "User Login Successful"
            }
            return jsonify(message)

        message = {
            "status": "403",
            "Message": "Please enter the correct password"
        }
        return jsonify(message)
    
@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        user = {}
        user['email'] = data.get('email')
        user['password'] = data.get('password')
        user['fullName'] = data.get('fullName')
        user['qualification'] = data.get('qualification')
        user['dob'] = data.get('dob')

        confirmPassword = data.get('confirmPassword')

        if user['password'] != confirmPassword:
            data = {
                "status": "400",
                "Message": "Both the passwords should match!"
            }
            return jsonify(data)
        
        try:
            insertUser(user)
            data = {
                "status": "201",
                "Message": "Account is successfully created. Please login to continue."
            }
            return jsonify(data)
        except sqlite3.IntegrityError:
            data = {
                "status": "400",
                "Message": "The email is already in use!"
            }
            return jsonify(data)

@main.route('/user/dashboard/<int:userId>', methods = ['GET'])
def userDashboard(userId):
    with sqlite3.connect('instance/quizMasterDB.db') as con:
        cursor = con.cursor()
        cursor.execute(
            '''SELECT * FROM user WHERE id = ? ''', (userId,)
        )
        user = list(cursor.fetchone())
        userName = user[3]
        cursor.execute(
            '''SELECT COUNT(*) FROM score WHERE user_id = ? ''', (userId,)
        )
        queryResult = list(cursor.fetchone())
        quizAttempted = queryResult[0]
        cursor.execute(
            '''SELECT MAX(total_scored) FROM score WHERE user_id = ? ''', (userId,)
        )
        queryResult = list(cursor.fetchone())
        maxScored = queryResult[0]
        cursor.execute(
            '''SELECT AVG(total_scored) FROM score WHERE user_id = ? ''', (userId,)
        )
        queryResult = list(cursor.fetchone())
        avgScored = queryResult[0]
        cursor.execute(
            '''SELECT * FROM quiz '''
        )
        queryResult = cursor.fetchall()
        print(queryResult)
        quizDict = {}
        quizList = []
        for quiz in queryResult:
            quiz = list(quiz)
            quizDict['id'] = quiz[0]
            quizDict['chapterId'] = quiz[1]
            quizDict['dateOfQuiz'] = quiz[3]
            quizDict['totalScore'] = quiz[2]
            quizDict['timeDuration'] = quiz[4]
            quizDict['difficultyLevel'] = quiz[5]
            quizList.append(quizDict)
            quizDict = {}

    data = {
        "userName": userName,
        "quizAttempted": quizAttempted,
        "maxScored": maxScored,
        "avgScored": avgScored,
        "quizList": quizList
    }
    return jsonify(data)

