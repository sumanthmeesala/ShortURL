import sqlite3

CREATE_USER_TABLE = '''
CREATE TABLE IF NOT EXISTS user (
	email       VARCHAR(30) PRIMARY KEY,
   	enPassword  VARCHAR(30) NOT NULL
)
'''
CREATE_USER = '''
INSERT INTO user(email, enPassword) values(?, ?);
'''
FIND_USER_BY_EMAIL_PASSWORD = '''
SELECT email
    FROM user
    WHERE email = ? AND enPassword = ?
'''


class UserRepository:
    def __init__(self):
        with sqlite3.connect('short-links-demo.db') as connection:
            connection.execute(CREATE_USER_TABLE)

    def createUser(self, email, enPassword) -> bool:
        with sqlite3.connect('short-links-demo.db') as connection:
            result = connection.execute(CREATE_USER, (email, enPassword))
            return result.rowcount == 1

    def isExistUserByEmailAndPassword(self, email, enPassword) -> bool:
        with sqlite3.connect('short-links-demo.db') as connection:
            result = connection.execute(FIND_USER_BY_EMAIL_PASSWORD, (email, enPassword))
            return len(result.fetchall()) == 1
