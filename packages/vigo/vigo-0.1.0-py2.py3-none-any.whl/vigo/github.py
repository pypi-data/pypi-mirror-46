from urllib.parse import quote_plus

import requests

from vigo.config import GeneralConfig
from vigo.exceptions import OpenstackerException

general_conf = GeneralConfig()


class Github:
    api_url = "https://api.github.com"
    url = "https://github.com"

    def api(self, query, method="GET"):
        if general_conf.debug:
            print("Execute {query}".format(query=query))
        req = requests.get(query)
        if req.status_code != 200:
            raise OpenstackerException(
                "github API error ({query}): {status}".format(
                    query=query, status=req.status_code
                )
            )
        return req.json()

    def search(self, query, repos):
        query = "{api_url}/search/code?q={query}+repo:{repos}".format(
            api_url=self.api_url,
            query=quote_plus(query),
            repos="+repo:".join(repos),
        )
        return self.api(query)
