from joao_ramos_constants import *
from q9_utils import *
from scapy.all import sniff, TCP, IP, Raw

def get_client_404_count(client):
    return len(read_log(filters=[
        ("client", client),
        ("status-code", 404)
    ]))


def sniff_package(packet):
    try:
        if not packet.haslayer(TCP): return
        if not packet.haslayer(Raw): return
        
        payload = packet[Raw].load.decode(DEFAULT_DECODE_FORMAT)
        if STATUS[404] in payload:
            client = packet[IP].dst
            print(f"[SNIFFER] Acesso a pagina inexistente por parte do cliente: {client}")
            count = get_client_404_count(client) 
            if count >= 3:
                print(f"[SNIFFER] PADRÃO ANOMALO: cliente {client} tentou acessar paginas inexistentes {count} vezes.")
    
    except Exception as e:
        print("[ERRO]")
        raise e


if __name__ == "__main__":
    print("_____________________________________")
    print("    INICIALIZANDO SNIFFER")
    print(f"[SNIFFER] Monitorando porta {PORT}...")
    sniff(iface="lo", filter=f"tcp port {PORT}", prn=sniff_package, store=0)