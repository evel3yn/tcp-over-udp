# Name: Simin Wen
# ID: wens3
# Version: python 3

import socket
import utils
from utils import States
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

# initial server_state
server_state = States.CLOSED

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

sock.bind((UDP_IP, UDP_PORT))  # wait for connection


# Some helper functions to keep the code clean and tidy
def update_server_state(new_state):
    global server_state
    if utils.DEBUG:
        print(server_state, '->', new_state)
    server_state = new_state


# Receive a message and return header, body and addr
# addr is used to reply to the client
# this call is blocking
def recv_msg():
    data, addr = sock.recvfrom(1024)
    header = utils.bits_to_header(data)
    body = utils.get_body_from_data(data)
    return (header, body, addr)


# the server runs in an infinite loop and takes
# action based on current state and updates its state
# accordingly
# You will need to add more states, please update the possible
# states in utils.py file
ack_number = 0
seq_number = 0
while True:
    if server_state == States.CLOSED:
        # we already started listening, just update the state
        update_server_state(States.LISTEN)
    elif server_state == States.LISTEN:
        # we are waiting for a message
        header, body, addr = recv_msg()
        # if received message is a syn message, it's a connection
        # initiation
        if header.syn == 1:
            seq_number = utils.rand_int()  # we randomly pick a sequence number
            ack_number = header.seq_num + 1
            # to be implemented
            update_server_state(States.SYN_RECEIVED)
    ### sending message from the server:
    #   use the following method to send messages back to client
    #   addr is recieved when we receive a message from a client (see above)
    #   sock.sendto(your_header_object.bits(), addr)

    elif server_state == States.SYN_RECEIVED:
        header = utils.Header(seq_number, ack_number, 1, 1, 0)
        sock.sendto(header.bits(), addr)
        update_server_state(States.SYN_SENT)
    elif server_state == States.SYN_SENT:
        header, body, addr2 = recv_msg()
        if addr == addr2 and header.ack == 1 and header.ack_num == seq_number + 1:
            update_server_state(States.ESTABLISHED)
        # if we never met such respond message, it will stuck here, we need a time limit to quit the state
    elif server_state == States.ESTABLISHED:
        header, body, addr3 = recv_msg()
        if addr == addr3 and header.fin == 1:
            seq_number = utils.rand_int()  # we randomly pick a sequence number
            ack_number = header.seq_num + 1
            update_server_state(States.FIN_RCVD)
    elif server_state == States.FIN_RCVD:
        header = utils.Header(seq_number, ack_number, 0, 1, 0)
        sock.sendto(header.bits(), addr3)
        update_server_state(States.CLOSE_WAIT)
    elif server_state == States.CLOSE_WAIT:
        # wait 2MSL
        time.sleep(1)
        seq_number = utils.rand_int()
        ack_number = header.ack_num
        header = utils.Header(seq_number, ack_number, 1, 1, 1)
        update_server_state(States.LAST_ACK)
    elif server_state == States.LAST_ACK:
        header, body, addr4 = recv_msg()
        if addr == addr4 and header.ack == 1 and header.ack_num == seq_number + 1 and header.seq_num == ack_number:
            update_server_state(States.CLOSED)
