# Copyright (c) 2023, Keith Rieck
# All rights reserved.

from machine import mem32


class I2cPerf:
    """
    Simple I2C peripheral class for the RP2040.
    An I2cPerf object passively waits for messages from a Controller object.
    This class only sends and receives a single byte.
    """
    I2C0_BASE = 0x40044000
    I2C1_BASE = 0x40048000
    IO_BANK0_BASE = 0x40014000

    mem_rw = 0x0000
    mem_xor = 0x1000
    mem_set = 0x2000
    mem_clr = 0x3000

    IC_CON = 0
    IC_TAR = 4
    IC_SAR = 8
    IC_DATA_CMD = 0x10
    IC_RAW_INTR_STAT = 0x34
    IC_RX_TL = 0x38
    IC_TX_TL = 0x3C
    IC_CLR_INTR = 0x40
    IC_CLR_RD_REQ = 0x50
    IC_CLR_TX_ABRT = 0x54
    IC_ENABLE = 0x6c
    IC_STATUS = 0x70

    def _write_reg(self, reg, data, method=0):
        mem32[self.i2c_base | method | reg] = data

    def _set_reg(self, reg, data):
        self._write_reg(reg, data, method=self.mem_set)

    def _clr_reg(self, reg, data):
        self._write_reg(reg, data, method=self.mem_clr)

    def __init__(self, i2c_ID=0, sda=0,  scl=1, address=0x41):
        self.scl = scl
        self.sda = sda
        self.perfAddress = address
        self.i2c_ID = i2c_ID
        if self.i2c_ID == 0:
            self.i2c_base = self.I2C0_BASE
        else:
            self.i2c_base = self.I2C1_BASE

        # 1 Disable DW_apb_i2c
        self._clr_reg(self.IC_ENABLE, 1)
        # 2 set slave address
        # clr bit 0 to 9
        # set slave address
        self._clr_reg(self.IC_SAR, 0x1ff)
        self._set_reg(self.IC_SAR, self.perfAddress & 0x1ff)
        # 3 write IC_CON  7 bit, enable in slave-only
        self._clr_reg(self.IC_CON, 0b01001001)
        # set SDA PIN
        mem32[self.IO_BANK0_BASE | self.mem_clr | (4 + 8 * self.sda)] = 0x1f
        mem32[self.IO_BANK0_BASE | self.mem_set | (4 + 8 * self.sda)] = 3
        # set SLA PIN
        mem32[self.IO_BANK0_BASE | self.mem_clr | (4 + 8 * self.scl)] = 0x1f
        mem32[self.IO_BANK0_BASE | self.mem_set | (4 + 8 * self.scl)] = 3
        # 4 enable i2c
        self._set_reg(self.IC_ENABLE, 1)

    def available(self):
        """
        Returns True/False on whether there is a message available to be received.
        """
        # get IC_STATUS
        status = mem32[self.i2c_base | self.IC_STATUS]
        # check RFNE receive fifio not empty
        if status & 8:
            return True
        return False

    def read(self):
        """
        Returns one byte sent from the Controller.
        """
        while not self.available():
            pass
        return mem32[self.i2c_base | self.IC_DATA_CMD] & 0xff

    def write(self, data):
        """
        Sends one byte back to the Controller.
        """
        # reset flag
        self._clr_reg(self.IC_CLR_TX_ABRT, 1)
        status = mem32[self.i2c_base | self.IC_CLR_RD_REQ]
        mem32[self.i2c_base | self.IC_DATA_CMD] = data & 0xff

    def any_read(self):
        status = mem32[self.i2c_base | self.IC_RAW_INTR_STAT] & 0x20
        if status:
            return True
        return False
