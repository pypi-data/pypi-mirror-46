# #  Drakkar-Software OctoBot-Channels
# #  Copyright (c) Drakkar-Software, All rights reserved.
# #
# #  This library is free software; you can redistribute it and/or
# #  modify it under the terms of the GNU Lesser General Public
# #  License as published by the Free Software Foundation; either
# #  version 3.0 of the License, or (at your option) any later version.
# #
# #  This library is distributed in the hope that it will be useful,
# #  but WITHOUT ANY WARRANTY; without even the implied warranty of
# #  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# #  Lesser General Public License for more details.
# #
# #  You should have received a copy of the GNU Lesser General Public
# #  License along with this library.
import asyncio

from octobot_channels.channels.exchange_channel import ExchangeChannel
from octobot_channels.channels.exchange.orders import OrdersProducer


class OrdersUpdater(OrdersProducer):
    ORDERS_REFRESH_TIME = 60

    def __init__(self, channel: ExchangeChannel):
        super().__init__(channel)

    async def start(self):
        while not self.should_stop:
            for pair in self.channel.exchange_manager.traded_pairs:
                # TODO
                await self.push(pair, await self.channel.exchange_manager.exchange_dispatcher.get_open_orders(pair))
            await asyncio.sleep(self.ORDERS_REFRESH_TIME)
