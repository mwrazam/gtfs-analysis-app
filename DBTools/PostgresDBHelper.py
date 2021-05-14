import sys
import psycopg2
import psycopg2.extras
from psycopg2 import sql


class PostgresDBHelper():
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.schema = 'public'

    def connect(self, dbname=None):
        if dbname:
            self.database = dbname
        
        try:
            self.connection = psycopg2.connect(host=self.host, user=self.user, password=self.password, dbname=self.database)
            self.connection.autocommit = True
            self.cursor = PostgresDBCursor(self.connection)
            print(f"Successfully connected to {self.database} as {self.user}.")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error connecting to the database")
            print(error)
            sys.exit(1)

        return self.connection

    def __enter__(self):
        return self.connect()

    def __exit__(self, type, value, traceback):
        self.disconnect()

    def change_database(self, dbname):
        self.database = dbname
        self.disconnect()
        self.connect()

    def disconnect(self):
        if self.connection:
            self.connection.close()
            #print(f"Successfully disconnected.")

    def list_databases(self, name=None):
        with self.cursor as c:
            c.execute(sql.SQL("SELECT DATNAME FROM PG_DATABASE;"))
            return c.fetchall()
        return False

    def list_tables(self, schema=None):
        if schema:
            self.schema = schema
        with self.cursor as c:
            c.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE (TABLE_CATALOG='{self.database}' and TABLE_SCHEMA='{self.schema}')")
            results = [res[0] for res in c.fetchall()]
            return results
        return False

    def get_table_columns(self, database, table_name):
        if self.database != database:
            self.disconnect()
            self.connect(database)
        if self.table_exists(table_name):
            with self.cursor as c:
                c.execute(f"SELECT table_catalog, table_schema, table_name,column_name, data_type from information_schema.columns where table_catalog in ('{self.database}') and table_schema not in ('pg_catalog', 'information_schema') and table_name = '{table_name}';")
                results = {res[3]:res[4] for res in c.fetchall()}
                return results
        return False


    def database_exists(self, name):
        with self.cursor as c:
            c.execute(f"SELECT DATNAME FROM PG_DATABASE WHERE DATNAME='{name}';")
            results = [res[0] for res in c.fetchall()]
            if len(results) > 0:
                return True
            else:
                return False
        return False

    def table_exists(self, name):
        with self.cursor as c:
            c.execute(f"SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='{name}';")
            results = [res[0] for res in c.fetchall()]
            if len(results) > 0:
                return True
            else:
                return False
        return False

    def drop_database(self, name):
        with self.cursor as c:
            c.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(sql.Identifier(name)))
            return True
        return False

    def drop_table(self, name):
        if self.table_exists(name):
            with self.cursor as c:
                c.execute(f"DROP TABLE {name};")
                return True
        return False

    def create_database(self, name):
        if not self.database_exists(name):
            with self.cursor as c:
                c.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(name)))
                return True
        else:
            print(f"Database '{name}' already exists, cannot create.")
        return False

    def build_agencies_tables(self, reload=False):
        self.create_database("app")
        self.disconnect()
        self.connect("app")
        if not self.table_exists("agencies"):
            self.execute_script_from_file("create_agencies_tables.sql")
        elif reload:
            if self.table_exists("agencies"):
                self.drop_table("agencies")
            self.execute_script_from_file("create_agencies_tables.sql")
        else:
            print(f"Table 'agencies' already exists, set reload=True to rebuild table.")
        return False

    def build_static_samples_tables(self, database=None, reload=False, tables=None):
        dont_delete_real_time_tables = set(['vehicle_positions', 'alert', 'trip_update'])
        if database:
            self.disconnect()
            self.connect(database)
        else: # by default create sample database and create sample tables there
            self.create_database("sample")
            self.disconnect()
            self.connect("sample")
        if not tables:
            tables = set(["agency", "stops", "routes", "trips", "stop_times", "calendar", "calendar_dates", 
                "fare_attributes", "fare_rules", "shapes", "frequencies", "transfers", "pathways", "levels",
                "feed_info", "translations", "attributions"])
        else:
            tables = set(tables)
        print(f"In {self.database}, we need to create these tables: {' ,'.join(tables)}")
        tables_in_db = set(self.list_tables())
        if len(tables - tables_in_db) > 0 or reload: # there are discrepencies from our list of tables to those in the sample database
            for t in tables_in_db: # wipe all tables in sample database
                self.drop_table(t)
            self.execute_script_from_file("create_sample_tables.sql")
            if database:
                remove_tables = (set(self.list_tables()) - tables - dont_delete_real_time_tables)
                for table in remove_tables:
                    self.drop_table(table)
        else:
            print(f"Static sample tables already exist, set reload=True to rebuild tables.")

    def create_static_templates_for_agency(self, agency_name, tables, reload=False):
        if not self.database_exists(agency_name):
            self.create_database(agency_name)
        self.build_static_samples_tables(database=agency_name,tables=tables,reload=reload)
        
    def sync_static_tables_for_agency(self, agency_name, static_data, reload=False):
        dont_delete_real_time_tables = set(['vehicle_positions', 'alert', 'trip_update'])
        if self.database != agency_name:
            self.disconnect()
            self.connect(agency_name)
        # ideally we would check our tables here before doing any loading...
        tables_in_db = set(self.list_tables()) - dont_delete_real_time_tables
        if len(tables_in_db) > 0:
            for table in tables_in_db:
                if reload:
                    with self.cursor as c:
                        c.execute(f"TRUNCATE {table};") # WARNING: THIS REQUIRES EXCLUSIVE ACCESS LOCK
                        
                results = []
                with self.cursor as c:
                    c.execute(f"SELECT * FROM {table} LIMIT 1;")
                    results = [res for res in c.fetchall()]

                if len(results) == 0:
                    if len(static_data[table]['data']) > 1:
                        print(f"Loading {len(static_data[table]['data'])} items into {table} table for {agency_name}")
                        cols = static_data[table]['cols']
                        query = f"INSERT INTO {table} ({','.join(cols)}) VALUES %s"
                        
                        with self.cursor as c:
                            psycopg2.extras.execute_values(c, query, static_data[table]['data'])
            print(f"Successfully loaded all static data for {self.database}")
            return True
        return False

    def sync_agencies(self, agencies, reload=False):
        if self.database != "app":
            self.disconnect()
            self.connect("app")
        if self.table_exists("agencies"):
            if reload:
                with self.cursor as c:
                    c.execute("DELETE FROM agencies;")
            with self.cursor as c:
                c.execute(f"SELECT * FROM agencies;")
                results = [res[0] for res in c.fetchall()]
                agencies_to_add = [a for a in agencies if a['agency_name'] not in results]
                if len(agencies_to_add) > 0:
                    columns = agencies_to_add[0].keys()
                    query = "INSERT INTO agencies ({}) VALUES %s".format(','.join(columns))
                    values = [[value for value in agency.values()] for agency in agencies_to_add]
                    psycopg2.extras.execute_values(c, query, values)

        else:
            print("Error: agencies table does not exist")
        return False

    def get_agencies(self, active=True):
        if self.database != "app":
            self.disconnect()
            self.connect("app")
        with self.cursor as c:
            if active:
                c.execute("SELECT * FROM agencies WHERE active='true';")
            else:
                c.execute("SELECT * FROM agencies;")
            keys = [desc[0] for desc in c.description]
            results = [dict(zip(keys, res)) for res in c.fetchall()]
            return results
        return False

    def get_realtime_vehicle_positions_count(self, agency):
        if agency:
            if self.database != agency:
                self.disconnect()
                self.connect(agency)
            with self.cursor as c:
                c.execute(f"SELECT count(*) FROM vehicle_positions;")
                res = c.fetchall()[0][0]
                return res
        return False

    def get_routes(self, agency):
        if agency:
            if self.database != agency:
                self.disconnect()
                self.connect(agency)
            with self.cursor as c:
                c.execute(f"SELECT * FROM routes;")
                res = [row for row in c.fetchall()]
                return res
        return False

    def get_route_shape(self, agency, route_id):
        if agency:
            if self.database != agency:
                self.disconnect()
                self.connect(agency)
            with self.cursor as c:
                c.execute(f"select distinct(trips.shape_id), trips.route_id, trips.direction_id, shapes.shape_pt_lat, shapes.shape_pt_lon, shapes.shape_pt_sequence::INTEGER from trips left join shapes on trips.shape_id=shapes.shape_id where trips.route_id='{route_id}' order by shapes.shape_pt_sequence::INTEGER asc;")
                res = [row for row in c.fetchall()]
                return res
        return False

    def get_trips(self, agency, route_id):
        if agency:
            if self.database != agency:
                self.disconnect()
                self.connect(agency)
            with self.cursor as c:
                query = f"select * from trips left join vehicle_positions on trips.trip_id=vehicle_positions.trip where route_id='{route_id}' order by timestamp asc;"
                c.execute(query)
                res = [row for row in c.fetchall()]
                return res
        return False

    def insert_position_update(self, agency_name, data):
        # data  = {cols: [columns...], data: [ [row], [row], ... ]}
        if agency_name:
            if self.database != agency_name:
                self.disconnect()
                self.connect(agency_name)
            with self.cursor as c:
                query = f"INSERT INTO vehicle_positions ({','.join(data['cols']) }) VALUES %s ON CONFLICT DO NOTHING;"
                psycopg2.extras.execute_values(c, query, data['data'])

    def execute_script_from_file(self, filename):
        fp = sys.path[0] + "/DBScripts/" + filename
        with open(fp, 'r') as sql_file:
            print(f"Executing {fp}")
            sql_commands = sql_file.read().split(';')
            for command in sql_commands:
                with self.cursor as c:
                    try:
                        c.execute(command)
                    except:
                        print(f"Command skipped: {command}")

class PostgresDBCursor():
    def __init__(self, connection):
        self.connection = connection
        self.cursor = None

    def __enter__(self):
        return self.create_cursor()

    def __exit__(self, type, value, traceback):
        self.close_cursor()

    def create_cursor(self):
        self.cursor = self.connection.cursor()
        return self.cursor

    def close_cursor(self):
        if self.cursor:
            self.cursor.close()