# pip install geoip2
#python .\getDomainFromIps.py
#
import geoip2.database
import re

db_path = 'GeoLite2-Country.mmdb'

reader = geoip2.database.Reader(db_path)

ip_file_path = 'ips.txt'
output_file_path = 'out.txt'


def is_valid_ip(ip):

    ipv4_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    if ipv4_pattern.match(ip):
        octets = ip.split('.')
        return all(0 <= int(octet) < 256 for octet in octets)
    return False

default_country = 'xxxxx'

with open(ip_file_path, 'r', encoding='utf-8') as file:
    ip_addresses = file.readlines()

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for ip in ip_addresses:
        ip = ip.strip()  
        if is_valid_ip(ip):
            try:
                response = reader.country(ip)
                country = response.country.name
                output_file.write(f"IP: {ip}, Country: {country}\n")
            except geoip2.errors.AddressNotFoundError:
                output_file.write(f"IP: {ip}, Country: {default_country}\n")
        else:
            output_file.write(f"IP: {ip}, Country: {default_country}\n")

reader.close()
