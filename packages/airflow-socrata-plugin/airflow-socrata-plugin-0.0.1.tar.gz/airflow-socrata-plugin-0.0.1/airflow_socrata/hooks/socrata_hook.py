# Hooks used to interface with Socrata SDK.

from sodapy import Socrata

from airflow.hooks.base_hook import BaseHook
from airflow.models import Variable
from airflow.exceptions import AirflowException


DEFAULT_SOCRATA_CONN = "http_socrata"

class SocrataHook(BaseHook):
    """Interact with Socrata using Socrata's Python SDK.
    """

    def __init__(self, conn_id=None):
        """Initializes the hook with Socrata SDK.

        Keyword Arguments:
            conn_id {str} -- Name of alternative connection to be used. (default: {None})
        """

        self.conn_info = self.__get_conn_info(conn_id)

    def __get_conn_info(self, conn_id=None):
        """Retrieves connection info from Airflow connections.
        
        Keyword Arguments:
            conn_id {str} -- Name of alternative connection to be used. (default: {None})
        
        Returns:
            Connection -- Connection info for Socrata.
        """

        if conn_id is not None:
            # Use overrride conn ID
            return self.get_connection(conn_id)
        else:
            return self.get_connection(DEFAULT_SOCRATA_CONN)

    def get_conn(self):
        """Authenticates with the Socrata API and returns the session object.

        Returns:
            Socrata -- The Socrata API session.
        """

        extras = self.conn_info.extra_dejson
        return Socrata(
            self.conn_info.host,
            extras["app_token"],
            self.conn_info.login,
            self.conn_info.password)
