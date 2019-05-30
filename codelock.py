# -*- coding: utf-8 -*-

from Crypto.Cipher import AES
from binascii import a2b_hex, b2a_hex

class CodeLock():

    def topassword(self, mingwen, miwen):
        mkey = 'wuhanyushengYSOD'
        miv = 'YSODwuhanyusheng'
        aes = AES.new(mkey.encode(), 2, miv.encode())
        if len(mingwen.encode()) > 0:
            yushu = 16 - len(mingwen.encode()) % 16
            mingwen1 = mingwen + '_' * yushu
            miwen = aes.encrypt(mingwen1.encode())
            return b2a_hex(miwen).decode()

        elif len(mingwen) == 0 and len(miwen) > 0:
            return aes.decrypt(a2b_hex(miwen)).decode().strip('_')
