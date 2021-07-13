import psycopg2
from psycopg2 import Error

try:
    # Подключение к существующей базе данных
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="123456",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="chat_bot")

    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()
    # Распечатать сведения о PostgreSQL
    #print("Информация о сервере PostgreSQL")
    #print(connection.get_dsn_parameters(), "\n")
    # Выполнение SQL-запроса
    #cursor.execute("SELECT version();")
    # Получить результат
    #record = cursor.fetchone()
    #print("Вы подключены к - ", record, "\n")

    #create_table = 'CREATE TABLE urls_(ID INT PRIMARY KEY, URLS TEXT, res INT);'
    create_table = 'CREATE TABLE links(ID INT, URLS TEXT, res INT);'

    #cursor.execute(create_table)
    #connection.commit()
    #print("Таблица успешно создана в PostgreSQL")


    def cheking(url):
        check_qu = "SELECT URLS FROM links"
        cursor.execute(check_qu)
        qu = cursor.fetchall()
        for i in qu:
            link = str(''.join(map(str, i)))
            print(link)

    def insert(id, url, result):
        insert_qu = "INSERT INTO links(ID, URLS, res) VALUES(%s, %s, %s) RETURNING id;"
        cursor.execute(insert_qu, (id, url, result))
        connection.commit()
        print("1 запись успешно вставлена")

    cheking('https://www.youtube.com/')
    #insert(8005655,'https://www.youtube.com/',291)





    #insert(121212, 'youtube', 140)
    def check_url(link):
        check = "SELECT res FROM links WHERE URLS = %s"
        cursor.execute(check, (link,))
        c = cursor.fetchall()
        for i in c:
            l = str(''.join(map(str, i)))
            if l == link:
                return False
            return True

    #check_url('https://www.youtube.com/')

    #check_url('youtube')
    '''
    check = "SELECT res FROM urls_ WHERE URLS = %s"
    cursor.execute(check, ('youtub',))
    c = cursor.fetchall()
    for i in c:
        l = int(''.join(map(str, i)))
        print(type(l))
    '''
    '''
    check = "SELECT res FROM URL WHERE URLS = %s"
    cursor.execute(check, ('https://www.youtube.com/',))
    c = cursor.fetchall()
    for i in c:
        l = str(''.join(map(str, i)))
        print(l)

    '''









except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        #cursor.close()
        #connection.close()
        print("Соединение с PostgreSQL закрыто")



