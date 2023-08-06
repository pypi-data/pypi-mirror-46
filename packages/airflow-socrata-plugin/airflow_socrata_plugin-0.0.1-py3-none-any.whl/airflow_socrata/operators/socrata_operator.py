# Operators used to interface with Socrata SDK.

from sodapy import Socrata

from airflow.models import BaseOperator
from airflow.models import Variable
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException

from airflow.hooks.postgres_hook import PostgresHook
from airflow_socrata.hooks.socrata_hook import SocrataHook


DEFAULT_PG_CONN = "etl_postgres"
DEFAULT_PG_SCHEMA = "public"
UPLOAD_CHUNK_SIZE = 10000

class SocrataOperator(BaseOperator):
    """The base Socrata API operator.
    """

    def __init__(self, *args, **kwargs):
        """Initializes a base Socrata operator.
        """

        # Set alternative connection ID if specified
        self.conn_id = None
        if "conn_id" in kwargs:
            cid_value = kwargs["conn_id"]
            if type(cid_value) is str:
                self.conn_id = cid_value

        super().__init__(*args, **kwargs)

    def execute(self, **kwargs):
        """Creates a Socrata hook and establishes connection.
        """

        self.socrata = SocrataHook(self.conn_id).get_conn()


class SocrataUpsertOperator(SocrataOperator):
    """The Socrata operator to upsert entries from PostgreSQL database.
    """

    def __init__(self,
                 table_name,
                 dataset_id,
                 replace,
                 postgres_conn_id=None,
                 postgres_schema=None,
                 *args, **kwargs):
        """Initializes an Socrata Upsert operator.
        Arguments:
            table_name {str} -- The name of the source PostgreSQL table.
            dataset_id {int} -- The ID of the target Socrata dataset.
            replace {bool} -- Whether to replace the whole dataset.
        """

        self.table_name = table_name
        self.dataset_id = dataset_id
        self.replace = replace
        self.postgres_conn_id = postgres_conn_id
        self.postgres_schema = postgres_schema

        if postgres_conn_id is None:
            self.postgres_conn_id = DEFAULT_PG_CONN

        if postgres_schema is None:
            self.postgres_schema = DEFAULT_PG_SCHEMA

        super().__init__(*args, **kwargs)

    def _select_table(self):
        """Selects the table from PostgreSQL database.
        Returns:
            list -- Query results.
        """

        return self.postgres.execute(f"SELECT * FROM {self.table_name};")

    def execute(self, context):
        """Upserts to the specified dataset from the specified PostgreSQL table.
        Arguments:
            context {[type]} -- [description]
        """

        # Initialize PostgreSQL hook
        self.postgres = PostgresHook(
            postgres_conn_id=self.postgres_conn_id,
            schema=self.postgres_schema).get_sqlalchemy_engine()

        # Initialize Socrata hook
        super().execute()

        # Load table
        table = self._select_table()
        self.table_dicts = [dict(row) for row in table]

        if self.replace:
            result = self.socrata.replace(self.dataset_id, self.table_dicts)
        else:
            # Code from etl-airflow
            for i in range(0, len(self.table_dicts), UPLOAD_CHUNK_SIZE):
                try:
                    result = self.socrata.upsert(self.dataset_id, self.table_dicts[i:i+UPLOAD_CHUNK_SIZE])
                except:
                    print(f"Error on record {i}")
                    result = self.socrata.upsert(self.dataset_id, self.table_dicts[i:i+UPLOAD_CHUNK_SIZE])
