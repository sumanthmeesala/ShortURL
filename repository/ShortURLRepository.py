import sqlite3, datetime

CREATE_SHORT_URL_TABLE = '''
CREATE TABLE IF NOT EXISTS shortURL (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
	email       VARCHAR(30),
	label       VARCHAR(30),
	shortURL    VARCHAR(30) NOT NULL,
	actualURL   VARCHAR(100) NOT NULL,
	createdDate DATETIME default (datetime(current_timestamp)),
	expiryDate  DATETIME,
	accessCount INTEGER default 0,
   	enPassword  VARCHAR(30)
)
'''

INSERT_SHORT_URL = '''
INSERT INTO
    shortURL(id, email, label, shortURL, actualURL, createdDate, expiryDate, accessCount, enPassword)
    values(?, ?, ?, ?, ?, ?, ?, ?, ?)
'''

FIND_SHORT_URL_BY_EMAIL = '''
SELECT id, email, label, shortURL, actualURL, createdDate, expiryDate, accessCount
    FROM shortURL
    WHERE email == ?
'''
FIND_SHORT_URL_BY_ID = '''
SELECT id, email, label, shortURL, actualURL, createdDate, expiryDate, accessCount
    FROM shortURL
    WHERE id == ?
'''
FIND_SHORT_URL_BY_SHORT_URL = '''
SELECT id, email, label, shortURL, actualURL, createdDate, expiryDate, accessCount
    FROM shortURL
    WHERE shortURL == ?
'''
FIND_MAX_ID = '''
SELECT max(id) FROM shortURL
'''


class ShortURLRepository:
    def __init__(self):
        with sqlite3.connect('short-links-demo.db') as connection:
            connection.execute(CREATE_SHORT_URL_TABLE)

    def createSHORTURL(self, ID, email, label, shortURL, actualURL, expiryDays, enPassword) -> bool:
        with sqlite3.connect('short-links-demo.db') as connection:
            result = connection.execute(INSERT_SHORT_URL, (ID, email, label, shortURL, actualURL, datetime.datetime.now(), datetime.datetime.now() +
                                                           datetime.timedelta(days=expiryDays), 0, enPassword))
            return result.rowcount == 1

    def findShortURLByEmail(self, email):
        with sqlite3.connect('short-links-demo.db') as connection:
            result = connection.execute(FIND_SHORT_URL_BY_EMAIL, [email])
            return result.fetchall()

    def findShortURLByID(self, id: int):
        with sqlite3.connect('short-links-demo.db') as connection:
            result = connection.execute(FIND_SHORT_URL_BY_ID, [id])
            return result.fetchone()

    def findShortURLByShortURL(self, shortURL):
        with sqlite3.connect('short-links-demo.db') as connection:
            result = connection.execute(FIND_SHORT_URL_BY_SHORT_URL, [shortURL])
            return result.fetchone()

    def nextID(self):
        with sqlite3.connect('short-links-demo.db') as connection:
            result = connection.execute(FIND_MAX_ID).fetchone()
            return 1 if result[0] is None else result[0] + 1