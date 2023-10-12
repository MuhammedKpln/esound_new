from typing import Union

import httpx

from config import CONFIG_FILE
from helpers import Message


class Auth:
    def __init__(self):
        self.access_token: Union[str, None] = None

    async def _login_esound(self, email: str, password: str) -> str:
        Message.info("Esound: Logging in..")
        async with httpx.AsyncClient() as client:
            data = {
                "client_id": "EsoundApp",
                "app": "esound",
                "device_id": "2E5B120A-19D2-4AA2-988E-E80378CD4619",
                "username": email,
                "password": password,
                "grant_type": "password",
                "autologin": "false"
            }
            response = await client.post('https://accounts.spicysparks.com/connect/token', data=data)
            json = response.json()

            try:
                Message.ok("Esound: Login succedeed.")
                return json["access_token"]
            except KeyError:
                Message.error(
                    f"{json['error']} - Please check your email and password inside {CONFIG_FILE}")
                exit()

    async def initialize(self, email: str, password: str):

        access_token = await self._login_esound(email, password)

        self.access_token = access_token
