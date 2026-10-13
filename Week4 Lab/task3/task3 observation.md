## Task 3 Observation

### R5
Although the baseline FixedWindow achieves the highest goodput, it is the worst sender. It keeps the bottleneck queue permanently full and creates an extremely high packet loss rate (37.4%). Heavy queuing adds large delay to every competing flow sharing the link. This greedy behaviour damages network fairness and overall stability, which caused the famous 1986 Internet congestion collapse.

### Converged window and link relation
My congestion‑control window converges around 21‑23 packets. The link’s bandwidth‑delay product (BDP) is approximately 20 packets. The steady‑state window stays slightly above BDP to fully utilize the pipe, but avoids overfilling the queue.
Experimental result: goodput 912.8 per 1000 slots, loss 1.9%, average queue 4.4. Goodput reaches 93% of baseline.

### Effect of gentler backoff
When using gentler backoff (reduce window less on loss), the goodput increases. The cost is higher average queue occupancy and slightly elevated packet‑loss ratio. If backoff is too mild, loss and queue length will violate the requirements R3 and R4.