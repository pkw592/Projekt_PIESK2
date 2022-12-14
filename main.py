from scapy.all import *
from scapy.layers.inet import IP, Ether, UDP, TCP
from scapy.all import rdpcap
import string
import random


def generate_mac():
    return f'{get_two_random()}:{get_two_random()}:{get_two_random()}:{get_two_random()}:{get_two_random()}:{get_two_random()}'

def generate_mac_list(length):
    mac_list = []
    for _ in range(length):
        mac_list.append(generate_mac())
    
    return mac_list

def get_two_random():
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', 
            '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    
    return f'{random.choice(numbers)}{random.choice(numbers)}'

def generate_ip_list(length):
    ip_list = []
    for _ in range(length):
        ip_list.append(socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff))))

    return ip_list

def get_random_string():
    random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k = random.randint(5,15)))
    return random_string

def sender(source, destination, mac):
    num = random.randint(1,3)
    if num == 3:
        pkt = Ether(src=mac)/IP(len=random.randint(1,50), src=source, dst=destination, id=random.randint(1,9))/TCP()/Raw(get_random_string())
    else:
        pkt = Ether(src=mac)/IP(len=random.randint(1,20), src=source, dst=destination, id=random.randint(1,9))/UDP()/Raw(get_random_string())
        print(pkt.show())
    
    sendp(pkt, iface=conf.iface)

def genetrate_traffic():
    destination_ip = input("Podaj IP docelowe: ")
    mac_number = int(input("Podaj ilość adresów MAC źródła: "))
    ip_number = int(input("Podaj ilość adresów IP źródła: "))
    mac_list = generate_mac_list(mac_number)
    ip_list = generate_ip_list(ip_number)
    while True:
        sender(source=random.choice(ip_list), destination=destination_ip, mac=random.choice(mac_list))

def generate_mac_flood():
    destination_ip = input("Podaj IP docelowe: ")
    ip_number = int(input("Podaj ilość adresów IP źródła: "))
    ip_list = generate_ip_list(ip_number)
    while True:
        pkt = Ether(src=generate_mac())/IP(len=random.randint(1,10), src=random.choice(ip_list), dst=destination_ip, id=random.randint(1,9))/UDP()
        sendp(pkt, iface=conf.iface)

def recreate_traffic():
    pcap_path = input('Podaj ścieżkę do pliku .pcap: ')
    packets = rdpcap(pcap_path)

    print(f"Number of packets: {len(packets)}")

    for packet in packets:
        sendp(packet, iface=conf.iface)

if __name__ == "__main__":
    print('Narzędzie do generowania ruchu stworzone na projekt z Projektowania systemów i sieci komputerowych')
    print('Aby wybrać akcję wpisz odpowiednią liczbę')
    print('1) Generowanie ruchu TCP/UDP')
    print('2) MAC flood')
    print('3) Odtwarzanie ruchu na podstawie pliku pcap')
    selected = int(input('Wybierz opcję: '))
    
    print('Naciśnij CTRL + C aby zatrzymać')
    if selected == 1:
        genetrate_traffic()
    
    if selected == 2:
        generate_mac_flood()

    if selected == 3:
        recreate_traffic()

    