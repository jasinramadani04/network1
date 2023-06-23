import socket
import requests
import json
from termcolor import colored

def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(response.text)
    return ip_data['ip']

def get_location_info():
    ip = get_public_ip()
    response = requests.get(f'http://ip-api.com/json/{ip}')
    location_data = json.loads(response.text)
    return location_data

def get_internet_service_provider():
    location_data = get_location_info()
    return location_data['isp']

def print_stylish(text):
    print(colored(text, 'cyan', attrs=['bold', 'underline']))

def scan_ports(ip, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def get_connected_users(ip, ports):
    users = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            sock.connect((ip, port))
            sock.sendall(b'WHO')
            response = sock.recv(1024)
            users.extend(response.decode().split(','))
            sock.close()
        except:
            pass
    return list(set(users))

def main():
    isp = get_internet_service_provider()
    ip = get_public_ip()
    location_data = get_location_info()
    latitude = location_data['lat']
    longitude = location_data['lon']
    open_ports = scan_ports(ip, [80, 443, 8080])  # Modify the list of ports to scan as per your requirements

    print_stylish('Internet Service Provider:')
    print(isp)
    print_stylish('Public IP Address:')
    print(ip)
    print_stylish('Geographic Location:')
    print(f'Latitude: {latitude}, Longitude: {longitude}')

    if len(open_ports) > 0:
        print_stylish('Connected Users:')
        users = get_connected_users(ip, open_ports)
        if len(users) > 0:
            for user in users:
                print(user)
        else:
            print('No users connected to the server.')
    else:
        print('No open ports found.')

if __name__ == '__main__':
    main()
