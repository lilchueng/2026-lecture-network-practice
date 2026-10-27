### Task2
A2: I ran traceroute from my home network rather than the campus Wi‑Fi, so I cannot find the hop where traffic leaves the campus network.
A3: This overseas trace does not expose an obvious trans‑ocean submarine cable hop, several hops show timeout and latency does not have a clear ~100ms jump.
A4: 1.1.1.1 took 4 observable hops. This demonstrates anycast: I connect to the geographically nearest Cloudflare replica.
A5: The `* * *` timeout lines have two causes. First, some routers refuse to send ICMP time‑exceeded packets. Second, actual packet loss on the network link.

B4: I cannot set up the Docker FRR routing environment on this Windows machine, so I did not collect experimental data for this part. Conceptually, reconvergence time is controlled by OSPF dead interval. Routers wait until the dead timer expires before marking a neighbor down.
B5: In theory, link restoration converges faster than link failure detection. Hello packets immediately detect a recovered neighbor, while failure detection relies on the dead timer.
C3: In theory, cost change propagates faster than link failure. Updated link cost is advertised immediately by LSA flooding, and there is no need to wait for the dead timer.