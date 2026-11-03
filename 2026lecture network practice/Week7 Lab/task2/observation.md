## Task2
1. The first entry to come back, and why it had to be that one
The gateway entry (192.168.31.1) returned first. When we ping the gateway, our host needs the gateway’s MAC address to send packets out of the local subnet. ARP is triggered for the gateway immediately, so this entry is refilled first.

2. Why a server on the other side of the world is not in your ARP table
ARP only resolves IP addresses within the same local Layer 2 LAN. The remote web server is on a different network. Our host only needs the gateway’s MAC to forward packets toward the internet; ARP is never used for remote public IPs.

3. The two destination addresses from B2, and what each one means
The ARP request destination MAC is `ff:ff:ff:ff:ff:ff`, the broadcast MAC. This means every device on this WiFi LAN will receive the request.
The ARP reply destination MAC is our laptop’s unicast MAC. This means only our host, the sender of the ARP request, receives the reply.