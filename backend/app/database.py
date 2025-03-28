import sqlite3
def setupDatabase():
    with sqlite3.connect('instance/quizMasterDB.db') as con:
        #USER table
        con.execute('''
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                qualification TEXT NOT NULL,
                dob DATE,
                is_admin BOOLEAN DEFAULT FALSE     
            )
        ''')
        #ADMIN account creation
        cursor = con.cursor()
        cursor.execute(
            '''SELECT * FROM user WHERE email = "quizmaster@goquizing.com"'''
        )
        admin = cursor.fetchone()
        if not admin:
            con.execute('''
                INSERT INTO USER ("email", "password", "full_name", "qualification", "dob", "is_admin")
                VALUES("quizmaster@goquizing.com", "admin123", "Quiz Master", "Quiz Master Pro", '2001-07-10', 1)
            ''')
        #SUBJECT table
        con.execute('''
            CREATE TABLE IF NOT EXISTS subject (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                desc TEXT NOT NULL    
            )
        ''')
        #CHAPTER table
        con.execute('''
            CREATE TABLE IF NOT EXISTS chapter (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                desc TEXT NOT NULL      
            )
        ''')
        #QUIZ table
        con.execute('''
            CREATE TABLE IF NOT EXISTS quiz (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chapter_id INTEGER NOT NULL,
                date_of_quiz DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_score INTEGER NOT NULL,
                time_duration TIME NOT NULL,
                difficulty_level TEXT NOT NULL,
                FOREIGN KEY(chapter_id) REFERENCES chapter(id)
            )
        ''')
        #QUESTION table
        con.execute('''
            CREATE TABLE IF NOT EXISTS question (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER NOT NULL,
                question_statement TEXT NOT NULL,
                option1 TEXT NOT NULL,
                option2 TEXT NOT NULL,
                correct_option TEXT NOT NULL CHECK(correct_option IN ('option1', 'option2')),
                FOREIGN KEY(quiz_id) REFERENCES quiz(id)
            )
        ''')
        #SCORE table
        con.execute('''
            CREATE TABLE IF NOT EXISTS score (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quiz_id INTEGER REFERENCES quiz(id),
                user_id INTEGER REFERENCES user(id),
                timestamp_of_attempt DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_scored INTEGER NOT NULL
            )
        ''')
        con.commit()

def userLogin(email, password):
    with sqlite3.connect('instance/quizMasterDB.db') as con:
        cursor = con.cursor()
        cursor.execute(
            '''SELECT * FROM user WHERE email = ? AND password = ? ''', (email,password)
        )
    return cursor.fetchone()

def insertUser(user):
    with sqlite3.connect('instance/quizMasterDB.db') as con:
        cursor = con.cursor()
        cursor.execute(
            '''INSERT INTO user ("email", "password", "full_name", "qualification", "dob") VALUES (?, ?, ?, ?, ?)''',(user['email'], user['password'], user['fullName'], user['qualification'], user['dob'])
        )
    con.commit()

def getUserById(userId):
    with sqlite3.connect('instance/quizMasterDB.db') as con:
        cursor = con.cursor()
        cursor.execute(
            '''SELECT * FROM user WHERE id = ? ''', (userId,)
        )
    return cursor.fetchone()

def getQuiz():
    with sqlite3.connect('instance/quizMasterDB.db') as con:
        cursor = con.cursor()
        cursor.execute(
            '''SELECT * FROM quiz '''
        )
    return cursor.fetchall()