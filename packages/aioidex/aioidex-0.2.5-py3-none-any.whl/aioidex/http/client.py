from asyncio import AbstractEventLoop

from aioidex.http.modules.private import Private
from aioidex.http.modules.public import Public
from aioidex.http.network import Network


class Client:
    def __init__(
            self,
            address: str = None,
            private_key: str = None,
            loop: AbstractEventLoop = None,
            timeout: int = None
    ) -> None:
        self._http = Network(address, private_key, loop, timeout)

        self.public = Public(self._http)
        self.private = Private(self._http)

    async def close(self, delay: float = 0.250):
        await self._http.close(delay)
