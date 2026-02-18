from utils.db.interface import DBInterface
import oracledb
from typing import List, Dict, Any, Optional, cast, Iterable
from utils.logger import Logger

log = Logger("AgileE6Provider")


class AgileE6Provider(DBInterface):
    """Oracle Agile E6 Database Provider implementation. This class provides methods to connect to an Oracle database, execute queries, and manage the connection lifecycle. It includes error handling and logging for better traceability and debugging.
    """

    def __init__(self, user: str, password: str, dsn: str):
        """Constructor for AgileE6Provider. Initializes the database connection parameters and sets up logging.
        Args:
            user (str): The username for the Oracle database.
            password (str): The password for the Oracle database.
            dsn (str): The Data Source Name (DSN) for the Oracle database.
        """

        self.params = {
            "user": user,
            "password": password,
            "dsn": dsn
        }
        self.connection: Optional[oracledb.Connection] = None
        log.info("AgileE6Provider initialized with provided database parameters.")

    def connect(self):
        """Establishes a connection in Thin Mode by default.
        This method attempts to connect to the Oracle database using the provided parameters. It includes error handling to catch and log any connection issues.
        
        Raises:
            oracledb.Error: If there is an error during the connection process.
        """

        try:
            conn = oracledb.connect(**self.params)
            if conn is None:
                raise oracledb.Error("Oracle connect returned None unexpected.")
            
            # Wir nutzen cast, um Pylance zu garantieren: Das hier IST eine Connection.
            self.connection = cast(oracledb.Connection, conn)
            log.info("Successfully connected to the Oracle database.")
        except oracledb.Error as e:
            log.error(f"Oracle Database connection Error: {e}")
            raise
    
    def _get_connection(self) -> oracledb.Connection:
        """Helper to satisfy the type checker regarding Optional connection.
         This method ensures that we have a valid connection before proceeding with any database operations. If the connection is not established, it attempts to connect and then checks again to guarantee that we have a valid connection object.
         Returns:
             oracledb.Connection: A valid Oracle database connection.
         Raises:
             oracledb.Error: If the connection could not be established after attempting to connect.
        """

        if self.connection is None:
            # Wir rufen connect auf, ignorieren aber den Rückgabewert der Methode
            # und prüfen lokal erneut, um Pylance absolute Sicherheit zu geben.
            self.connect()
            
        # Der "Double Check" mit Assertion oder explizitem Cast
        if self.connection is None:
            raise oracledb.Error("Failed to initialize connection.")
            
        return self.connection

    def disconnect(self):
        """Closes the database connection.
        This method checks if a connection exists and attempts to close it. It includes error handling to catch and log any issues that may arise during the disconnection process.
        """

        if self.connection:
            try:
                self.connection.close()
                log.info("Database connection closed successfully.")
            except oracledb.Error as e:
                log.error(f"Error closing database connection: {e}")
            finally:
                self.connection = None

    def execute_query(self, query: str) -> List[List[Any]]:
        """Executes a given SQL query with optional parameters and returns the results as a list of dictionaries.
        This method establishes a connection if not already connected, executes the provided SQL query with the given parameters, and returns the results. It includes error handling to manage any issues that may arise during query execution.
        Args:
            query (str): The SQL query to be executed.
        Returns:
            List[List[Any]]: A list of lists representing the query results, where each inner list corresponds to a row with column values.
        Raises:
            oracledb.Error: If there is an error during query execution.
        """

        conn = self._get_connection()
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                conn.commit()
                return cursor.fetchall()
        except oracledb.Error as e:
            log.error(f"Error executing query: {e}")
            raise

    def get_bom_first_level(self, parent_part_id: str) -> List[Dict[str, Any]]:
        """
        Executes the parent-child join to retrieve the first level of a BOM.
        This method retrieves the first level of the Bill of Materials (BOM) for a given parent item ID by executing a SQL query that joins the relevant tables. It returns the results as a list of dictionaries, where each dictionary represents a child item with its details. The method includes error handling to manage any issues that may arise during query execution.
        Args:
            parent_part_id (str): The part ID of the parent item for which to retrieve the BOM.
        Returns:
            List[Dict[str, Any]]: A list of dictionaries representing the child items in the BOM, where each dictionary contains details such as child_id, item_type, lev_ind, pos_no, chk_name, and cur_flag.
        Raises:
            oracledb.Error: If there is an error during query execution.
        """

        conn = self._get_connection()

        query = """
        SELECT 
            son.part_id AS child_id, 
            son.item_type, 
            son.lev_ind,
            bom.pos_no, 
            son.chk_name,
            son.cur_flag
        FROM t_master_dat fat
        JOIN t_master_str bom ON fat.c_id = bom.c_id_1
        JOIN t_master_dat son ON bom.c_id_2 = son.c_id
        WHERE fat.part_id = :part_id 
          AND fat.cur_flag = 'y'
        ORDER BY bom.pos_no
        """
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, part_id=parent_part_id)
                
                description = cursor.description
                if description is None:
                    return []
                
                columns = [str(col[0]).lower() for col in description]
                
                # Fetchall absichern: Wir casten das Ergebnis zu einem Iterable.
                # Damit weiß Pylance: Man kann darüber loopen.
                raw_data = cursor.fetchall()
                if raw_data is None:
                    return []
                
                iterable_data = cast(Iterable[Any], raw_data)
                
                results = [dict(zip(columns, row)) for row in iterable_data]
                return results
        except oracledb.Error as e:
            log.error(f"Error executing BOM query: {e}")
            return []
    
    def get_item_details(self, part_id: str) -> Dict[str, Any]:
        """
        Retrieves details of a specific item by its part ID.
        This method retrieves the details of a specific item from the database using its part ID. It executes a SQL query to fetch the relevant information and returns it as a dictionary. The method includes error handling to manage any issues that may arise during query execution.
        Args:
            part_id (str): The part ID of the item for which to retrieve details.
        Returns:
            Dict[str, Any]: A dictionary containing the details of the item, such as part_id, item_type, lev_ind, chk_name, and cur_flag. If the item is not found or an error occurs, an empty dictionary is returned.
        Raises:
            oracledb.Error: If there is an error during query execution.
        """
        conn = self._get_connection()

        query = """
        SELECT 
            part_id, 
            item_type,
            lev_ind,
            chk_name,             
            cur_flag
        FROM t_master_dat
        WHERE part_id = :part_id
          AND cur_flag = 'y'
        """
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, part_id=part_id)
                
                description = cursor.description
                if description is None:
                    return {}
                
                columns = [str(col[0]).lower() for col in description]
                
                row = cursor.fetchone()
                if row is None:
                    return {}
                
                result = dict(zip(columns, row))
                return result
        except oracledb.Error as e:
            log.error(f"Error executing item details query: {e}")
            return {}