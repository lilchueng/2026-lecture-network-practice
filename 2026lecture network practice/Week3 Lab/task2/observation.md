# observation.md
1. Local DNS cache prevents new DNS queries. We must run `ipconfig /flushdns` before experiments to clear cache, otherwise A2/A3/A4 packets cannot be captured.
2. A2 is the client DNS query packet (QR=0). A3 is the DNS server response packet. A4 is the response containing CNAME alias records for CDN steering.
3. DNS uses UDP port 53 for communication. Firewall can easily block UDP packets and lead to DNS timeout.
4. CDN uses CNAME redirection. Based on the geographic location of DNS resolver, CDN schedules nearby edge nodes to decrease access delay.