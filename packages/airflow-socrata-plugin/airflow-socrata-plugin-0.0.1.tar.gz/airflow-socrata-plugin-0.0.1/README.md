# Airflow-Socrata
Simple hooks and operators for uploading data to Socrata.

# Features
- Upsert or reupload PostgreSQL tables to Socrata

# Install
Using pip:
```bash
pip3 install airflow-socrata-plugin
```

# Usage
Create a connection named `http_socrata` of type `http` to store Socrata credentials. *You can also pass in `conn_name` parameter in DAG definition to override.*

Create a connection named `etl_postgres` of type `postgres` to store PostgreSQL credentials. *You can also pass in `postgres_conn_name` parameter in DAG definition to override.*

By default, the plugin looks for the specified table under `public` schema. The schema can be specified with `postgres_schema` parameter.

The plugin is published as a pip package. Refer to the [example DAG](example_dag.py) for available parameters.
