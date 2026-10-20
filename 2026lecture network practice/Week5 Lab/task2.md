# Task 2 Report

## Part A: Campus Wi‑Fi
A1. Interface IPv4 address: 192.168.31.133; Subnet mask: 255.255.255.0.

A2. Subnet is 192.168.31.0/24. Network address: 192.168.31.0, first usable host: 192.168.31.1, last usable host: 192.168.31.254, broadcast address: 192.168.31.255. This result is verified and matches the network_range function from Task 1.

A3. Default gateway: 192.168.31.1. The gateway is inside this subnet. It must reside in the same local subnet because the host uses ARP (Layer‑2 broadcast) to resolve the gateway’s MAC address; ARP cannot cross subnet boundaries.

A4. Public IP observed from the external server: 175.203.115.142.

A5. The local address 192.168.31.133 is an RFC1918 private address. Since the private IP differs from the public IP, NAT is used. The campus router translates private local addresses into the public ISP address for internet communication.

## Part B: Phone Tethering
B2.
- Campus Wi‑Fi: private 192.168.31.133, mask 255.255.255.0, gateway 192.168.31.1, public 175.203.115.142
- Phone tethering: private 172.20.10.2, mask 255.255.255.240, gateway 172.20.10.1, public 211.36.143.137

B3.
Private IPv4 addresses differ because the DHCP servers on the campus router and mobile hotspot assign addresses from separate private pools. Subnet sizes also differ: campus Wi‑Fi uses a /24 subnet for many clients, while the phone hotspot uses a smaller /28 subnet with only 14 usable hosts.
The public IPs are different as well. Campus Wi‑Fi uses the campus ISP’s public address, and phone tethering uses the mobile carrier’s public IP. Both connections rely on NAT to map private addresses to public internet addresses.

## Part C: DHCP Capture
C1. The captured pcapng contains the full DHCP DORA sequence: Discover, Offer, Request, and Acknowledge.

C2. In the DHCP Discover packet, the source IP is 0.0.0.0 and the destination is the broadcast address 255.255.255.255. The client has no valid IP yet, so it broadcasts to locate any available DHCP server on the local LAN.

C3. The DHCP server offers an IP lease. In my capture, the lease time is 3600 seconds (1 hour).

C4. The Discover message must be broadcast, since the client lacks an IP address. By the time the server sends the ACK, the client has requested a specific IPv4 address. The DHCP server may unicast the ACK directly to that requested address. When half of the lease time passes, the client will initiate lease renewal.