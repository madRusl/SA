def convert_ipv4(ip_addr):
    return tuple(int(n) for n in ip_addr.split('.'))


def check_ipv4_in(ip_addr):
    return convert_ipv4('172.22.213.0') < convert_ipv4(ip_addr) < convert_ipv4('172.22.215.255')
