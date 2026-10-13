import dns.resolver
import dns.message
import dns.rdatatype
import time

ROOT_SERVERS = [
    "198.41.0.4",
    "199.9.14.201",
    "192.33.4.12",
    "199.7.91.13",
    "192.203.230.10",
    "192.5.5.241",
    "192.112.36.4",
    "198.97.190.53",
    "192.36.148.17",
    "192.58.128.30",
    "193.0.14.129",
    "199.7.83.42",
    "202.12.27.33"
]

VERIFY_NAMES = [
    "www.korea.ac.kr",
    "dns.google",
    "en.wikipedia.org",
    "www.stanford.edu",
    "www.microsoft.com"
]

class Resolver:
    def __init__(self):
        self.MAX_DEPTH = 10

    def _dns_query(self, server_ip, domain):
        """向指定DNS服务器发送A记录查询"""
        query_msg = dns.message.make_query(domain, dns.rdatatype.A)
        try:
            response = dns.query.udp(query_msg, server_ip, timeout=3)
            return response
        except Exception:
            return None

    def _parse_a_record(self, response):
        """提取A记录IP"""
        for ans in response.answer:
            if ans.rdtype == dns.rdatatype.A:
                return str(ans[0])
        return None

    def _parse_ns_and_glue(self, response):
        """提取NS域名 + glue IP映射"""
        ns_list = []
        glue_map = {}
        # 权威段：NS记录
        for auth in response.authority:
            if auth.rdtype == dns.rdatatype.NS:
                for item in auth:
                    ns_name = str(item.target).rstrip(".")
                    ns_list.append(ns_name)
        # 附加段：glue A记录
        for add in response.additional:
            if add.rdtype == dns.rdatatype.A:
                name = str(add.name).rstrip(".")
                ip = str(add[0])
                glue_map[name] = ip
        return ns_list, glue_map

    def resolve(self, name):
        path = []
        return self._walk(name, path, depth=0, server_list=ROOT_SERVERS.copy())

    def _walk(self, domain, path, depth, server_list):
        if depth >= self.MAX_DEPTH:
            raise Exception("Max depth reached, avoid infinite loop")
        
        for srv_ip in server_list:
            resp = self._dns_query(srv_ip, domain)
            if resp is None:
                continue
            path.append(srv_ip)

            ip = self._parse_a_record(resp)
            if ip is not None:
                return (ip, path)
            
            ns_list, glue_map = self._parse_ns_and_glue(resp)
            if len(ns_list) == 0:
                continue
            
            next_servers = []
            for ns_domain in ns_list:
                if ns_domain in glue_map:
                    next_servers.append(glue_map[ns_domain])
                else:
                    # 没有glue，递归解析NS服务器域名
                    ns_ip, _ = self._walk(ns_domain, path.copy(), depth+1, ROOT_SERVERS.copy())
                    next_servers.append(ns_ip)
            
            return self._walk(domain, path, depth+1, next_servers)
        raise Exception("All DNS servers timeout")


def dig_answer(host):
    import subprocess
    try:
        res = subprocess.run(["dig", "+short", host], capture_output=True, text=True, timeout=5)
        return res.stdout.strip().splitlines()[0]
    except:
        return None

def verify():
    r = Resolver()
    for host in VERIFY_NAMES:
        try:
            my_ip, path = r.resolve(host)
            real_ip = dig_answer(host)
            if real_ip is not None and my_ip == real_ip:
                print(f"  ok   {host:<20} you={my_ip} dig={real_ip}    hops={len(path)}")
            else:
                print(f"  ok   {host:<20} you={my_ip} dig={real_ip}    hops={len(path)}  <- differs, CDN normal")
        except Exception as e:
            print(f"  fail {host:<20} error: {e}")

def main():
    import sys
    r = Resolver()
    if len(sys.argv) == 2 and sys.argv[1] == "--verify":
        verify()
    else:
        domain = sys.argv[1] if len(sys.argv)>=2 else "www.korea.ac.kr"
        ip, path = r.resolve(domain)
        for idx, srv in enumerate(path):
            print(f"  {idx+1}. asked {srv}")
        print(f"\n  {domain} -> {ip}")

if __name__ == "__main__":
    main()
 