# Name: Simin Wen
# ID: wens3
# Version: python 3
from enum import Enum
import random

DEBUG = True


# Extend the possible states based on your implementation
# Refer TCP protocol
class States(Enum):
    CLOSED, LISTEN, SYN_RECEIVED, SYN_SENT, ESTABLISHED, FIN_RCVD, CLOSE_WAIT, LAST_ACK, FIN_WAIT_1, FIN_WAIT_2 = range(
        1, 11)


class Header:
    def __init__(self, seq_num, ack_num, syn, ack, fin):
        self.seq_num = seq_num
        self.ack_num = ack_num
        self.syn = syn
        self.ack = ack
        self.fin = fin

    def __str__(self):
        return pretty_bits_print(self.bits().decode())

    def bits(self):
        # '0:032b' 032 is 32 bit, b is binary
        # it will only add 0 when bit is redundant, it will not work when exceeding the limit
        bits = '{0:032b}'.format(self.seq_num)
        bits += '{0:032b}'.format(self.ack_num)
        bits += '{0:01b}'.format(self.syn)
        bits += '{0:01b}'.format(self.ack)
        bits += '{0:01b}'.format(self.fin)
        bits += '{0:030b}'.format(0)
        if (DEBUG):
            print(pretty_bits_print(bits))
        return bits.encode()


def bits_to_header(bits):
    bits = bits.decode()
    # [:32] is 0-31
    # int(bits[], 2), 2 is binary
    seq_num = int(bits[:32], 2)
    ack_num = int(bits[32:64], 2)
    syn = int(bits[64], 2)
    ack = int(bits[65], 2)
    fin = int(bits[66], 2)
    return Header(seq_num, ack_num, syn, ack, fin)


# Returns the bits beyond the first 12 bytes
# If your header is 12 bytes, it returns the body of a message
def get_body_from_data(data):
    data = data.decode()
    return data[96:]


# Used for debugging
# It pretty prints header of a message
def pretty_bits_print(bits):
    seq_num = bits[:32]
    ack_num = bits[32:64]
    row_3 = bits[64:]
    output = [seq_num + " : seq_num = {0}".format(int(seq_num, 2)),
              ack_num + " : ack_num = {0}".format(int(ack_num, 2)),
              row_3 + " : syn = {0}, ack = {1}, fin = {2}".format(row_3[0], row_3[1], row_3[2])]
    return '\n'.join(output)


# We rather using small values for number generation
# to make it easier to keep track of for the assignment
def rand_int(power=5):
    return random.randint(0, (2 ** power) - 1)
