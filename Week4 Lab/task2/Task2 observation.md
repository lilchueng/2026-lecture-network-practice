# Task 2 Observation
## Part A
A2:
- SYN: packet number = 10
- SYN‑ACK: packet number = 11
- ACK: packet number = 12

A3:
Client initial sequence number: 4281312351
Server initial sequence number: 158812640

The initial sequence numbers are not zero.
The ISN is randomly generated for each new connection. This prevents sequence number prediction attacks, and avoids ambiguity between delayed old packets and new TCP connections.

A4:
MSS: 1460 bytes
Window scale factor: 256
SACK permitted: Yes

A5:
Scaled advertised receive window = raw window value × 2^(window scale factor).
The receiver’s advertised window is large enough, so it is not the bottleneck.
The actual limiting factor is bandwidth‑delay product and round‑trip time (RTT). According to §3.7, maximum throughput = window / RTT. Even if the link capacity is high, large RTT restricts throughput.

## Part B
B1: Two network labels: campus wifi, tethering (phone hotspot).
B2: 5 measurements collected for each network.

B3:
Campus wifi:
    Median throughput: 43.40 Mbps
    Spread: min = 31.9 Mbps, max = 78.22 Mbps
    Median handshake time: 27.8 ms

Tethering:
    Median throughput: 53.89 Mbps
    Spread: min = 39.0 Mbps, max = 58.67 Mbps
    Median handshake time: 65.0 ms

B4:
The spread between repeated measurements comes from variable wireless interference, network queueing delay, background traffic on the link, and dynamic server load. These transient network conditions change for every trial, leading to different measured throughput.
Campus‑wifi shows extremely high spread (106%). Many students share the same wireless access point; competing background traffic causes heavy queueing and large performance fluctuation across runs. Tethering has much lower spread (25%) because fewer devices compete for the mobile link.

B5:
Handshake time and throughput are not independent. Longer handshake time means larger RTT.
From §3.7, throughput is bounded by window size divided by RTT.
Higher RTT reduces bandwidth‑delay product, which limits maximum throughput even if raw physical link capacity is the same.
In our result, tethering obtains higher median throughput but suffers a much larger TCP‑handshake RTT compared with campus‑wifi. This illustrates that link bit‑rate alone cannot determine real TCP performance; round‑trip delay plays a critical role.