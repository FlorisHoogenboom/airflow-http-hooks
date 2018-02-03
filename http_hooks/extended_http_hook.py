import json
from airflow.hooks.http_hook import HttpHook


class ExtendedHttpHook(HttpHook):
    """
    Extended version of the HTTP Hook that allows headers to be specified
    in the Airflow connections interface. This comes in handy since the
    access tokens for Harvest need to be submitted in the Authorization
    headers.
    """
    def get_conn(self, headers):
        """
        Overridden method of parent get_conn. This method fetches the extra
        paramters as specified in the airflow connection interface and extends
        the given headers with the headers specified there.
        :param headers: a dict of headers.
        :return: HTTP session to be used with requests.
        """
        if not headers:
            headers = {}

        conn = self.get_connection(self.http_conn_id)
        extra = json.loads(
            conn.get_extra()
        )

        if (
            type(extra) is dict and
            type(extra.get('headers')) is dict
        ):
            return super(ExtendedHttpHook, self).get_conn(
                {**headers, **extra['headers']}
            )
        else:
            return super(ExtendedHttpHook, self).get_conn(
                headers
            )
