## Task1: Iterative DNS Resolver
This program implements iterative DNS lookup starting from root DNS servers.
Root servers do not return target domain IP directly. They return NS records delegating to TLD nameservers.
The resolver then queries TLD server, which delegates to the authoritative nameserver of the target domain.
If NS records do not come with glue A records, the program needs to resolve the nameserver domain first to get its IP.
If one DNS server fails or times out, the program will try the next available server.
A maximum depth limit prevents infinite loops caused by CNAME loops.
CDN domains like www.microsoft.com may return different IP addresses on different queries, as CDN uses distributed edge servers.