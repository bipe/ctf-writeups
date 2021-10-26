from scapy.all import *
packets = rdpcap('./filtered.pcapng')
data = b""
#0 to 41 because there are only the filtered packets in this .pcapng file
i = 0  
while i<=41:
	data += raw(packets[i])[64:]
	i+=1
f = open("zipped", "wb")
f.write(data)