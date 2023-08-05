from aioidex.http.modules.base import BaseModule


class Private(BaseModule):
    """Contract-Backed Endpoints

    https://docs.idex.market/#tag/Contract-Backed-Trade-Endpoints
    """
    async def order(self, token_buy:str, amount_buy, token_sell, amount_sell):