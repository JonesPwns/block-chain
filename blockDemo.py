# *-* coding: utf-8 *-*

import random
import re
import struct
import subprocess
import unittest
from collections import namedtuple
from copy import deepcopy as copy
from datetime import datetime, timedelta, timezone
from hashlib import sha1
from pathlib import Path
from shlex import split
from subprocess import PIPE, CalledProcessError
from sys import byteorder
from tempfile import TemporaryDirectory
from typing import BinaryIO, List, Callable
from uuid import UUID, uuid4
from functools import partial

random.seed()

Block = namedtuple("Block", ["prev_hash", "timestamp", "case_id", "evidence_id", "state", "d_length", "data"])

file_path = 'blockchain_test'

STATE = {
    "init": b"INITIAL\0\0\0\0",
    "in": b"CHECKEDIN\0\0",
    "out": b"CHECKEDOUT\0",
    "dis": b"DISPOSED\0\0\0",
    "des": b"DESTROYED\0\0",
    "rel": b"RELEASED\0\0\0",
    "INITIAL": b"INITIAL\0\0\0\0",
    "CHECKEDIN": b"CHECKEDIN\0\0",
    "CHECKEDOUT": b"CHECKEDOUT\0",
    "DISPOSED": b"DISPOSED\0\0\0",
    "DESTROYED": b"DESTROYED\0\0",
    "RELEASED": b"RELEASED\0\0\0",
}
INITIAL = Block(
    prev_hash=0,  # 20 bytes
    timestamp=0,  # 08 bytes
    case_id=UUID(int=0),  # 16 bytes
    evidence_id=0,  # 04 bytes
    state=STATE["init"],  # 11 bytes
    d_length=14,  # 04 bytes
    data=b"Initial block\0",
)

block_head_fmt = "20s d 16s I 11s I"
block_head_len = struct.calcsize(block_head_fmt)
block_head_struct = struct.Struct(block_head_fmt)

fp = open('./test003','rb')

#======================================================================
# Unpacking the block structure
#======================================================================
block = fp.read(68)
blockContents = block_head_struct.unpack(block)
timestamp = datetime.fromtimestamp(blockContents[1])

print(timestamp)
print(blockContents)

fp.close()


#======================================================================
# packing the structure
#======================================================================
block = Block(
    prev_hash=bytes("0", "utf-8"),  # 20 bytes
    timestamp=0,  # 08 bytes
    case_id=UUID(int=0),  # 16 bytes
    evidence_id=0,  # 04 bytes
    state=STATE["init"],  # 11 bytes
    d_length=14,  # 04 bytes
    data=b"Initial block\0",
)
#block.case_id.int.to_bytes(16, byteorder="little"), #or "big"
block_bytes = block_head_struct.pack(
    b"",
    0,
    bytes("0", "utf-8"),
    0,
    b"INITIAL\0\0\0\0",
    14,

)
pack_data = struct.pack("14s", block.data)
fp = open(file_path, 'ab')
fp.write(block_bytes)
fp.write(pack_data)
fp.close()
with open(file_path, 'rb') as openfileobject:
    block = openfileobject.read(68)
    blockContents = block_head_struct.unpack(block)
    leng = blockContents[5]
    print("length:", leng)
    data_file = openfileobject.read(leng)
    print("Data: ", data_file)
#upack it
#print("contensts NEW!!!!!")
#blockContents_new1 = block_head_struct.unpack(block_bytes)
#print(blockContents_new1)
print("testing")
s = bytes("what", "utf-8")
struct.pack("%ds" % (len(s)),s)
t = struct.unpack("%ds" % (len(s)),s)
print(t[0])
print("more testing")
b="testing"
data_bytes = bytes(b,"utf-8")
data_pack = struct.pack("%ds" %(7),data_bytes)
r = struct.pack("7s", b'232')
q = struct.unpack("7s",r)
print(q[0])