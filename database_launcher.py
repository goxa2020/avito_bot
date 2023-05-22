import psycopg2
import logging


class Database_launcher:
    def __init__(self, database, user, password, host, port):
        self.connection = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()
        logging.info("Database connection successful.")

    def add_user(self, user_id: str | int) -> None:
        with self.connection:
            self.cursor.execute(f'INSERT INTO users (user_id) VALUES({user_id})')
            self.connection.commit()
            return

    def user_is_admin(self, user_id) -> bool:
        with self.connection:
            self.cursor.execute(f'SELECT * FROM admins WHERE admin_id = {user_id}')
            return bool(len(self.cursor.fetchall()))

    def user_exists(self, user_id) -> bool:
        with self.connection:
            self.cursor.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
            result = self.cursor.fetchall()
            return bool(len(result))

    def get_users(self) -> list[tuple]:
        with self.connection:
            self.cursor.execute("SELECT * FROM users")
            return self.cursor.fetchall()

    def add_admin(self, user_id: str | int, appointed_by: str | int, admin_name: str) -> None:
        with self.connection:
            self.cursor.execute(f'INSERT INTO admins VALUES{user_id, appointed_by, admin_name}')
            self.connection.commit()
            return

    def get_admins(self) -> list[tuple]:
        with self.connection:
            self.cursor.execute("SELECT * FROM admins")
            return self.cursor.fetchall()

    def del_admin(self, admin_id: str | int) -> None:
        with self.connection:
            self.cursor.execute(f'DELETE FROM admins WHERE admin_id = {admin_id}')
            self.connection.commit()
            return

    def admin_exists(self, admin_id: str | int) -> bool:
        with self.connection:
            self.cursor.execute(f"SELECT * FROM admins WHERE admin_id = {admin_id}")
            result = self.cursor.fetchall()
            return bool(len(result))

    def get_admin_name(self, admin_id: str | int) -> str | None:
        if self.admin_exists(admin_id):
            with self.connection:
                self.cursor.execute(f'SELECT admin_name FROM admins WHERE admin_id = {admin_id}')
                result = self.cursor.fetchall()[0][0]
                return str(result)
        else:
            logging.info(f'Админ {admin_id} отсутствует')
            return

    def add_ad(self, user_name: str, product_name: str, amount: str | int, price: str | int, town: str,
               picture_id: str | int | None, user_id: str | int, description: str, posted: bool = False) -> None:
        with self.connection:
            self.cursor.execute(f'INSERT INTO ads(user_name, product_name, amount, price, town, picture_id, user_id, description, posted) '
                                f'VALUES{user_name, product_name, amount, price, town, picture_id, user_id, description, posted}')
            self.connection.commit()
            return

    def del_ad(self, ad_id: str | int) -> None:
        with self.connection:
            self.cursor.execute(f'DELETE FROM ads WHERE ad_id = {ad_id}')
            self.connection.commit()
            return

    def update_ad_status(self, ad_id: str | int, posted_status: bool = True):
        with self.connection:
            self.cursor.execute(f'UPDATE ads SET posted = {posted_status} WHERE ad_id = {ad_id}')
            self.connection.commit()
            return

    def update_ad_post_id(self, ad_id: str | int, post_id: str | int) -> None:
        with self.connection:
            self.cursor.execute(f'UPDATE ads SET post_id = {post_id} WHERE ad_id = {ad_id}')
            self.connection.commit()
            return

    def get_posted_ads(self) -> list[tuple]:
        with self.connection:
            self.cursor.execute("SELECT * FROM ads WHERE posted = true")
            return self.cursor.fetchall()

    def get_not_posted_ads(self) -> list[tuple]:
        with self.connection:
            self.cursor.execute("SELECT * FROM ads WHERE posted = false")
            return self.cursor.fetchall()

    def get_user_ads(self, user_id: str | int) -> list[tuple]:
        with self.connection:
            self.cursor.execute(f"SELECT * FROM ads WHERE user_id = {user_id}")
            return self.cursor.fetchall()

    def close(self) -> None:
        logging.info('Database shutdown')
        self.connection.close()
        self.cursor.close()
        return
