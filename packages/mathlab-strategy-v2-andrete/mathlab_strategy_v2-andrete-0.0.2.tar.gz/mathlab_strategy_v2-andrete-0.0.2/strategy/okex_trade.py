import asyncio
import threading

from .okex import runClient
from .trade_tool import TradeTool
from .utf8logger import INFO


class OkexTrade(object):
    def __init__(self, pair):
        loop = asyncio.get_event_loop()
        inputs = asyncio.Queue(loop=loop)
        stop = loop.create_future()
        self.trade = TradeTool(loop, inputs)
        asyncio.ensure_future(runClient(loop, inputs, stop, self.trade, pair), loop=loop)
        thread = threading.Thread(target=loop.run_forever)
        thread.start()
        while self.trade.getLongQty() is None:
            pass
        INFO("trade is ready!")
        # try:
        #     while True:
        #         # Since there's no size limit, put_nowait is identical to put.
        #         message = input("> ")
        #         if message == '1': # ENTERLONG
        #             self.trade.do_maker_parallel("ENTER", "LONG", 5)
        #         elif message == '2': # ENTERSHORT
        #             self.trade.do_maker_parallel("ENTER", "SHORT", 5)
        #         elif message == '3': # EXITLONG
        #             self.trade.do_taker_parallel("EXIT", "LONG", 0)
        #         elif message == '4': # EXITSHORT
        #             self.trade.do_maker_parallel("EXIT", "SHORT", 0)
        #         elif message == '0': # quick empty
        #             self.trade.empty_quickly()
        #         else:
        #             continue
        # except (KeyboardInterrupt, EOFError):
        #     loop.call_soon_threadsafe(stop.set_result, None)

    def enter_long(self, typ, vol):
        if typ == "taker":
            self.trade.do_taker_parallel("ENTER", "LONG", vol)
        if typ == "maker":
            self.trade.do_maker_parallel("ENTER", "LONG", vol)

    def enter_short(self, typ, vol):
        if typ == "taker":
            self.trade.do_taker_parallel("ENTER", "SHORT", vol)
        if typ == "maker":
            self.trade.do_maker_parallel("ENTER", "SHORT", vol)

    def exit_long(self, typ, vol):
        if typ == "taker":
            self.trade.do_taker_parallel("EXIT", "LONG", vol)
        if typ == "maker":
            self.trade.do_maker_parallel("EXIT", "LONG", vol)

    def exit_short(self, typ, vol):
        if typ == "taker":
            self.trade.do_taker_parallel("EXIT", "SHORT", vol)
        if typ == "maker":
            self.trade.do_maker_parallel("EXIT", "SHORT", vol)

    def empty_all(self):
        self.trade.empty_quickly()

if __name__ == "__main__":
    a = OkexTrade("ETHUSD")
    # a.enter_long("taker", 5)
