
"""
    IoTeX API
    ===============
"""

import math
from iotexapi.module import Module
from iotexapi.proto.api import api_pb2 as api

import logging
from collections import namedtuple
from iotexapi.proto.api.api_pb2_grpc import APIServiceStub

from iotexapi.proto.types import action_pb2 as actions

from iotexapi.common.account import Account, PrivateKey
from iotexapi.common.toolz import (
    assoc
)

from eth_utils import (
    to_hex, keccak
)

import grpc

log = logging.getLogger(__name__)


class Iotx(object):
    
    def __init__(self, iotex, node_api):
        """
         Args:
            node_api (str):  GRPC of the node to connect to.
        """
        self.iotex = iotex

        # open a gRPC channel
        self.channel = grpc.insecure_channel(node_api['api'])
        self.stub = APIServiceStub(self.channel)

    def getAccount(self, address=None):
        if address==None:
            address = self.iotex.default_address.io
        return self.stub.GetAccount(api.GetAccountRequest(address=address))

    def getActionsByIndexRequest(self, start=0, count=10):
        byIndex=api.GetActionsByIndexRequest(start=start, count=count)
        return self.stub.GetActions(api.GetActionsRequest(byIndex=byIndex))

    def getActionByHashRequest(self, actionHash, checkPending=False):
        byHash=api.GetActionByHashRequest(actionHash=actionHash, checkPending=checkPending)
        return self.stub.GetActions(api.GetActionsRequest(byHash=byHash))

    def getActionsByAddress(self, address, start=0, count=10):
        byAddr=api.GetActionsByAddressRequest(address=address, start=start, count=count)
        return self.stub.GetActions(api.GetActionsRequest(byAddr=byAddr))
    
    def getUnconfirmedActionsByAddressRequest(self, address, start=0, count=10):
        unconfirmedByAddr=api.GetUnconfirmedActionsByAddressRequest(address=address, start=start, count=count)
        return self.stub.GetActions(api.GetActionsRequest(unconfirmedByAddr=unconfirmedByAddr))

    def getActionsByBlockRequest(self, blkHash, start=0, count=10):
        byBlk=api.GetActionsByBlockRequest(blkHash=blkHash, start=start, count=count)
        return self.stub.GetActions(api.GetActionsRequest(byBlk=byBlk))

    def getBlockMetas(self, hash=None, start=None, count=None):
        if not start==None and not count==None:
            return self.stub.GetBlockMetas(api.GetBlockMetasRequest(byIndex=api.GetBlockMetasByIndexRequest(start=start, count=count)))
        elif hash:
            return self.stub.GetBlockMetas(api.GetBlockMetasRequest(byHash=api.GetBlockMetaByHashRequest(blkHash=hash)))
        else:
            return None

    def getChainMeta(self):
        return self.stub.GetChainMeta(api.GetChainMetaRequest())

    def getEpochMeta(self, epoch):
        return self.stub.GetEpochMeta(api.GetEpochMetaRequest(epochNumber=epoch))

    def getReceiptByAction(self, actionHash):
        return self.stub.GetReceiptByAction(api.GetReceiptByActionRequest(actionHash=actionHash))

    def transferTo(self, to, amount, options=None):
        if options is None:
            options = {}

        if 'from' not in options:
            options = assoc(options, 'from', self.iotex.default_address.io)

        action = actions.Action(core=self.actionCore(options))

        transfer = actions.Transfer(amount=str(amount), recipient=to)
        if 'message' in options:
            transfer.payload = bytes(str.encode(options['message']))

        action.core.transfer.CopyFrom(transfer)
        result = self.sign_broadcast(action)

        return result

    def claimRewards(self, amount, options=None):
        if options is None:
            options = {}

        action = actions.Action(core=self.actionCore(options))

        claim = actions.ClaimFromRewardingFund(amount=str(amount))
        if 'message' in options:
            claim.data = bytes(str.encode(options['message']))

        action.core.claimFromRewardingFund.CopyFrom(claim)
        result = self.sign_broadcast(action)

        return result
    
    def sign_broadcast(self, action):

        if not action.core.gasLimit:
            txId = keccak(action.core.SerializeToString()).hex()
            signature = Account.sign_hash(txId, self.iotex.private_key)
            action.signature = signature.signature[0:64]+bytes([ord(signature.signature[64:65])-27])
            action.senderPubKey = bytes.fromhex(
                PrivateKey(self.iotex.private_key).public_key
            )
            
            gasLimit = self.stub.EstimateGasForAction(api.EstimateGasForActionRequest(action=action))
            action.core.gasLimit = gasLimit.gas

        txId = keccak(action.core.SerializeToString()).hex()
        signature = Account.sign_hash(txId, self.iotex.private_key)
        
        action.signature = signature.signature[0:64]+bytes([ord(signature.signature[64:65])-27])
        
        action.senderPubKey = bytes.fromhex(
            PrivateKey(self.iotex.private_key).public_key
        )
        toSend = api.SendActionRequest(action=action)
        result = self.stub.SendAction(toSend)

        return result

    def actionCore(self, options=None) -> actions.ActionCore:
        nonce=1
        gasLimit=None
        gasPrice=1

        if 'nonce' in options:
            nonce = options['nonce']
        else:
            account = self.getAccount()
            nonce = account.accountMeta.pendingNonce
        
        if 'gasLimit' in options:
            gasLimit=options['gasLimit']            
        
        if 'gasPrice' in options:
            gasPrice=options['gasPrice']
        else:
            suggestGasPrice = self.stub.SuggestGasPrice(api.SuggestGasPriceRequest())
            gasPrice = suggestGasPrice.gasPrice
            
        return  actions.ActionCore(version=1,nonce=nonce,
            gasLimit=gasLimit, gasPrice=str(gasPrice))
        
        



