#
# Day 16 Packet Decoder : https://adventofcode.com/2021/day/16
# 

import sys
import time
sys.path.insert(1, '../Libs')
from advent_libs import *
from data_packet_class import *

def hex_to_binary(hex):
    return bin(int(hex, 16))[2:].zfill(4)

def remove_string(binary_string:str, num):
    return binary_string[num:]

def read_char(string, from_pos, num_chars):
    print_assert(from_pos + num_chars <= len(string),"ERROR IN LENGTH")

    char = ""
    for i in range(from_pos,(from_pos+num_chars)):
        char += string[i]
    return char

def read_int(string, from_pos, num_chars):
    char = read_char(string,from_pos,num_chars)
    dec_num = int(char,2)
    return dec_num

# TypeID 4
# Literal values represent a single number 
def get_literal_value(binary_string):
    value = ""
    while ( True ):
        is_end = read_int(binary_string,0,1) 
        value += read_char(binary_string,1,4)
        binary_string = remove_string(binary_string,5)
        if is_end == 0:
            break
    return binary_string,int(value,2)

def create_packet(binary_string):
    packet_version = read_int(binary_string,0,3)
    packet_typeId  = read_int(binary_string,3,3)
    binary_string = remove_string(binary_string,6)
    packet = DataPacket(packet_version,packet_typeId)
    return (binary_string,packet)

def decode_binary_packet(binary_string):

    if ( len ( binary_string ) < 11 ):
        return None

    (binary_string,packet) = create_packet(binary_string)

    if packet.typeId == 4:
        binary_string,value = get_literal_value(binary_string)
        packet.add_number(value)
        return binary_string,packet
    else:

        # Read sub packets
        op_mode = read_int(binary_string,0,1)
        binary_string = binary_string[1:]
        if op_mode == 0:
            binary_string, packet_list = decode_subpackets_by_length(binary_string)
            packet.add_children(packet_list)
        else:
            binary_string, packet_list = decode_subpackets_by_number(binary_string)
            packet.add_children(packet_list)

#    if len(binary_string) > 0 :
#        child = decode_binary_packet(binary_string)
#        if not child is None:
#            packet.add_child(child)

    return (binary_string,packet)

def decode_subpackets_by_length(binary_string):
    packet_list = list()
    length_of_packets = int(read_char(binary_string,0,15),2)
    binary_string = binary_string[15:]
    length_used = 0

    while ( length_used < length_of_packets ):
        binary_string_new, packet = decode_binary_packet(binary_string)
        length_used += len(binary_string) - len(binary_string_new)
        binary_string = binary_string_new
        packet_list.append(packet)
    
    return binary_string,packet_list

def decode_subpackets_by_number(binary_string):
    packet_list = list()
    num_packets = read_char(binary_string,0,11)
    binary_string = binary_string[11:]
    dec_num_packets = int(num_packets,2)            

    for _ in range(dec_num_packets):
        binary_string, packet = decode_binary_packet(binary_string)
        packet_list.append(packet)

    return binary_string, packet_list



def decode_string_packet(string):
    binary_string = ""
    for j in range(len(string)):
        binary_string += str(hex_to_binary(string[j]))
    s,packet = decode_binary_packet(binary_string)
    return packet

def run_literal_sum(binary_string):
    packet = decode_string_packet(binary_string)
    return packet.literal_sum()

def run_version_sum(binary_string):
    packet = decode_string_packet(binary_string)
#    print(packet.to_string())
    return packet.version_sum()

def run_calculate(binary_string):
    packet = decode_string_packet(binary_string)
    #print(packet.to_string())
    return packet.calculate_all()

def run_puzzle1(filename):
    data = loadfile(filename)
    return run_version_sum(data[0])

def run_puzzle2(filename):
    data = loadfile(filename)
    return run_calculate(data[0])

# Unittests for puzzle 1
unittest(run_literal_sum, 2021 , "D2FE28")
unittest(run_literal_sum, 30 , "38006F45291200")
unittest(run_version_sum, 14 , "EE00D40C823060")
unittest(run_version_sum, 16 , "8A004A801A8002F478")
unittest(run_version_sum, 12 , "620080001611562C8802118E34")
unittest(run_version_sum, 23 , "C0015000016115A2E0802F182340")
unittest(run_version_sum, 31 , "A0016C880162017C3686B18A3D4780")

# Unittests for puzzle 2
unittest(run_calculate, 3 , "C200B40A82")
unittest(run_calculate, 54 , "04005AC33890")
unittest(run_calculate, 7 , "880086C3E88112")
unittest(run_calculate, 9 , "CE00C43D881120")
unittest(run_calculate, 1 , "D8005AC2A8F0")
unittest(run_calculate, 0 , "F600BC2D8F")
unittest(run_calculate, 0 , "9C005AC2F8F0")
unittest(run_calculate, 1 , "9C0141080250320F1802104A08")

unittest(run_puzzle1, 886 , "packet_data.txt")
unittest(run_puzzle2, 446899 , "packet_data.txt")

# 13476220616073 <- too high