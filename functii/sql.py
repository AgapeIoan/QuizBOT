import json

from mysql.connector import connect, Error

with open("storage/configs/sql.json", "r", encoding='utf-8') as f:
    SQL_CONFIG = json.load(f)

def connect_to_db():
    try:
        connection = connect(
            host=SQL_CONFIG["host"],
            user=SQL_CONFIG["user"],
            password=SQL_CONFIG["password"],
            database=SQL_CONFIG["database"]
        )
        return connection
    except Error as e:
        print(e)

# INSERT INTO `data` 
# (`int_id`, `discord_uid`, `question_number`, `answer_number`, `total`) 
# VALUES 
# (NULL, 'discord_uid', 'question_number', 'answer_number', 'total+1 or 1')

def send_data_to_db(discord_uid, question_number, answer_number):
    connection = connect_to_db()
    cursor = connection.cursor(buffered=True)

    query = f"SELECT * FROM `data` WHERE `discord_uid` = {discord_uid} AND `question_number` = {question_number} AND `answer_number` = '{answer_number}'"
    cursor.execute(query)
    if cursor.fetchone():
        query = f"UPDATE `data` SET `total` = `total` + 1 WHERE `discord_uid` = '{discord_uid}' AND `question_number` = '{question_number}' AND `answer_number` = '{answer_number}'"
    else:
        query = f"INSERT INTO `data` (`int_id`, `discord_uid`, `question_number`, `answer_number`, `total`) VALUES (NULL, '{discord_uid}', '{question_number}', '{answer_number}', '1')"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

def read_answered_questions(discord_uid):
    connection = connect_to_db()
    cursor = connection.cursor(buffered=True)

    query = f"SELECT DISTINCT `question_number` FROM `data` WHERE `discord_uid` = '{discord_uid}'"
    cursor.execute(query)
    answered_questions = cursor.fetchall()
    cursor.close()
    connection.close()

    return answered_questions
    