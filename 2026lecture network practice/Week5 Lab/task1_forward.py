#!/usr/bin/env python3
"""Week 5 · Task 1 — Subnets and longest-prefix match.

Textbook §4.3.2 (IPv4 addressing, CIDR) and §4.3.3 (forwarding).

Two things a router does with every packet: work out which prefixes the
destination falls inside, and pick the longest one. The second is the whole
of "longest prefix match", and it is the reason the internet's routing table
can hold a million entries and still be answerable.

You build both, from integers up. No `ipaddress` module - that library is
exactly the thing you are supposed to understand this week.

    python3 task1_forward.py --verify
"""
import argparse


# ---------------- 内部辅助函数（禁止使用库） ----------------
def _ip_str_to_int(ip_str: str) -> int:
    """把 "a.b.c.d" IPv4字符串转为32位无符号整数"""
    octets = list(map(int, ip_str.split(".")))
    if len(octets) != 4 or any(o < 0 or o > 255 for o in octets):
        raise ValueError("Invalid IPv4 address")
    return (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]


def _int_to_ip_str(num: int) -> str:
    """32位整数转回 IPv4字符串 a.b.c.d"""
    num = num & 0xFFFFFFFF  # 保证是32位无符号
    o1 = (num >> 24) & 0xFF
    o2 = (num >> 16) & 0xFF
    o3 = (num >> 8) & 0xFF
    o4 = num & 0xFF
    return f"{o1}.{o2}.{o3}.{o4}"


def _make_mask(prefix_len: int) -> int:
    """生成前缀对应的32位子网掩码"""
    if prefix_len == 0:
        return 0
    return ((1 << prefix_len) - 1) << (32 - prefix_len)


# ---------------- 任务函数实现 ----------------
def parse_cidr(cidr):
    """'163.152.6.0/24' -> (network as int, prefix length).

    Requirements: reject a prefix length outside 0-32, and reject an address
    whose host bits are set when they should not be (163.152.6.5/24 is a
    common way to write a host, but it is not a network).
    """
    ip_part, plen_str = cidr.split("/")
    plen = int(plen_str)
    # R1：前缀长度必须在0~32
    if plen < 0 or plen > 32:
        raise ValueError(f"Prefix length {plen} out of range (0-32)")

    ip_int = _ip_str_to_int(ip_part)
    mask = _make_mask(plen)
    net_int = ip_int & mask
    # R2：主机位必须全0；如果原IP和网络地址不一样，报错
    if ip_int != net_int:
        raise ValueError(f"{cidr} is not a valid network (host bits set)")
    return net_int, plen


def network_range(cidr):
    """'163.152.6.0/24' -> (first usable, last usable, broadcast) as strings.

    Careful at the edges. /31 and /32 do not have a usable host range in the
    ordinary sense - decide what you return and say so in observation.md.
    """
    net_int, plen = parse_cidr(cidr)
    mask = _make_mask(plen)
    wildcard = (~mask) & 0xFFFFFFFF
    broadcast_int = net_int | wildcard

    if plen == 32:
        # /32：单主机路由，唯一地址，无独立广播
        single = _int_to_ip_str(net_int)
        return (single, single, single)
    elif plen == 31:
        # RFC3021：点对点链路，两个地址都可用，不区分网络/广播
        a = _int_to_ip_str(net_int)
        b = _int_to_ip_str(net_int + 1)
        return (a, b, b)
    else:
        # 常规前缀 <=30：网络号+1为首个可用，广播-1为最后可用
        first = _int_to_ip_str(net_int + 1)
        last = _int_to_ip_str(broadcast_int - 1)
        bcast = _int_to_ip_str(broadcast_int)
        return (first, last, bcast)


class ForwardingTable:
    """Longest-prefix-match forwarding.

    add(cidr, next_hop)  ·  lookup(address) -> next_hop or None

    The default route 0.0.0.0/0 matches everything and is the shortest prefix,
    so it must lose to any other match. If two entries have the same prefix
    length, the table is malformed - say what you do.
    """
    def __init__(self):
        # 保存路由：列表，元素 (prefix_len, network_int, next_hop)
        self.routes = []

    def add(self, cidr, next_hop):
        net_int, plen = parse_cidr(cidr)
        # 策略：同前缀+同网络直接覆盖；如果【相同前缀长度、不同网络】则一起保留
        # 同前缀同网络：删除旧条目，添加新的下一跳
        self.routes = [r for r in self.routes if not (r[0]==plen and r[1]==net_int)]
        self.routes.append((plen, net_int, next_hop))

    def lookup(self, address):
        addr_int = _ip_str_to_int(address)
        best_plen = -1
        best_hop = None

        for plen, net, hop in self.routes:
            mask = _make_mask(plen)
            if (addr_int & mask) == net:
                # 匹配；更长前缀优先
                if plen > best_plen:
                    best_plen = plen
                    best_hop = hop
        return best_hop


# ------------------------------------------------------------------- harness
RANGE_CASES = [
    ("192.168.0.0/24",  "192.168.0.1",   "192.168.0.254",  "192.168.0.255"),
    ("10.0.0.0/8",      "10.0.0.1",      "10.255.255.254", "10.255.255.255"),
    ("172.16.32.0/20",  "172.16.32.1",   "172.16.47.254",  "172.16.47.255"),
    ("203.0.113.64/26", "203.0.113.65",  "203.0.113.126",  "203.0.113.127"),
]

TABLE = [
    ("0.0.0.0/0",       "default-gw"),
    ("10.0.0.0/8",      "campus"),
    ("10.20.0.0/16",    "eng-building"),
    ("10.20.30.0/24",   "lab-floor"),
    ("10.20.30.64/26",  "lab-rack-2"),
    ("192.168.1.0/24",  "home"),
]

LOOKUP_CASES = [
    ("10.20.30.70",   "lab-rack-2"),     # inside all four 10.x entries
    ("10.20.30.10",   "lab-floor"),
    ("10.20.99.1",    "eng-building"),
    ("10.99.0.1",     "campus"),
    ("8.8.8.8",       "default-gw"),
    ("192.168.1.77",  "home"),
]


def verify():
    fails = 0
    for cidr, first, last, bcast in RANGE_CASES:
        try:
            got = network_range(cidr)
        except NotImplementedError:
            print("  network_range is still a stub"); return 1
        except Exception as e:
            print(f"  FAIL  {cidr:<18} raised {e!r}"); fails += 1; continue
        ok = tuple(got) == (first, last, bcast)
        print(f"  {'ok  ' if ok else 'FAIL'}  {cidr:<18} {got}")
        fails += not ok

    t = ForwardingTable()
    try:
        for cidr, hop in TABLE:
            t.add(cidr, hop)
    except NotImplementedError:
        print("  ForwardingTable is still a stub"); return 1

    for addr, expect in LOOKUP_CASES:
        got = t.lookup(addr)
        ok = got == expect
        print(f"  {'ok  ' if ok else 'FAIL'}  {addr:<16} -> {got}  (want {expect})")
        fails += not ok

    print(f"\n  {len(RANGE_CASES) + len(LOOKUP_CASES) - fails}"
          f"/{len(RANGE_CASES) + len(LOOKUP_CASES)} ok")
    return 1 if fails else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--verify", action="store_true")
    a = p.parse_args()
    raise SystemExit(verify() if a.verify else p.print_help())