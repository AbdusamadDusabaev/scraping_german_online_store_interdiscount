import pymysql
from pymysql import cursors
from config import user, password, port, host, db_name
import os
import shutil


def database(query):
    try:
        connection = pymysql.connect(port=port, host=host, user=user, password=password,
                                     database=db_name, cursorclass=cursors.DictCursor)
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            connection.commit()
            return result
        except Exception as ex:
            print(f"Something Wrong: {ex}")
            return "Error"
        finally:
            connection.close()
    except Exception as ex:
        print(f"Connection was not completed because {ex}")
        return "Error"


def create_table():
    query = """CREATE TABLE products(`product_id` VARCHAR(50), `language` VARCHAR(5), `title` VARCHAR(500), 
              `price` FLOAT, `category` VARCHAR(100), `description` TEXT, `characteristics` JSON);"""
    result = database(query=query)
    if result != "Error":
        print("[INFO] Таблица успешно создана")
    else:
        print("[ERROR] Не удалось создать таблицу. Проверьте конфигурации базы данных или обратитесь к разработчику")


def record_product(product_id, language, title, price, category, description, characteristics):
    title = title.replace('"', "'")
    description = description.replace('"', "'")
    characteristics = characteristics.replace("'", r'\'')
    query = f"""INSERT INTO products 
                (`product_id`, `language`, `title`, `price`, `category`, `description`, `characteristics`)
                VALUES 
                ("{product_id}", "{language}", "{title}", {price}, "{category}", "{description}", '{characteristics}');"""
    result = database(query=query)
    if result != "Error":
        print(f"[INFO] Товар с id = {product_id} на языке {language} успешно записан в базу данных")
    else:
        print(f"[ERROR] Ошибка при записи в базу данных товара с id = {product_id}")


def create_photos_dir():
    if os.path.isdir("photos"):
        shutil.rmtree("photos")
        os.mkdir("photos")
    else:
        os.mkdir("photos")
    print("[INFO] Папка photos успешно создана")


if __name__ == "__main__":
    create_table()
    create_photos_dir()
