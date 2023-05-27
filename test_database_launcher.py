import unittest
from config import database_name, database_user, database_password, database_host, database_port
from database_launcher import Database_launcher


class TestDatabaseLauncher(unittest.TestCase):
    def setUp(self) -> None:
        self.database = Database_launcher(
            database=database_name,
            user=database_user,
            password=database_password,
            host=database_host,
            port=database_port
        )

    def tearDown(self) -> None:
        self.database.close()

    def test1_add_user(self):
        try:
            self.database.add_user(123456789)
            self.database.add_user('987654321')
        except Exception as error:
            print(error)
            self.assertTrue(False)

    def test2_user_exists1(self):
        self.assertTrue(self.database.user_exists('123456789'))
        self.assertTrue(self.database.user_exists(987654321))

    def test3_delete_user(self):
        self.database.del_user('123456789')
        self.database.del_user(987654321)

    def test4_user_exists2(self):
        self.assertFalse(self.database.user_exists('123456789'))
        self.assertFalse(self.database.user_exists(987654321))

    def test5_user_is_admin(self):
        self.assertFalse(self.database.user_is_admin(123456789))
        self.assertFalse(self.database.user_is_admin('987654321'))

    def test6_add_admin(self):
        self.database.add_admin('123456789', 55896, 'шалак')
        self.database.add_admin(987654321, '69855', 'шалак')
        self.assertRaises(Exception, self.database.add_admin, list(), tuple(), 8436)

    def test7_get_admins(self):
        result = self.database.get_admins()
        self.assertIsInstance(result, list)

    def test8_admin_exists1(self):
        self.assertTrue(self.database.admin_exists(123456789))
        self.assertTrue(self.database.admin_exists('987654321'))

    def test9_get_admin_name1(self):
        self.assertEqual(self.database.get_admin_name(123456789), 'шалак')
        self.assertEqual(self.database.get_admin_name('987654321'), 'шалак')
        self.assertIsNone(self.database.get_admin_name(444))
        self.assertIsNone(self.database.get_admin_name('555'))

    def test10_del_admin(self):
        try:
            self.database.del_admin('123456789')
            self.database.del_admin(987654321)
            self.database.del_admin(5555)
        except Exception as error:
            print(error)
            self.assertTrue(False)

    def test11_admin_exists2(self):
        self.assertFalse(self.database.admin_exists(123456789))
        self.assertFalse(self.database.admin_exists('987654321'))

    def test12_add_ad(self):
        self.database.add_ad('u_name', 'p_name', 10, 100, 'town', 'pic_id', 123, 'yes')
        self.assertRaises(Exception, self.database.add_ad, list(), tuple(), 8436)

    def test13_update_ad_status(self):
        self.database.update_ad_status(self.database.get_ad_by_data('u_name', 'p_name', 10, 100, 'town', 'pic_id', 123, 'yes')[0])
        self.assertRaises(Exception, self.database.update_ad_status)

    def test14_del_ad(self):
        self.database.del_ad(self.database.get_ad_by_data('u_name', 'p_name', 10, 100, 'town', 'pic_id', 123, 'yes')[0])
