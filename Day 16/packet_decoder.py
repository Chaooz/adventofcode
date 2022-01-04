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

def read_char(string, from_pos, num_chars):
    char = ""

    if ( from_pos + num_chars > len(string )):
        print("ERROR IN LENGTH")
        return char

    for i in range(from_pos,(from_pos+num_chars)):
        char += string[i]
    #print("CHAR:" + char)
    return char

def read_int(string, from_pos, num_chars):
    char = read_char(string,from_pos,num_chars)
    dec_num = int(char,2)
    #print("read int: " + char + " => " + str(dec_num))
    return dec_num

def remove_string(binary_string:str, num):
    return binary_string[num:]

# TypeID 4
# Literal values represent a single number 
def read_literal(packet:DataPacket,binary_string):
    block_list = ""
    while ( True ):
        is_end = read_int(binary_string,0,1) 
        block = read_char(binary_string,1,4)
        block_list += block
        binary_string = remove_string(binary_string,5)
        packet.add_block("read_literal",0,block)
        if is_end == 0:
            break

    if len(block_list) > 0:
        number = int(block_list,2)
        packet.add_number(number)
    return binary_string

def read_operator(packet:DataPacket,binary_string):

    op_mode = read_int(binary_string,0,1)
    if op_mode == 0:
        bits = read_char(binary_string,1,15)
        dec_packet_length = int(bits,2)
        block = read_char(binary_string,16,dec_packet_length)
        binary_string = remove_string(binary_string, 16+dec_packet_length)
        packet.add_block("Operator 0 (" + str(dec_packet_length) + ")",dec_packet_length,block)
    else:
        num_packets = read_char(binary_string,1,11)
        dec_num_packets = int(num_packets,2)
        binary_string = binary_string[12:]
        #print("OP with num packets:" + str(dec_num_packets))
        packet.add_block("Operator 1 (" + str(dec_num_packets) + ")",dec_num_packets,binary_string)
        binary_string = ""
   
    return binary_string

def read_packet(binary_string, packet):
    packet_version = read_int(binary_string,0,3)
    packet_typeId  = read_int(binary_string,3,3)
    binary_string = remove_string(binary_string,6)
    packet = DataPacket(packet_version,packet_typeId)

    # Sum packets
    if packet_typeId == 4:
#        if packet is None:
#        packet = DataPacket(packet_version,packet_typeId)
        binary_string = read_literal(packet,binary_string)
    else:
#        packet = DataPacket(packet_version,packet_typeId)
        binary_string = read_operator(packet,binary_string)
    return (binary_string,packet)

def decode_binary_packet(binary_string, packet):

    if ( len ( binary_string ) < 11 ):
        return None

    (binary_string,new_packet) = read_packet(binary_string,packet)

    #if packet is None:
    #    print("change packet")
    packet = new_packet

    # Read sub packets
    for (d,block) in packet.blocks:
        child_packet = decode_binary_packet(block,packet)
        if not child_packet is None:
            packet.add_child(child_packet)

    if len(binary_string) > 0 :
        p = decode_binary_packet(binary_string, packet)
        if not p is None:
            packet.add_child(p)
#            print("P:" + p.to_string())

    return packet

def decode_string_packet(string):
    binary_string = ""
    for j in range(len(string)):
        binary_string += str(hex_to_binary(string[j]))
    return decode_binary_packet(binary_string, None)

def run_literal_sum(binary_string):
    packet = decode_string_packet(binary_string)
    return packet.literal_sum()

def run_version_sum(binary_string):
    packet = decode_string_packet(binary_string)
    return packet.version_sum()

def run_calculate(binary_string):
    packet = decode_string_packet(binary_string)
    print(packet.to_string())
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

#unittest(run_puzzle1, 886 , "packet_data.txt")
#unittest(run_puzzle2, 886 , "packet_data.txt")
