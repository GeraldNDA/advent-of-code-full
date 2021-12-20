#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from enum import Enum
from itertools import islice
import operator
from operator import methodcaller
from functools import reduce
# Input Parse
puzzle = AdventOfCode(year=2021, day=16)
puzzle_input = puzzle.get_input()

# Actual Code
def int_from_bits(bitstream):
    return int("".join(bitstream), 2)

def as_bitstream(transmission):
    binary_transmission = f"{int(transmission, 16):b}"
    binary_transmission = "0"*(-len(binary_transmission) % 4) + binary_transmission
    return iter(binary_transmission)

class PacketType(Enum):
    SUM = 0
    PRODUCT = 1
    MIN = 2
    MAX = 3
    LITERAL = 4
    GT = 5
    LT = 6
    EQ = 7

    def get_func(self):
        if self is PacketType.SUM:
            return operator.add
        if self is PacketType.PRODUCT:
            return operator.mul
        if self is PacketType.MIN:
            return min
        if self is PacketType.MAX:
            return max
        if self is PacketType.GT:
            return operator.gt
        if self is PacketType.LT:
            return operator.lt
        if self is PacketType.EQ:
            return operator.eq
        return None

    def is_pairwise_op(self):
        return self.value in (PacketType.GT, PacketType.LT, PacketType.EQ)



    def apply(self, val):
        packet_op = self.get_func()
        if not packet_op:
            assert type(val) in (int, Packet)
            return val if type(val) is int else val.effective_val()
        assert type(val) is tuple
        val = tuple(map(lambda v: v if type(v) is int else v.effective_val(), val))
        if self.is_pairwise_op():
            assert len(val) == 2
            return val[0] if packet_op(*val) else val[1]
        else:
            return reduce(packet_op, val)
    # Assume there will be more to add here

class Packet:
    def __init__(self, version, type, value) -> None:
        self.version = version
        self.type = type
        self.value = value
    
    def __repr__(self) -> str:
        return f"Packet(version={self.version}, type={self.type}, value={self.value})"

    def version_sum(self):
        if type(self.value) is tuple:
            return self.version + sum(map(methodcaller("version_sum"), self.value))
        else:
            return self.version

    def effective_val(self):
        if type(self.value) is tuple:
            return self.type.apply(self.value)
        else:
            return self.value
    @staticmethod
    def decode(bitstream):
        # First three bits are version
        version_bits = tuple(islice(bitstream, 3))
        if len(version_bits) != 3:
            assert len(version_bits) == 0, version_bits
            return None
        version = int_from_bits(version_bits)
        packet_type = PacketType(int_from_bits(islice(bitstream, 3)))
        if packet_type is PacketType.LITERAL:
            bit_count = 6
            bits = ""
            done = False
            while not done:
                done = next(bitstream) == "0"
                bits += "".join(islice(bitstream, 4))
                bit_count += 5
            return Packet(version=version, type=packet_type, value=int(bits, 2))
        else:
            # Operator packet
            if next(bitstream) == "0":
                packet_len = int_from_bits(islice(bitstream, 15))
                sub_packets = islice(bitstream, packet_len)
                packets = tuple()
                done = False
                while not done:
                    packet = Packet.decode(sub_packets)
                    if not packet:
                        return Packet(version=version, type=packet_type, value=packets)
                    packets += (packet,)
            else:
                num_packets = int_from_bits(islice(bitstream, 11))
                return Packet(version=version, type=packet_type, value=tuple(Packet.decode(bitstream) for _ in range(num_packets)))

# Result
packet = Packet.decode(as_bitstream(puzzle_input))
print(packet.effective_val())