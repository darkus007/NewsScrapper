from database.postgresql import PostgreSQL


class TestPostgreSQL:

    def test_prepare_database(self, connection_for_test):
        """ Данные не теряются при выполнении функции prepare_database() """
        with connection_for_test.cursor() as cursor:
            cursor.execute("INSERT INTO root (url) VALUES ('http://test.ru') ON CONFLICT (url) DO NOTHING")
            connection_for_test.commit()
        PostgreSQL(connect=connection_for_test).prepare_database()
        with connection_for_test.cursor() as cursor:
            cursor.execute("SELECT root.url FROM root LEFT JOIN page ON root.id = page.root_id LIMIT 1;")
            assert len(cursor.fetchall()) > 0

    def test_add_root(self, connection_for_test):
        added_id = PostgreSQL(connect=connection_for_test).add('root', {"url": "http://test.add.root.ru"})
        assert added_id is not None
        with connection_for_test.cursor() as cursor:
            cursor.execute(f"SELECT * FROM root WHERE id = {added_id};")
            assert cursor.fetchall()[0][0] == added_id

    def test_add_page(self, connection_for_test):
        added_id = PostgreSQL(connect=connection_for_test)\
            .add('page', {"root_id": 1, "title": "Title test_add_page text",
                          "url": "http://test.add.table.ru", "html": "html page"})
        assert added_id is not None
        with connection_for_test.cursor() as cursor:
            cursor.execute(f"SELECT * FROM page WHERE id = {added_id};")
            assert cursor.fetchall()[0][0] == added_id

    def test_fetch_root(self, connection_for_test):
        fetched_id = PostgreSQL(connect=connection_for_test).fetch('root', ['id'], {"url": "http://test.add.root.ru"})
        assert fetched_id is not None
        with connection_for_test.cursor() as cursor:
            cursor.execute(f"SELECT id FROM root WHERE id = {fetched_id[0][0]};")
            assert cursor.fetchall() == fetched_id

    def test_fetch_page(self, connection_for_test):
        fetched_id = PostgreSQL(connect=connection_for_test).fetch('page', ['id'], {"url": "http://test.add.table.ru"})
        assert fetched_id is not None
        with connection_for_test.cursor() as cursor:
            cursor.execute(f"SELECT id FROM page WHERE root_id = {fetched_id[0][0]};")
            assert cursor.fetchall() == fetched_id
