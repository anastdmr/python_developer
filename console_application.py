import sqlite3


def main():
    conn = sqlite3.connect ('library.db') #присоединение к базе данных
    cur = conn.cursor()#курсор базы данных (далее БД)
    cur.execute('''create table if not exists LIBRARY (ID integer PRIMARY KEY NOT NULL,
                                        TITLE text, AUTHOR text,
                                        YEARS integer, STATUS text)''')

    m = 0 #type: int
    while m != 6:
        print ("Меню:")
        print("0. Создать базу данных.")
        print ("1. Добавить книгу.")
        print("2. Удалить книгу.")
        print("3. Найти книгу.")
        print("4. Показать все книги библиотеки.")
        print("5. Изменить статус книги.")
        print("6. Выйти.")
        m = int(input("Выберите действие, которое вы хотите выполнить:"))#type: int
        if m == 1:
            add_book()
        elif m == 2:
            del_book()
        elif m == 3:
            find_book()
        elif m ==4:
            print_lib()
        elif m == 5:
            update_status()
        elif m == 0:
            create_db()
        elif m == 6:
            print ("До свидания!")
            break



    conn.commit() #для сохранения всех изменений
    conn.close() #закрытие БД

def add_book() -> str:
    conn = sqlite3.connect('library.db')  # присоединение к базе данных
    cur = conn.cursor()  # курсор базы данных (далее БД)
    title_input = input("Введите название книги: ")
    author_input = input("Введите автора книги:")
    year_input = int(input("Введите год написания книги:"))
    cur.execute('''insert into LIBRARY (TITLE, AUTHOR, YEARS, STATUS)
                        values (?, ?, ?, "в наличии")''',
                        (title_input,author_input,year_input))
    conn.commit()  # для сохранения всех изменений
    conn.close()  # закрытие БД
    write_DB()
    return print ("Книга добавлена!")

def del_book():
    conn = sqlite3.connect('library.db')  # присоединение к базе данных
    cur = conn.cursor()  # курсор базы данных (далее БД)
    id_input = int(input("Введите ID книги, которую хотите удалить:")) #type: int
    cur.execute('''select ID from LIBRARY where ID == ?''', (id_input,))
    result_id = cur.fetchall() #type: list
    if result_id is not None:
        cur.execute('''delete from LIBRARY where ID == ?''', (id_input,))
    else:
        print("Книги с таким ID нет в библиотеке!")
    conn.commit()  # для сохранения всех изменений
    conn.close()  # закрытие БД
    write_DB()
    return print("Книга удалена!")

def find_book():
    conn = sqlite3.connect('library.db')  # присоединение к базе данных
    cur = conn.cursor()  # курсор базы данных (далее БД)
    print ("По какому критерию будет выполняться поиск:")
    print ("1 - по названию книги;")
    print("2 - по автору;")
    print("3 - по году написания?")
    print("Введите нужную цифру:")
    n = int(input()) #type: int
    if n == 1:
        find_title = input("Введите искомое название: ").lower() #type: str
        cur.execute('''select * from LIBRARY where lower(TITLE) like ?''', ('%'+find_title[1:]+'%',))
        tit = cur.fetchone() #type: list
        if tit is not None:
            #print(' ID TITLE                    AUTHOR           YEAR STATUS')
            print(f'{tit[0]:2} {tit[1]:25} {tit[2]:15} {tit[3]:5} {tit[4]:15}')
        else:
            print ("Книги с таким названием нет в библиотеке!")
    elif n == 2:
        find_author = input("Введите искомого автора: ").lower() #type: str
        cur.execute('''select * from LIBRARY where lower(AUTHOR) like ?''', ('%'+find_author[1:]+'%',))
        auth = cur.fetchone() #type: list
        if auth is not None:
            #print(' ID TITLE                    AUTHOR           YEAR STATUS')
            print(f'{auth[0]:2} {auth[1]:25} {auth[2]:15} {auth[3]:5} {auth[4]:15}')
        else:
            print("Книги с таким автором нет в библиотеке!")
    elif n == 3:
        find_year = int(input("Введите искомый год написания: ")) #type: int
        cur.execute('''select * from LIBRARY where YEARS == ?''', (find_year,))
        result_year = cur.fetchall() #type: list
        if result_year is not None:
            #print(' ID TITLE                    AUTHOR           YEAR STATUS')
            for rows in result_year:
                print(f'{rows[0]:2} {rows[1]:25} {rows[2]:15} {rows[3]:5} {rows[4]:15}')
        else:
            print("Книги с таким годом написания нет в библиотеке!")
    conn.commit()  # для сохранения всех изменений
    conn.close()  # закрытие БД

def print_lib():
    conn = sqlite3.connect('library.db')  # присоединение к базе данных
    cur = conn.cursor()  # курсор базы данных (далее БД)
    cur.execute('select * from LIBRARY')
    result = cur.fetchall() #type: list
    print(' ID TITLE                    AUTHOR           YEARS STATUS')
    for row in result:
        print(f'{row[0]:2} {row[1]:25} {row[2]:15} {row[3]:5} {row[4]:15}')
    conn.commit()  # для сохранения всех изменений
    conn.close()  # закрытие БД

def update_status() -> str:
    conn = sqlite3.connect('library.db')  # присоединение к базе данных
    cur = conn.cursor()  # курсор базы данных (далее БД)
    id_input = int(input("Введите ID книги, статус которой хотите поменять:")) #type: int
    cur.execute('''select ID from LIBRARY where ID == ?''', (id_input,))
    result_id = cur.fetchall() #type: list
    if result_id is not None:
        new_status = input("Введите новый стату для книги (в наличии/выдана):") #type: str
        cur.execute('''update LIBRARY set STATUS = ? where ID == ?''', (new_status, id_input))
    else:
        print ("Книги с таким ID нет в библиотеке!")
    conn.commit()  # для сохранения всех изменений
    conn.close()  # закрытие БД
    write_DB()
    return print("Статус книги обновлен!")

def write_DB(): #записываем таблицу в текстовый файл
    #БД будет записываться обновленная, то есть в файле не будет прежних версий БД
    file_lib = open('library_text.txt', 'w+')
    conn = sqlite3.connect('library.db')  # присоединение к базе данных
    cur = conn.cursor()  # курсор базы данных (далее БД)
    cur.execute('select * from LIBRARY')
    result = cur.fetchall() #type: list
    with open('library_text.txt', 'r') as f:
        if f.read() == '':
            s_title = (' ID TITLE                    AUTHOR           YEARS STATUS') #type: str
            file_lib.write('\n')
            file_lib.write(s_title)
            for row in result:
                s = (f'{row[0]:2} {row[1]:25} {row[2]:15} {row[3]:5} {row[4]:15}') #type: str
                file_lib.write(s)
                file_lib.write('\n')
            file_lib.close()
        else:
            with open('library_text.txt', 'r+') as f2:
                f2.truncate(0)
                s_title = (' ID TITLE                    AUTHOR           YEARS STATUS') #type: str
                file_lib.write('\n')
                file_lib.write(s_title)
                for row in result:
                    s = (f'{row[0]:2} {row[1]:25} {row[2]:15} {row[3]:5} {row[4]:15}') #type: str
                    file_lib.write(s)
                    file_lib.write('\n')
                file_lib.close()

    conn.commit()  # для сохранения всех изменений
    conn.close()  # закрытие БД

def create_db () -> str:
    conn = sqlite3.connect('library.db')  # присоединение к базе данных
    cur = conn.cursor()  # курсор базы данных (далее БД)
    cur.execute('''create table if not exists LIBRARY (ID integer PRIMARY KEY NOT NULL,
                                            TITLE text, AUTHOR text,
                                            YEARS integer, STATUS text)''')
    # пусть в нашей таблице уже есть несколько книг
    cur.execute('''insert into LIBRARY (TITLE, AUTHOR, YEARS, STATUS)
                values ("Сто лет одиночества", "Г.Г. Маркес", 1967, "в наличии"),
                        ("Мастер и Маргарита", "М. Булгаков", 1940, "выдана"),
                        ("Отверженные", "В. Гюго", 1862, "в наличии")''')
    conn.commit()  # для сохранения всех изменений
    conn.close()  # закрытие БД
    return print("База данных создана!")

main()

