import psycopg2
from decouple import config


def connect_postgresql():
    global db, cursor
    db = psycopg2.connect(dbname=config("dbname"), user=config("user"), password=config("password"),
                          host=config("host"), port=config("port"))
    cursor = db.cursor()
    if cursor:
        print('Database successfully connected')


async def insert_sql(state):
    async with state.proxy() as data:
        cursor.execute(
            "INSERT INTO profiles_ordertour(tour_id,user_id,quantity,number,arranged_date) "
            "VALUES(%s,%s,%s,%s, CURRENT_DATE)",
            tuple(data.values()),
        )
    db.commit()


async def get_qr_code(qr_code):
    cursor.execute("""SELECT * FROM tour_tour WHERE qr_code = %s""", (qr_code,))
    tours = cursor.fetchone()
    return tours


async def get_category(category_id):
    cursor.execute("""SELECT name FROM tour_category WHERE id = %s""", (category_id,))
    category = cursor.fetchone()
    return category


async def get_guide(guide_id):
    cursor.execute("""SELECT name,surname FROM tour_guide WHERE id = %s """, (guide_id,))
    guide = cursor.fetchone()
    return guide


async def get_qr_code_tour(qr_code):
    cursor.execute("""SELECT id FROM tour_tour WHERE qr_code = %s""", (qr_code,))
    tour = cursor.fetchone()
    return tour


async def get_username_user(username):
    cursor.execute("""SELECT id FROM users_user WHERE username = %s""", (username,))
    user = cursor.fetchone()
    return user
