from scapy.all import sniff, TCP, Raw
from joao_ramos_constants import *


def sniff_package(packet):
    if not packet.haslayer(TCP): return
    if not packet[TCP].dport == PORT: return 
    if not packet.haslayer(Raw): return
    
    if len(packet[Raw].load) < SIZE_PREFIX_LEN:
        print("[SNIFFER] Payload não possui prefixo apropriado")
        return

    payload = packet[Raw].load
    size = -1
    try:
        size_raw = payload[:SIZE_PREFIX_LEN].decode(DEFAULT_DECODE_FORMAT)
        size = int(size_raw)
        if size == 0 : raise ValueError
    except:
        print(f"[SNIFFER] Prefixo do pacote não condizente com o protocolo: \t size={size_raw}")
    
    if size==-1: size=size_raw
    msg = payload[SIZE_PREFIX_LEN:]
    print(f"[SNIFFER] Mensagem capturada"+
        f"\n    - Prefixo : {size_raw}"+
        f"\n    - Mensagem: {msg}"+
        f"\n    - Tamanho esperado: {size}"+
        f"\n    - Tamanho real: {len(msg)}"+
        (f"\n    STATUS INCONSISTENTE" if len(msg) != size else "")
    )

if __name__ == "__main__":
    print("_____________________________________")
    print("    INICIALIZANDO SNIFFER")
    print(f"[SNIFFER] Monitorando porta {PORT}...")
    sniff(iface="lo", filter=f"tcp port {PORT}", prn=sniff_package, store=0)