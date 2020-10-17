#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from controller import DRingCtrl

# based on:
# https://lists.gnu.org/archive/html/jami/2017-05/msg00023.html
#

class EchoController(DRingCtrl):
    def __init__(self):
        super().__init__("EchoController", False)
        self.accountId = self.configurationmanager.getAccountList()[0]

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
 
if __name__ == "__main__":
    ctrl = EchoController()
    # before running needs to: register ringid or use first registered account
    # it may also need to save the information
    ctrl.run()
