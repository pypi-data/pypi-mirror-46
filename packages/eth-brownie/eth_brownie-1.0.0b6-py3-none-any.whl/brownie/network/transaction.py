#!/usr/bin/python3

import threading
import time

import eth_abi
from hexbytes import HexBytes

from .web3 import Web3
from brownie.cli.utils import color
from brownie.exceptions import VirtualMachineError
from brownie.network.history import TxHistory, _ContractHistory
from brownie.network.event import decode_logs, decode_trace
from brownie.project.sources import Sources
from brownie.types import KwargTuple
from brownie.types.convert import format_output
from brownie._config import ARGV, CONFIG


TX_INFO = """
Transaction was Mined{4}
---------------------
{0[key]}Tx Hash{0}: {0[value]}{1.txid}{0}
{0[key]}From{0}: {0[value]}{2}{0}
{0[key]}{3}{0}
{0[key]}Block{0}: {0[value]}{1.block_number}{0}
{0[key]}Gas Used{0}: {0[value]}{1.gas_used}{0} / {0[value]}{1.gas_limit}{0} ({0[value]}{5:.1%}{0})
"""


gas_profile = {}

history = TxHistory()
_contracts = _ContractHistory()
web3 = Web3()
sources = Sources()


class TransactionReceipt:

    '''Attributes and methods relating to a broadcasted transaction.

    * All ether values are given in wei.
    * Before the tx confirms, many values are set to None.
    * trace, revert_msg return_value, and events from a reverted tx
      are only available if debug_traceTransaction is enabled in the RPC.

    Attributes:
        fn_name: Name of the method called in the transaction
        txid: Transaction ID
        sender: Address of the sender
        receiver: Address of the receiver
        value: Amount transferred
        gas_price: Gas price
        gas_limit: Gas limit
        gas_used: Gas used
        input: Hexstring input data
        nonce: Transaction nonce
        txindex: Index of the transaction within the mined block
        contract_address: Address of contract deployed by the transaction
        logs: Raw transaction logs
        status: Transaction status: -1 pending, 0 reverted, 1 successful
        events: Decoded transaction log events
        trace: Stack trace from debug_traceTransaction
        return_value: Returned value from contract call
        revert_msg: Error string from reverted contract all'''

    def __init__(self, txid, sender=None, silent=False, name='', callback=None):
        if type(txid) is not str:
            txid = txid.hex()
        if CONFIG['logging']['tx'] and not silent:
            print("\n{0[key]}Transaction sent{0}: {0[value]}{1}{0}".format(color, txid))
        history._add_tx(self)
        self.__dict__.update({
            '_trace': None,
            'block_number': None,
            'contract_address': None,
            'fn_name': name,
            'gas_limit': None,
            'gas_price': None,
            'gas_used': None,
            'input': None,
            'logs': [],
            'nonce': None,
            'receiver': None,
            'sender': sender,
            'status': -1,
            'txid': txid,
            'txindex': None,
            'value': None
        })
        t = threading.Thread(
            target=self._await_confirm,
            args=[silent, callback],
            daemon=True
        )
        t.start()
        try:
            t.join()
            if ARGV['cli'] == "console":
                return
            if ARGV['coverage']:
                self.trace
            if not self.status:
                raise VirtualMachineError({
                    "message": "revert "+(self.revert_msg or ""),
                    "source": self.error(1)
                })
        except KeyboardInterrupt:
            if ARGV['cli'] != "console":
                raise

    def _await_confirm(self, silent, callback):
        while True:
            tx = web3.eth.getTransaction(self.txid)
            if tx:
                break
            time.sleep(0.5)
        if not self.sender:
            self.sender = tx['from']
        self.__dict__.update({
            'receiver': tx['to'],
            'value': tx['value'],
            'gas_price': tx['gasPrice'],
            'gas_limit': tx['gas'],
            'input': tx['input'],
            'nonce': tx['nonce'],
        })
        if tx['to'] and _contracts.find(tx['to']) is not None:
            self.receiver = _contracts.find(tx['to'])
            if not self.fn_name:
                self.fn_name = "{}.{}".format(
                    self.receiver._name,
                    self.receiver.get_method(tx['input'])
                )
        if not tx['blockNumber'] and CONFIG['logging']['tx'] and not silent:
            print("Waiting for confirmation...")
        receipt = web3.eth.waitForTransactionReceipt(self.txid, None)
        self.__dict__.update({
            'block_number': receipt['blockNumber'],
            'txindex': receipt['transactionIndex'],
            'gas_used': receipt['gasUsed'],
            'contract_address': receipt['contractAddress'],
            'logs': receipt['logs'],
            'status': receipt['status']
        })
        self.events = decode_logs(receipt['logs'])
        if self.fn_name and ARGV['gas']:
            _profile_gas(self.fn_name, receipt['gasUsed'])
        if not silent:
            if CONFIG['logging']['tx'] >= 2:
                self.info()
            elif CONFIG['logging']['tx']:
                print(
                    ("{1} confirmed {2}- {0[key]}block{0}: {0[value]}{3}{0}   "
                     "{0[key]}gas used{0}: {0[value]}{4}{0} ({0[value]}{5:.2%}{0})").format(
                        color,
                        self.fn_name or "Transaction",
                        "" if self.status else "({0[error]}{1}{0}) ".format(
                            color,
                            self.revert_msg or "reverted"
                        ),
                        self.block_number,
                        self.gas_used,
                        self.gas_used / self.gas_limit
                    )
                )
                if receipt['contractAddress']:
                    print("{1} deployed at: {0[value]}{2}{0}".format(
                        color,
                        self.fn_name.split('.')[0],
                        receipt['contractAddress']
                    ))
        if callback:
            callback(self)

    def __repr__(self):
        c = {-1: 'pending', 0: 'error', 1: None}
        return "<Transaction object '{}{}{}'>".format(
            color(c[self.status]), self.txid, color
        )

    def __hash__(self):
        return hash(self.txid)

    def __getattr__(self, attr):
        if attr not in (
            'events',
            'modified_state',
            'return_value',
            'revert_msg',
            'trace',
            '_trace'
        ):
            raise AttributeError("'TransactionReceipt' object has no attribute '{}'".format(attr))
        if self.status == -1:
            return None
        if self._trace is None:
            self._get_trace()
        if attr == "trace":
            self._evaluate_trace()
        return self.__dict__[attr]

    def info(self):
        '''Displays verbose information about the transaction, including
        decoded event logs.'''
        if self.contract_address:
            line = "New Contract Address{0}: {0[value]}{1}".format(color, self.contract_address)
        else:
            line = "To{0}: {0[value]}{1.receiver}{0}\n{0[key]}Value{0}: {0[value]}{1.value}".format(
                color, self
            )
            if self.input != "0x00":
                line += "\n{0[key]}Function{0}: {0[value]}{1}".format(color, self.fn_name)
        print(TX_INFO.format(
            color,
            self,
            self.sender if type(self.sender) is str else self.sender.address,
            line,
            "" if self.status else " ({0[error]}{1}{0})".format(
                color, self.revert_msg or "reverted"
            ),
            self.gas_used / self.gas_limit
        ))
        if self.events:
            print("   Events In This Transaction\n   --------------------------")
            for event in self.events:
                print("   "+color('bright yellow')+event.name+color())
                for k, v in event.items():
                    print("      {0[key]}{1}{0}: {0[value]}{2}{0}".format(
                        color, k, v
                    ))
            print()

    def _get_trace(self):
        '''Retrieves the stack trace via debug_traceTransaction, and finds the
        return value, revert message and event logs in the trace.'''
        self.return_value = None
        self.revert_msg = None
        self._trace = []
        if (self.input == "0x" and self.gas_used == 21000) or self.contract_address:
            self.modified_state = False
            self.trace = []
            return
        trace = web3.providers[0].make_request(
            'debug_traceTransaction',
            [self.txid, {}]
        )
        if 'error' in trace:
            self.modified_state = None
            raise ValueError(trace['error']['message'])
        self._trace = trace = trace['result']['structLogs']
        if self.status:
            # get return value
            self.modified_state = bool(next((i for i in trace if i['op'] == "SSTORE"), False))
            log = trace[-1]
            if log['op'] != "RETURN":
                return
            contract = self.contract_address or self.receiver
            if type(contract) is str:
                return
            abi = [
                i['type'] for i in
                getattr(contract, self.fn_name.split('.')[-1]).abi['outputs']
            ]
            offset = int(log['stack'][-1], 16) * 2
            length = int(log['stack'][-2], 16) * 2
            data = HexBytes("".join(log['memory'])[offset:offset+length])
            self.return_value = eth_abi.decode_abi(abi, data)
            if not self.return_value:
                return
            if len(self.return_value) == 1:
                self.return_value = format_output(self.return_value[0])
            else:
                self.return_value = KwargTuple(
                    self.return_value,
                    getattr(contract, self.fn_name.split('.')[-1]).abi
                )
        else:
            # get revert message
            self.modified_state = False
            self.revert_msg = ""
            if trace[-1]['op'] == "REVERT":
                offset = int(trace[-1]['stack'][-1], 16) * 2
                length = int(trace[-1]['stack'][-2], 16) * 2
                if length:
                    data = HexBytes("".join(trace[-1]['memory'])[offset+8:offset+length])
                    self.revert_msg = eth_abi.decode_abi(["string"], data)[0].decode()
            # get events from trace
            self.events = decode_trace(trace)

    def _evaluate_trace(self):
        '''Adds the following attributes to each step of the stack trace:

        address: The address executing this contract.
        contractName: The name of the contract.
        fn: The name of the function.
        source: Start and end offset associated source code.
        jumpDepth: Number of jumps made since entering this contract. The
                   initial value is 1.'''
        self.trace = trace = self._trace
        if not trace:
            return
        contract = self.contract_address or self.receiver
        pc = contract._build['pcMap'][0]
        fn = sources.get_contract_name(pc['contract'], pc['start'], pc['stop'])
        fn += "."+self.fn_name.split('.')[-1]
        last_map = {0: {
            'address': contract.address,
            'contract': contract,
            'fn': [fn],
        }}
        trace[0].update({
            'address': last_map[0]['address'],
            'contractName': last_map[0]['contract']._name,
            'fn': last_map[0]['fn'][-1],
            'jumpDepth': 1,
            'source': {
                'filename': pc['contract'],
                'start': pc['start'],
                'stop': pc['stop']
            }
        })
        for i in range(1, len(trace)):
            # if depth has increased, tx has called into a different contract
            if trace[i]['depth'] > trace[i-1]['depth']:
                address = web3.toChecksumAddress(trace[i-1]['stack'][-2][-40:])
                contract = _contracts.find(address)
                stack_idx = -4 if trace[i-1]['op'] in ('CALL', 'CALLCODE') else -3
                memory_idx = int(trace[i-1]['stack'][stack_idx], 16) * 2
                sig = "0x" + "".join(trace[i-1]['memory'])[memory_idx:memory_idx+8]
                pc = contract._build['pcMap'][trace[i]['pc']]
                fn = sources.get_contract_name(pc['contract'], pc['start'], pc['stop'])
                fn += "."+(contract.get_method(sig) or "")
                last_map[trace[i]['depth']] = {
                    'address': address,
                    'contract': contract,
                    'fn': [fn],
                    }
            last = last_map[trace[i]['depth']]
            contract = last['contract']
            trace[i].update({
                'address': last['address'],
                'contractName': contract._name,
                'fn': last['fn'][-1],
                'jumpDepth': len(set(last['fn']))
            })
            pc = contract._build['pcMap'][trace[i]['pc']]
            trace[i]['source'] = {
                'filename': pc['contract'],
                'start': pc['start'],
                'stop': pc['stop']
            }
            # jump 'i' is moving into an internal function
            if pc['jump'] == 'i':
                last['fn'].append(pc['fn'] or last['fn'][-1])
            # jump 'o' is coming out of an internal function
            elif pc['jump'] == "o" and len(['fn']) > 1:
                del last['fn'][-1]

    def call_trace(self):
        '''Displays the sequence of contracts and functions called while
        executing this transaction, and the structLog index where each call
        or jump occured. Any functions that terminated with REVERT or INVALID
        opcodes are highlighted in red.'''
        trace = self.trace
        sep = max(i['jumpDepth'] for i in trace)
        idx = 0
        for i in range(1, len(trace)):
            if (
                trace[i]['depth'] == trace[i-1]['depth'] and
                trace[i]['jumpDepth'] == trace[i-1]['jumpDepth']
            ):
                continue
            _print_path(trace[i-1], idx, sep)
            idx = i
        _print_path(trace[-1], idx, sep)

    def error(self, pad=3):
        '''Displays the source code that caused the transaction to revert.

        Args:
            pad: Number of unrelated lines of code to include before and after
        '''
        try:
            idx = self.trace.index(next(i for i in self.trace if i['op'] in ("REVERT", "INVALID")))
        except StopIteration:
            return ""
        while True:
            if idx == -1:
                return ""
            trace = self.trace[idx]
            if not trace['source']['filename']:
                idx -= 1
                continue
            span = (trace['source']['start'], trace['source']['stop'])
            if sources.get_fn(trace['source']['filename'], span[0], span[1]) != trace['fn']:
                idx -= 1
                continue
            return self.source(idx)

    def source(self, idx, pad=3):
        '''Displays the associated source code for a given stack trace step.

        Args:
            idx: Stack trace step index
            pad: Number of unrelated lines of code to include before and after
        '''
        trace = self.trace[idx]
        if not trace['source']['filename']:
            return ""
        source = sources[trace['source']['filename']]
        span = (trace['source']['start'], trace['source']['stop'])
        newlines = [i for i in range(len(source)) if source[i] == "\n"]
        try:
            start = newlines.index(next(i for i in newlines if i >= span[0]))
            stop = newlines.index(next(i for i in newlines if i >= span[1]))
        except StopIteration:
            return ""
        ln = start + 1
        start = newlines[max(start-(pad+1), 0)]
        stop = newlines[min(stop+pad, len(newlines)-1)]
        result = ((
            'Source code for trace step {0[value]}{4}{0}:\n  File {0[string]}' +
            '"{1}"{0}, line {0[value]}{2}{0}, in {0[callable]}{3}{0}:'
        ).format(color, trace['source']['filename'], ln, trace['fn'], idx))
        result += ("{0[dull]}{1}{0}{2}{0[dull]}{3}{0}".format(
            color,
            source[start:span[0]],
            source[span[0]:span[1]],
            source[span[1]:stop]
        ))
        return result


def _print_path(trace, idx, sep):
    col = "error" if trace['op'] in ("REVERT", "INVALID") else "pending"
    name = "{}{}".format(trace['fn'], color(col))
    print(
        ("  "*sep*trace['depth']) + ("  "*(trace['jumpDepth']-1)) +
        "{}{} {}{} ({})".format(color(col), name, color('dull'), idx, trace['address']) +
        color()
    )


def _profile_gas(fn_name, gas_used):
    gas_profile.setdefault(
        fn_name,
        {
            'avg': 0,
            'high': 0,
            'low': float('inf'),
            'count': 0
        }
    )
    gas = gas_profile[fn_name]
    gas.update({
        'avg': (gas['avg']*gas['count'] + gas_used) / (gas['count']+1),
        'high': max(gas['high'], gas_used),
        'low': min(gas['low'], gas_used)
    })
    gas['count'] += 1
