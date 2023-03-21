import psycopg2
from decouple import config

global db, cursor


def connect_postgresql():
    global db, cursor
    db = psycopg2.connect(
        dbname=config("dbname"),
        user=config("user"),
        password=config("password"),
        host=config("host"),
        port=config("port"),
    )
    cursor = db.cursor()
    if cursor:
        print("Database successfully connected")


async def insert_sql_app(data):
    cursor.execute(
        "INSERT INTO profiles_ordertour(tour_id,user_id) " "VALUES(%s,%s)",
        data,
    )
    db.commit()


async def insert_sql_state_app(state):
    cursor.execute(
        "INSERT INTO profiles_ordertour(quantity,number,arranged_date) "
        "VALUES(%s,%s, CURRENT_DATE)",
        tuple(state.values()),
    )
    db.commit()


async def get_tour_id_app(id_):
    cursor.execute("""SELECT * FROM tour_tour WHERE id = %s""", (id_,))
    tours = cursor.fetchone()
    return tours


async def get_actual_limit(tour_id):
    cursor.execute("""SELECT actual_limit FROM tour_tour WHERE id = %s""", (tour_id,))
    tours = cursor.fetchone()
    if tours[0] is None:
        tours = 0
        return tours
    return tours[0]


async def get_quantity_limit(tour_id):
    cursor.execute("""SELECT quantity_limit FROM tour_tour WHERE id = %s""", (tour_id,))
    tours = cursor.fetchone()
    return tours[0]


async def update_actual_limit(quantity, tour_id):
    cursor.execute(
        "UPDATE tour_tour SET actual_limit = %s WHERE id = %s ", (quantity, tour_id)
    )
    db.commit()


async def insert_sql(state):
    async with state.proxy() as data:
        cursor.execute(
            "INSERT INTO profiles_ordertour(tour_id,user_id,quantity,number,way_of_payment,payment,arranged_date) "
            "VALUES(%s,%s,%s,%s,%s,%s ,CURRENT_DATE)",
            tuple(data.values()),
        )
    db.commit()


async def get_qr_code(qr_code):
    cursor.execute("""SELECT * FROM tour_tour WHERE qr_code = %s""", (qr_code,))
    tours = cursor.fetchone()
    return tours


async def get_qr_code_tour(qr_code):
    cursor.execute("""SELECT id FROM tour_tour WHERE qr_code = %s""", (qr_code,))
    tour = cursor.fetchone()
    return tour


async def get_tour_title(qr_code):
    cursor.execute("""SELECT title FROM tour_tour WHERE id = %s""", (qr_code,))
    tour = cursor.fetchone()
    return tour


async def get_tour_price(qr_code):
    cursor.execute("""SELECT price FROM tour_tour WHERE id = %s""", (qr_code,))
    tour = cursor.fetchone()
    return tour[0]


async def get_tour(id):
    cursor.execute("""SELECT id FROM tour_tour WHERE qr_code = %s""", (id,))
    tour = cursor.fetchone()
    return tour


async def get_username_user(username):
    cursor.execute("""SELECT id FROM users_user WHERE username = %s""", (username,))
    user = cursor.fetchone()
    return user


async def get_username(username):
    cursor.execute("""SELECT username FROM users_user WHERE id = %s""", (username,))
    user = cursor.fetchone()
    return user
