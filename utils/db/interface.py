from abc import ABC, abstractmethod
from typing import Any, Dict, List
from utils.logger import Logger

log = Logger("DBInterface")

class DBInterface(ABC):
    @abstractmethod
    def connect(self) -> None:
        """Establish a connection to the database."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close the connection to the database."""
        pass

    @abstractmethod
    def execute_query(self, query: str,) -> List[List[Any]]:
        """Execute a query against the database and return the results as a list of lists."""
        pass

    @abstractmethod
    def get_item_details(self, part_id: str) -> Dict[str, Any]:
        """Retrieve details of a specific item by its part ID."""
        pass

    @abstractmethod
    def get_bom_first_level(self, parent_id: str) -> List[Dict[str, Any]]:
        """Retrieve the first level of the Bill of Materials (BOM) for a given parent item ID."""
        pass