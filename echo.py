#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from controller import DRingCtrl
import time
import qrcode
import signal
from gi.repository import GLib

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Based on:                                                     #
# https://lists.gnu.org/archive/html/jami/2017-05/msg00023.html #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class EchoController(DRingCtrl):
    def __init__(self, accountId):
        super().__init__("EchoController", False)
        self.accountId = accountId

    def onIncomingCall_cb(self, callId):
        self.Refuse(callId)
 
    def onIncomingAccountMessage(self, accountID, messageID, fromAccount, payloads):
        # Avoid to react to message from self.
        if fromAccount == self.accountId:
            return

        # If we have multiple accounts, avoid to react from another account
        if accountID != self.accountId:
            return

        echo = 'Echo: %s' % payloads['text/plain']
        self.sendTextMessage(str(accountID), str(fromAccount), str(echo))

def removePrefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def getOrCreateAccount():
    ctrl = DRingCtrl("Initializing", False)

    ctrl.setHistoryLimit(1)

    accountList = ctrl.getAllEnabledAccounts()
    if accountList.__len__() > 0:
        return accountList[0]

    name = "EchoBot"
    accDetails = {
        'Account.type': 'RING',
        'Account.alias': name,
        'Account.displayName': name,
        'Account.ringtoneEnabled': "false",
        'Account.videoEnabled': 'false',
        'Account.activeCallLimit': '0',
        #'Account.upnpEnabled': 'false',
        #'Account.proxyEnabled': 'true'
    }
    account = ctrl.addAccount(accDetails)

    detail = ctrl.getAccountDetails(account)
    while detail['Account.username'] == '':
        print('Waiting for username')
        time.sleep(1)
        detail = ctrl.getAccountDetails(account)
    
    # Save account to qrcode
    print('Account username: %s.' % str(detail['Account.username']))
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    data = removePrefix(str(detail['Account.username']), "ring:")
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcode.png")

if __name__ == "__main__":
    ctrl = EchoController(getOrCreateAccount())

    def stop(controller, sig):
        controller.stopThread()
        signal.signal(sig, signal.SIG_DFL)

    signal.signal(signal.SIGINT, lambda signal, b : stop(ctrl, signal))
    signal.signal(signal.SIGTERM, lambda signal, b : stop(ctrl, signal))

    ctrl.run()
    GLib.MainLoop().quit()
