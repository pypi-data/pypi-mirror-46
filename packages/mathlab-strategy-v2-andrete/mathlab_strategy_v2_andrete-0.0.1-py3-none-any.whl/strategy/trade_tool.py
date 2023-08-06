import time
from .utf8logger import INFO, ERROR


class TradeTool(object):
    def __init__(self, loop, inputs):
        self.side_dic = {"ENTERLONG": 1, "ENTERSHORT": 2, "EXITLONG": 3, "EXITSHORT": 4}
        self.loop = loop
        self.inputs = inputs
        self.stall_volume = 1
        self.long_qty = None
        self.short_qty = None
        self.long_avail_qty = None
        self.short_avail_qty = None
        self.order_status_map = {}

    def do_maker_parallel(self, action, side, current_volume):
        action_side = action + side
        name = "maker"
        if action_side == "ENTERLONG":
            while current_volume > self.long_avail_qty:
                vol_list = set()
                tmp_volume = current_volume
                while tmp_volume > self.long_avail_qty:
                    real_vol = min(self.stall_volume, tmp_volume - self.long_avail_qty)
                    vol_list.add(real_vol)
                    tmp_volume -= self.stall_volume
                self.epoch_parallel(name, action_side, vol_list)

        if action_side == "ENTERSHORT":
            while current_volume > self.short_avail_qty:
                vol_list = set()
                tmp_volume = current_volume
                while tmp_volume > self.short_avail_qty:
                    real_vol = min(self.stall_volume, tmp_volume - self.short_avail_qty)
                    vol_list.add(real_vol)
                    tmp_volume -= self.stall_volume
                self.epoch_parallel(name, action_side, vol_list)

        if action_side == "EXITLONG":
            while self.long_qty > current_volume:
                vol_list = set()
                tmp_volume = self.long_qty
                while tmp_volume > current_volume:
                    real_vol = min(self.stall_volume, tmp_volume - current_volume)
                    vol_list.add(real_vol)
                    tmp_volume -= self.stall_volume
                self.epoch_parallel(name, action_side, vol_list)

        if action_side == "EXITSHORT":
            while self.short_qty > current_volume:
                vol_list = set()
                tmp_volume = self.short_qty
                while tmp_volume > current_volume:
                    real_vol = min(self.stall_volume, tmp_volume - current_volume)
                    vol_list.add(real_vol)
                    tmp_volume -= self.stall_volume
                self.epoch_parallel(name, action_side, vol_list)

    def do_taker_parallel(self, action, side, current_volume):
        action_side = action + side
        name = "taker"
        if action_side == "ENTERLONG":
            while current_volume > self.long_avail_qty:
                vol_list = set()
                tmp_volume = current_volume
                while tmp_volume > self.long_avail_qty:
                    real_vol = min(self.stall_volume, tmp_volume - self.long_avail_qty)
                    vol_list.add(real_vol)
                    tmp_volume -= self.stall_volume
                self.epoch_parallel(name, action_side, vol_list)

        if action_side == "ENTERSHORT":
            while current_volume > self.short_avail_qty:
                vol_list = set()
                tmp_volume = current_volume
                while tmp_volume > self.short_avail_qty:
                    real_vol = min(self.stall_volume, tmp_volume - self.short_avail_qty)
                    vol_list.add(real_vol)
                    tmp_volume -= self.stall_volume
                self.epoch_parallel(name, action_side, vol_list)

        if action_side == "EXITLONG":
            while self.long_qty > current_volume:
                vol_list = set()
                tmp_volume = self.long_qty
                while tmp_volume > current_volume:
                    real_vol = min(self.stall_volume, tmp_volume - current_volume)
                    vol_list.add(real_vol)
                    tmp_volume -= self.stall_volume
                self.epoch_parallel(name, action_side, vol_list)

        if action_side == "EXITSHORT":
            while self.short_qty > current_volume:
                vol_list = set()
                tmp_volume = self.short_qty
                while tmp_volume > current_volume:
                    real_vol = min(self.stall_volume, tmp_volume - current_volume)
                    vol_list.add(real_vol)
                    tmp_volume -= self.stall_volume
                self.epoch_parallel(name, action_side, vol_list)

    def epoch_parallel(self, name, side, vol_list):
        order_nums = len(vol_list)
        INFO(name + " parallel: " + side + ", order counts: {}".format(order_nums))
        for real_vol in vol_list:
            self.loop.call_soon_threadsafe(
                self.inputs.put_nowait,
                (self.side_dic[side], name, real_vol)
            )
        INFO(side + " parallel waiting for response...")
        max_waiting_secs = 3
        t = 0
        while len(self.order_status_map) < order_nums:
            INFO(side + " waiting for parallel order status changed...")
            time.sleep(1)
            t += 1
            if t >= max_waiting_secs:
                ERROR(name + " parallel: out of waiting time {} secs".format(t))
                break
            pass
        for oid in self.order_status_map:
            if self.order_status_map[oid] in (0, 1):
                self.loop.call_soon_threadsafe(
                    self.inputs.put_nowait,
                    (oid, "cancel", None)
                )
        self.order_status_map = {}

    def empty_quickly(self):
        if self.long_qty > 0:
            self.do_taker_parallel("EXIT", "LONG", 0)
        if self.short_qty > 0:
            self.do_taker_parallel("EXIT", "SHORT", 0)

    def getStallVolume(self):
        return self.stall_volume

    def setLongQty(self, qty):
        self.long_qty = int(qty)

    def getLongQty(self):
        return self.long_qty

    def setShortQty(self, qty):
        self.short_qty = int(qty)

    def setLongAvailQty(self, qty):
        self.long_avail_qty = int(qty)

    def setShortAvailQty(self, qty):
        self.short_avail_qty = int(qty)

    def setOrderStatus(self, os, oid):
        self.order_status_map[oid] = os
