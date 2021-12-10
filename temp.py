# print_eth_json.py
import json
import subprocess as sp
import pprint

json_str = sp.check_output("tshark -c 2 -T json".split(' ')).decode('utf-8')
tshark_pkts = json.loads(json_str)
# Transform tshark json into a scapy-like packet-json list.
pkts_json = [pkt['_source']['layers'] for pkt in tshark_pkts]
# pprint.pprint(pkts_json[0])
print(pkts_json[0])