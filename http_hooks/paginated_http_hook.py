from http_hooks.extended_http_hook import ExtendedHttpHook


class PaginatedHttpHook(ExtendedHttpHook):
    @staticmethod
    def pagination_function(resp):
        """
        This function takes a JSON response as content and produces
        the next page URL
        :param resp: A requests Response object
        :return: The queryparams that should be passed to fetch the next page.
        """
        contents = resp.json()

        if (
            type(contents) is dict and
            contents.get('total_pages', None) > contents.get('page', None)
        ):
            return {
                'page': contents.get('page') + 1
            }

        return None


    def __init__(
            self,
            *args,
            pagination_function=pagination_function,
            method='GET',
            **kwargs
    ):
        if method != 'GET':
            raise TypeError('Paginated responses only make sense in the context of GET requests.')

        self.next_page = pagination_function
        super(PaginatedHttpHook, self).__init__(*args, method=method, **kwargs)


    def run(self, endpoint, data=None, headers=None, extra_options=None):
        """
        Performs the request. Be Carfull: future request might fail. Therefore,
        make sure to make the rest of your Task idempotent so that you can manage
        failiures and rerun correctly.
        :param endpoint:
        :param data:
        :param headers:
        :param extra_options:
        :yields: A response object for every pages request.
        """
        if not data:
            data = {}

        resp = super(PaginatedHttpHook, self).run(
            endpoint,
            data=data,
            headers=headers,
            extra_options=extra_options
        )

        yield resp

        # After the first request, check if there are any extra pages
        # if so, keep yielding

        while(self.pagination_function(resp)):
            next_page_params = self.pagination_function(resp)

            resp = super(PaginatedHttpHook, self).run(
                endpoint,
                data={**data, **next_page_params},
                headers=headers,
                extra_options=extra_options
            )

            yield resp
