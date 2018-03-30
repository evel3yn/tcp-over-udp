# TCP OVER UDP

## Modifications

### utils file

- Add states in class States
```py
 CLOSED, LISTEN, SYN_RECEIVED, SYN_SENT, ESTABLISHED, FIN_RCVD, CLOSE_WAIT, LAST_ACK, FIN_WAIT_1, FIN_WAIT_2 = range(1, 11)
```
- Add fin in class Header, including constructor, bits(), bits_to_header(), pretty_bits_print(bits) functions

### server file
- Finished code in while loop, including 3-way handshake and 4-way teardown

### client file
- Finished code in class Client, including handshake(self) and terminate(self)
- I didn't use multi-process related function