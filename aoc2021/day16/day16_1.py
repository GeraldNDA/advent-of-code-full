#!/usr/bin/env python3
# Add current dir to path
import sys
from pathlib import Path
sys.path.append(str(Path.cwd()))

# Imports
from aoc import AdventOfCode

from enum import Enum
from itertools import islice
from operator import methodcaller
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
    LITERAL = 4
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
    @staticmethod
    def decode(bitstream):
        # First three bits are version
        version_bits = tuple(islice(bitstream, 3))
        if len(version_bits) != 3:
            assert len(version_bits) == 0, version_bits
            return None
        # print(version_bits)
        version = int_from_bits(version_bits)
        packet_type = int_from_bits(islice(bitstream, 3))
        if packet_type == PacketType.LITERAL.value:
            bit_count = 6
            bits = ""
            done = False
            while not done:
                done = next(bitstream) == "0"
                bits += "".join(islice(bitstream, 4))
                bit_count += 5
            # print(bit_count)
            # print(bits,"|","", end="")
            # for _ in islice(bitstream, -(bit_count) % 4):
            #     print(_, end="")
            #     pass
            # print()
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
# print("".join(as_bitstream(puzzle_input)))
packet = Packet.decode(as_bitstream(puzzle_input))
print(packet.version_sum())