from typing import Optional
from utils.db.interface import DBInterface
from utils.db.providers import AgileE6Provider, CIMDBProvider
from utils.db.credentials import CredentialManager
from utils.logger import Logger

log = Logger("DBFactory")

class DBFactory:
    """
    Factory to create and configure database providers based on the environment.
    """

    @staticmethod
    def get_provider(env: str, system_type: str = "AGILE_E6") -> DBInterface:
        """
        Returns a configured DB provider for the specified environment.
        
        Args:
            env: The environment (e.g., 'PROD', 'QS', 'PQE', 'BLD')
            system_type: The type of PLM system (default: 'AGILE_E6')
        """
        # 1. Zugangsdaten über den CredentialManager holen
        cm = CredentialManager()
        creds = cm.get_credentials(env)
        
        log.info(f"Creating provider for {system_type} in {env} environment.")

        # 2. Den richtigen Provider instanziieren
        if system_type.upper() == "AGILE_E6":
            # Local Import, um Abhängigkeiten sauber zu halten
            from utils.db.providers.agile_e6_sql import AgileE6Provider
            
            return AgileE6Provider(
                user=creds["user"],
                password=creds["password"],
                dsn=creds["dsn"]
            )
            
        elif system_type.upper() == "CIMDB":
            raise NotImplementedError("CIMDBProvider is not yet fully implemented.")

        else:
            error_msg = f"Unknown system type: {system_type}"
            log.error(error_msg)
            raise ValueError(error_msg)