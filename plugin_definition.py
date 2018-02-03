from airflow.plugins_manager import AirflowPlugin

# Airflows import system for plugins is not
# great at handling plugins seperated over
# multiple files. Therefore import the path
# explicitly.
import sys
from os.path import join, dirname
sys.path.append(
    join(dirname(__file__))
)
print(sys.path)
import http_hooks

class BetterHttp(AirflowPlugin):
	"""
	This plugin provides HTTP hooks for Airflow with
	enhanced functionality. E.g. they allow for specifying
	authentication information other than Basic Auth
	and enable simple reading of paginated endpoints.
	"""

	name = "better_http"
	hooks = [
		http_hooks.ExtendedHttpHook,
		http_hooks.PaginatedHttpHook
	]