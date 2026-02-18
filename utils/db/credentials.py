import os
from typing import Dict
from dotenv import load_dotenv
from utils.logger import Logger

log = Logger("CredentialManager")

class CredentialManager:
    """Manages database credentials for different PLM environments (PROD, QS, etc.)."""
    
    def __init__(self):
        # Lädt die .env Datei beim Initialisieren
        load_dotenv()

    def get_credentials(self, env: str) -> Dict[str, str]:
        """
        Returns a dictionary with user, password, and dsn for the given environment.
        Expects keys like PROD_USER, PROD_PASSWORD, PROD_DSN in .env
        """
        env = env.upper()
        for key, value in os.environ.items():
            log.debug(f"Env Var: {key} = {'***' if 'PASSWORD' in key else value}")
                     
        credentials = {
            "user": os.getenv(f"{env}_USER"),
            "password": os.getenv(f"{env}_PASSWORD"),
            "dsn": os.getenv(f"{env}_DSN")
        }

        # Validierung: Fehlt etwas Wesentliches?
        missing = [key for key, value in credentials.items() if not value]
        if missing:
            error_msg = f"Missing credentials for environment {env}: {', '.join(missing)}"
            log.error(error_msg)
            raise ValueError(error_msg)

        log.info(f"Credentials for {env} successfully loaded.")
        return credentials # type: ignore (Pylance safe, as we validated None values)