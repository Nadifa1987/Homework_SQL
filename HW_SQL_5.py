import psycopg2

def create_db():
    with conn.cursor() as cur:
        cur.execute("""
             CREATE TABLE IF NOT EXISTS clients(
                 client_id serial PRIMARY KEY,
                 first_name TEXT NOT NULL,
                 last_name TEXT NOT NULL,
                 email varchar(100) UNIQUE
                 );""")

        cur.execute('''CREATE TABLE IF NOT EXISTS phone(
                 phones_id serial PRIMARY KEY,
                 phones varchar(60) UNIQUE,
                 client_id integer REFERENCES clients(client_id)
                 );''')

        print('Таблицы созданы')

# Добавить телефон клиенту
def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO phone(client_id,phones) 
        VALUES(%s, %s);""",(client_id, phone))

    print('Телефон добавлен!')

# Добавить нового клиента
def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO clients(first_name, last_name, email)
        VALUES(%s, %s, %s) RETURNING client_id;""", (first_name, last_name, email))
        list_id = list(cur.fetchone())
        # print(list_id)
        if phones != None:
            client_id = list_id[0]
            add_phone(conn,client_id, phones)
    print('Клиент добавлен!')

# Изменение данных клиента
def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    if first_name != None:
        with conn.cursor() as cur:
            cur.execute("""UPDATE clients SET first_name=%s
            WHERE client_id = %s;""", (first_name,client_id))
    if last_name != None:
        with conn.cursor() as cur:
            cur.execute("""UPDATE clients SET last_name=%s
            WHERE client_id = %s;""", (last_name, client_id))
    if email != None:
        with conn.cursor() as cur:
            cur.execute("""UPDATE clients SET email=%s
            WHERE client_id = %s;""", (email, client_id))
    if phones != None:
        delete_phone(conn, client_id)
        add_phone(conn,client_id, phones)
    with conn.cursor() as cur:
        cur.execute("""SELECT * FROM clients as cl 
            LEFT JOIN phone as pn ON cl.client_id = pn.client_id
            WHERE cl.client_id = %s;""", (client_id,))
        print(f'Новые данные клиента: client update {cur.fetchone()}')

# Удалить телефон клиента
def delete_phone(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone WHERE client_id = %s;""", (client_id,))

    print('Телефон удален!')

# Удалить клиента
def delete_client(conn, client_id):
    delete_phone(conn, client_id)
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM clients WHERE client_id = %s;""",(client_id,))
    print('Клиент удален!')

# Найти данные клиента по его имени, фамилии, почте, телефону
def find_client(conn, **values):
    for key, value in values.items():
        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM clients as c 
                LEFT JOIN phone as p ON c.client_id = p.client_id 
                WHERE {key} = '{value}'
        """)
            print('Данные клиента: ', (cur.fetchone()))


with psycopg2.connect(database="client_db", user="postgres", password="") as conn:
    # pass  # вызывайте функции здесь
    # create_db()
    # add_client(conn,'Курочкин', 'Вася','курочкин@example.com','89262223344')
    # add_client(conn, 'Курочкина', 'Света', 'курочка@example.com', '89265556622')
    # add_client(conn, 'Серегин', 'Игнат', 'игнат@example.com', '89778888888')
    # add_client(conn, 'Лапухова', 'Ира', 'лапира@example.com', '89167771112')
    # add_client(conn, 'Свистулькин', 'Максим', 'макс@example.com')
    # add_client(conn, 'Solovey', 'Sergey', 'solovey@example.com', '8926223333')
    # add_phone(conn, '6', '8945557777')
    # add_phone(conn, '3', '84953333555')
    # change_client(conn, '6', last_name ='Игоречек', phones = '89261111111')
    # change_client(conn, '2', first_name ='Некурочкинабольше')
    # delete_phone(conn, '3')
    # delete_client(conn, '4')
    # find_client(conn, email='игнат@example.com')

conn.close()