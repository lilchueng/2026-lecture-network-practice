import json
import dns.resolver
import dns.exception

def trace_cname_chain(domain: str, resolver_ip: str):
    """追踪CNAME完整解析链，返回整条解析记录"""
    resolver = dns.resolver.Resolver()
    resolver.nameservers = [resolver_ip]
    chain = []
    current_name = domain
    max_depth = 10  # 防止无限循环

    while max_depth > 0:
        try:
            ans = resolver.resolve(current_name, 'A')
            # 获取A记录IP
            ip_list = [r.address for r in ans.rrset]
            chain.append({
                "domain": current_name,
                "type": "A",
                "value": ip_list
            })
            break
        except dns.resolver.CNAMEChain:
            pass
        except dns.exception.DNSException as e:
            try:
                cname_ans = resolver.resolve(current_name, 'CNAME')
                cname_target = str(cname_ans[0].target).rstrip('.')
                chain.append({
                    "domain": current_name,
                    "type": "CNAME",
                    "value": cname_target
                })
                current_name = cname_target
                max_depth -= 1
            except Exception as err:
                chain.append({"error": str(err)})
                break
    return chain

if __name__ == "__main__":
    target_domain = "www.korea.ac.kr"
  
    resolvers = {
        "KR_ISP": "168.126.63.1",
        "US_GOOGLE": "8.8.8.8"
    }
    result = {}
    for name, dns_ip in resolvers.items():
        print(f"正在使用 {name}({dns_ip}) 解析 {target_domain}")
        result[name] = trace_cname_chain(target_domain, dns_ip)

    # 输出chains.json
    with open("chains.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print("完成！结果已经保存到 chains.json")