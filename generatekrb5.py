def generate_krb5_conf(fqdn: str) -> str:
    parts = fqdn.strip().split(".")
    if len(parts) < 2:
        return "❌ Invalid FQDN format. Example: dc01.fluffy.htb"

    domain = ".".join(parts[1:])
    realm = domain.upper()

    return f"""[libdefaults]
    default_realm = {realm}
    dns_lookup_realm = false
    dns_lookup_kdc = false

[realms]
    {realm} = {{
        kdc = {fqdn}
        admin_server = {fqdn}
    }}

[domain_realm]
    .{domain} = {realm}
    {domain} = {realm}
    {fqdn} = {realm}
"""

if __name__ == "__main__":
    fqdn = input("Enter FQDN (e.g., dc01.fluffy.htb): ")
    print("\nGenerated krb5.conf:\n")
    print(generate_krb5_conf(fqdn))
