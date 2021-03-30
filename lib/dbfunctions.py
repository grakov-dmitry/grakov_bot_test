import sqlite3
import os
import datetime

connecntion = sqlite3.connect(str(os.getcwd()) + '\grakov_bot', check_same_thread=False)
cursor = connecntion.cursor()

def addUser(message):
    userId = message.from_user.id
    userFN = message.from_user.first_name
    userLN = message.from_user.last_name
    userName = message.from_user.username
    userIsbot = message.from_user.is_bot
    userLangCode = message.from_user.language_code
    userCanJoinGroups = message.from_user.can_join_groups
    userCanReadAllGroupMessages = message.from_user.can_read_all_group_messages
    userSuppInlineQueries = message.from_user.supports_inline_queries
    cursor = connecntion.cursor()

    #Chek user exsist
    sql = f"SELECT * FROM users WHERE id = {userId}"
    cursor.execute(sql)
    list = cursor.fetchall() 
    if (list):
        sql = (f"""
                UPDATE users 
                SET is_bot = '{userIsbot}', first_name = '{userFN}', last_name = '{userLN}', username = '{userName}', language_code = '{userLangCode}', 
                can_join_groups = '{userCanJoinGroups}', can_read_all_group_messages = '{userCanReadAllGroupMessages}', support_inline_queries = '{userSuppInlineQueries}'
                WHERE id = '{userId}'
                """)
        cursor.execute(sql)
        connecntion.commit()
    else:
        sql = "SELECT * FROM users"
        cursor.execute(sql)
        countUsersIds = len(cursor.fetchall()) + 1
        sql = (f"""INSERT INTO users
                    VALUES ('{countUsersIds}', '{userId}', '{userIsbot}', '{userFN}', 
                    '{userLN}', '{userName}', '{userLangCode}', '{userCanJoinGroups}', '{userCanReadAllGroupMessages}', '{userSuppInlineQueries}', false)""")
        cursor.execute(sql)
        connecntion.commit()

def botLogs(message):
    userId = message.from_user.id
    cursor = connecntion.cursor()
    sql = f"SELECT table_user_id FROM users WHERE id = {userId}"
    cursor.execute(sql)
    connecntion.commit()
    botUserId = str(cursor.fetchall()[0])[1:-2]
    messageText = message.text
    dateTime = str(datetime.datetime.now())[0:-7]
    messageText = messageText.replace('"', '')
    messageText = messageText.replace('\'', '')
    sql = "SELECT id FROM logs"
    cursor.execute(sql)
    countLogs = len(cursor.fetchall()) + 1
    sql = (f"""INSERT INTO logs
                    VALUES ('{countLogs}', '{userId}', '{botUserId}', '{messageText}', '{dateTime}')""")
    cursor.execute(sql)
    connecntion.commit()

def isUserAdmin(message):
    userId = message.from_user.id
    sql = f"SELECT is_admin FROM users WHERE id = {userId}"
    cursor.execute(sql)
    flagAdmin = str(cursor.fetchall()[0])[1:-2]
    if int(flagAdmin) == 1:
        return True
    else:
        return False

def getLogs():
    sql = f"SELECT logs.message, logs.date_time, users.first_name, users.last_name, users.username FROM logs LEFT JOIN users ON logs.bot_user_id = users.table_user_id ORDER BY logs.id DESC LIMIT 10"
    cursor.execute(sql)
    logsObj = cursor.fetchall()
    textLogs= "Последние 10 записей в логах: \n"
    for oneLog in logsObj:
        textLogs = textLogs + str(oneLog[1]) + ":\n" + str(oneLog[3]) + " " + str(oneLog[2]) + "(" + str(oneLog[4]) + "):\n'" + str(oneLog[0]) + "' \n\n"
    return textLogs

def getUserCity(userId):
    sql = f"SELECT user_city FROM users_cities WHERE user_id = {userId}"
    cursor.execute(sql)
    user_city = str(cursor.fetchall()[0])[2:-3]
    return user_city

def setNewCity(call):
    userId = call.from_user.id
    city = call.data
    userCity = getUserCity(userId)

    if (userCity):
        sql = (f"""
                UPDATE users_cities 
                SET user_city = '{city}'
                WHERE user_id = '{userId}'
                """)
        cursor.execute(sql)
        connecntion.commit()
    else:
        sql = (f"""INSERT INTO users_cities
                    VALUES ('{userId}', '{city}')""")
        cursor.execute(sql)
        connecntion.commit()