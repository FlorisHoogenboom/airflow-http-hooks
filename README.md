# Better HTTP hooks for Airflow

This repository contains an Airflow plugin that enhances the functionality of the default HttpHook. Reason for this was that in my work I often find my self duplicating logic when using Airflow to move data provided by some RESTfull service to e.g. a database.

Currently two additional Hooks are provided: `ExtendedHttpHook` and `PaginatedHttpHook`.

## Example usage
To use these hooks in your airflow project clone this repository into the `plugins` folder as defined in `airflow.cfg` (default is `$AIRFLOW_HOME/plugins`). You can than simply import the plugins:
```{python}
from airflow.hooks.better_http import ExtendedHttpHook, PaginatedHttpHook

# Your code...
```

### ExtendedHttpHook
This hook provides similar functionality to the default HttpHook, however this hook allows one to specify additional headers to be sent with each request in Airflows connection interface as JSON. This may be desirable when working with HTTP endpoints that need some other form of authentication than the default Basic Auth.

### PaginatedHttpHook
This hook can be used to get data from endpoints that are paginated. It uses a callable provided in the `pagination_function` parameter to derive the parameters to fetch the next page. The `run` method is a generator that yields each time a new page is fetched.