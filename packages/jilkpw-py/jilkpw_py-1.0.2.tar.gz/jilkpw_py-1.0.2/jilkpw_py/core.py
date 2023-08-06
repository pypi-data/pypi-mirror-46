"""
core.py contains all of the basic utilities of this wrapper
"""

import requests
from jilkpw_py.error_catch import ResponseErrors


class JilkpwWrapper:
    api_endpoint = "https://jilk.pw/api/v1.0/public"

    def find(self, guild_id: int):
        """
        Gets the Jilk.pw listing from the given guild ID
        """

        listing = self._get_listing(guild_id)

        print(listing)

    def _get_listing(self, guild_id: int):
        """
        Gets response from Jilk.pw & throws exeptions
        """

        resp = requests.get(f"{self.api_endpoint}",
                            params={"guild_id": guild_id})

        ResponseErrors(resp.status_code)

        return resp.json()["details"]
