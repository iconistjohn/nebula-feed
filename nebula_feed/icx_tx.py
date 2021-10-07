import json
from datetime import datetime
from iconsdk.icon_service import IconService
from iconsdk.providers.http_provider import HTTPProvider
from iconsdk.builder.call_builder import CallBuilder
from iconsdk.exception import JSONRPCException

# connect to ICON main-net
icon_service = IconService(HTTPProvider("https://ctz.solidwallet.io", 3))

# util function
def hex_to_int(hex) -> int:
    return int(hex, 16)

# not used atm..
class IcxBlock:
    def __init__(self) -> None:
        self.block_height = icon_service.get_block("latest")["height"]
        self.block = icon_service.get_block(self.block_height)

    def get_latest_block(self) -> dict:
        return icon_service.get_block("latest")

    def get_block(self, block: int) -> dict:
        return icon_service.get_block(block)
        
    def get_tx_result(self, tx_hash: str) -> dict:
        return icon_service.get_transaction_result(tx_hash)

    def call(self, to, method, params=None):
        try:
            call = CallBuilder().to(to).method(method).params(params).build()
            result = icon_service.call(call)
            return result
        except JSONRPCException as e:
            raise Exception(e)

# class to collect info available in icx transaction
class TxInfo:
    def __init__(self, tx: json) -> None:
        self.txHash = str(tx["txHash"])
        self.contract = str(tx["to"])
        self.address = str(tx["from"])
        #self.timestamp = datetime.fromtimestamp(tx["timestamp"] / 1000000).replace(microsecond=0).isoformat()
        self.timestamp = int(tx["timestamp"] / 1000000)
        self.cost = "{:.2f}".format(int(tx["value"]) / 10 ** 18)
        self.method = tx["data"]["method"]
        self.tokenId = int(tx["data"]["params"]["_token_id"], 16)

        if self.method == "create_auction":
            self.set_price = ""
            self.starting_price = str(hex_to_int(tx["data"]["params"]["_starting_price"]) / 10 ** 18)
            self.duration_in_hours = str(hex_to_int(tx["data"]["params"]["_duration_in_hours"]))
        elif self.method == "list_token":
            self.set_price = str(hex_to_int(tx["data"]["params"]["_price"]) / 10 ** 18)
            self.starting_price = ""
            self.duration_in_hours = ""
        else:
            self.set_price = ""
            self.starting_price = ""
            self.duration_in_hours = ""
