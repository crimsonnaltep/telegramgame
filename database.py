# from sqlalchemy import create_engine, text, inspect
# from sqlalchemy import insert
# import pandas as pd
#
# config = {
#     "username": "root",
#     "password": "Tikobog666",
#     "hostname": "localhost",
#     "port": "3306",
#     "dbname": "telegramdb"
# }
#
#
# def connect_to_db():
#     engine = create_engine(
#         f'mysql+pymysql://{config["username"]}:{config["password"]}@{config["hostname"]}:{config["port"]}/{config["dbname"]}')
#     return engine
#
#
# def create_table(chat_id):
#     con = connect_to_db()
#     cursor = con.raw_connection().cursor()
#     if not check_table(chat_id):
#         cursor.execute(f'''
#                 CREATE TABLE players_{chat_id} (
#                     Username varchar(255),
#                     UserId varchar(255)
#                 );
#             ''')
#         cursor.execute(f'''
#                 CREATE TABLE games_{chat_id} (
#                     Username varchar(255),
#                     Date date
#                 );
#             ''')
#
#
# def reg_user(user_id, username, chat_id):
#     con = connect_to_db().connect()
#     cursor = connect_to_db().raw_connection().cursor()
#     cursor.execute(f"""
#             INSERT INTO players_{chat_id} (Username, UserId)
#             VALUES ('{username}', '{user_id}')
#         """)
#     con.commit()
#
#
# def get_players(chat_id):
#     con = connect_to_db()
#     cursor = con.raw_connection().cursor()
#     cursor.execute(f"SELECT * FROM players_{chat_id}")
#     results = cursor.fetchall()
#     print(results)
#
#
# def check_user(chat_id, user_id):
#     engine = connect_to_db()
#     players_table_exists = inspect(engine).has_table(f"players_{chat_id}")
#     if players_table_exists:
#         connection = engine.raw_connection()
#         cursor = connection.cursor()
#         cursor.execute(f"SELECT COUNT(*) FROM players_{chat_id} WHERE UserId = {user_id}")
#         results = cursor.fetchall()
#         if results:
#             print("there is a user")
#         else:
#             print("there is not a user")
#     else:
#         print("there is not a table")
#
#
# def check_table(chat_id):
#     con = connect_to_db()
#     cursor = con.raw_connection().cursor()
#     return cursor.execute(f"SHOW TABLES LIKE 'games_{chat_id}';")
#
#
# reg_user(1, 1, 1)
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
import pandas as pd
from datetime import datetime
import random

def connect_to_db():
    # todo вынемсти все креды в конфиг файл
    engine = create_engine(f'mysql+pymysql://root:Tikobog666@localhost:3306/telegramdb')
    return engine


def create_table(chat_id):
    # todo сделать отдельную функцию проверки наличия таблицы по аналогии с функцией ckeck_user
    engine = connect_to_db()
    Session = sessionmaker(bind=engine)
    session = Session()
    players_table_exists = inspect(engine).has_table(f"players_{chat_id}")
    games_table_exists = inspect(engine).has_table(f"games_{chat_id}")
    if not players_table_exists and not games_table_exists:
        players_table_query = text(f'''
                CREATE TABLE IF NOT EXISTS players_{chat_id} (
                    Username varchar(255),
                    UserId varchar(255)
                );
            ''')

        games_table_query = text(f'''
                CREATE TABLE games_{chat_id} (
                    UserId varchar(255),
                    Date date
                );
            ''')
        session.execute(players_table_query)
        session.commit()  # Commit after each execution if auto-commit is not enabled
        session.execute(games_table_query)
        session.commit()


def reg_user(user_id, username, chat_id):
    if not check_user(chat_id, user_id):
        engine = connect_to_db()
        with engine.connect() as connection:
            registration_user = text(f"""
                INSERT INTO players_{chat_id} (Username, UserId)
                VALUES ('{username}', '{user_id}');
            """)
            Session = sessionmaker(bind=engine)
            session = Session()
            session.execute(registration_user)
            session.commit()
        return("Добро пожаловать в гей клуб !")
    else:
        # todo писать это сообщение в чат
        return("Ты уже зареган чмо тупое")


def get_players(chat_id):
    engine = connect_to_db()
    sql_query = f"""SELECT distinct UserId FROM players_{chat_id}"""
    result_df = pd.read_sql(sql=sql_query, con=engine)

    return result_df['UserId'].values


def check_user(chat_id, user_id):
    players = get_players(chat_id)
    if str(user_id) in players:
        return True
    else:
        return False


def select_winner(chat_id):
    players = get_players(chat_id)
    return random.choice(players)


def get_username_by_id(user_id, chat_id):
    con = connect_to_db()
    cursor = con.raw_connection().cursor()
    cursor.execute(f"SELECT Username from players_{chat_id} WHERE UserId = {user_id}")
    result = cursor.fetchall()

    return result[0][0]


def add_winner(chat_id):
    winnerId = select_winner(chat_id)
    today = datetime.now()
    winningTime = today.strftime("%Y-%m-%d")
    winnerUsername = get_username_by_id(winnerId, chat_id)
    engine = connect_to_db()
    with engine.connect() as connection:
        adding_winner = text(f"""
                    INSERT INTO games_{chat_id} (UserId, Date)
                    VALUES ('{winnerId}', TIMESTAMP('{winningTime}'));
                """)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.execute(adding_winner)
        session.commit()
    return winnerUsername


def get_dates(chat_id):
    engine = connect_to_db()
    sql_query = f"""SELECT distinct Date FROM games_{chat_id}"""
    result_df = pd.read_sql(sql=sql_query, con=engine)

    return result_df['Date'].values



def winner_by_date(chat_id, date):
    engine = connect_to_db()
    sql_query = f"""SELECT UserId FROM games_{chat_id} WHERE Date = TIMESTAMP('{date}')"""
    result_df = pd.read_sql(sql=sql_query, con=engine)

    return get_username_by_id(result_df['UserId'].values[0], chat_id)

def getWinnerTable(chat_id):
    engine = connect_to_db()
    sql_query_winners = f"""SELECT UserId FROM games_{chat_id}"""
    result_df_winners = pd.read_sql(sql=sql_query_winners, con=engine)

    return result_df_winners.values


def getPlayersTable(chat_id):
    engine = connect_to_db()
    sql_query_users = f"""SELECT DISTINCT UserId FROM players_{chat_id}"""
    result_df_players = pd.read_sql(sql=sql_query_users, con=engine)

    return result_df_players.values


def showWinningCount(chat_id):
    players = getPlayersTable(chat_id)
    winners = getWinnerTable(chat_id)
    engine = connect_to_db()
    sql_query = f"""SELECT UserId, COUNT(*) FROM games_{chat_id} GROUP BY UserId ORDER BY COUNT(*) DESC"""
    result_df = pd.read_sql(sql=sql_query, con=engine)

    return result_df.values

print(winner_by_date("4108565981", "2024-03-26"))