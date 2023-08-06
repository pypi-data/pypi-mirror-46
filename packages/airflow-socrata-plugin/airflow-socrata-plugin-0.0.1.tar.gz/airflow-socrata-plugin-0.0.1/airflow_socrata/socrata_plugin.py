# Plugin definition file.
from airflow.plugins_manager import AirflowPlugin
from airflow.models import BaseOperator
from airflow.hooks.base_hook import BaseHook
from airflow_socrata.operators.socrata_operator import SocrataUpsertOperator
from airflow_socrata.hooks.socrata_hook import SocrataHook


class SocrataPlugin(AirflowPlugin):
    name = 'airflow_socrata'
    operators = [SocrataUpsertOperator]
    hooks = [SocrataHook]

    # A list of class(es) derived from BaseExecutor
    executors = []
    # A list of references to inject into the macros namespace
    macros = []
    # A list of objects created from a class derived
    # from flask_admin.BaseView
    admin_views = []
    # A list of Blueprint object created from flask.Blueprint
    flask_blueprints = []
    # A list of menu links (flask_admin.base.MenuLink)
    menu_links = []
