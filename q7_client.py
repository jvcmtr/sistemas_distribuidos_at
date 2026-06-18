

from joao_ramos_constants import *
import socket
import threading

def with_prefixed_bytes(msg, prefix_size):
    s = msg.encode()
    size = f"{len(msg)}"
    padding = prefix_size - len(size)
    prefix = f"{'0'*padding}{size}".encode() 
    return prefix + s

def TCP_client(name, messagem, prefix_size=SIZE_PREFIX_LEN):   
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(ADDR)
        
        print(f"  [CLIENT {name}] Mensagem a ser enviada: '{messagem}'")
        encoded_msg = with_prefixed_bytes(messagem, prefix_size)
        print(f"  [CLIENT {name}] Enviando mensagem ao servidor: '{encoded_msg}'")
        s.sendall(encoded_msg)
        
        response = s.recv(DEFAULT_BUFFER_SIZE)
        if response:
            print(f"  [CLIENT {name}] Resposta do Servidor: {response.decode(DEFAULT_DECODE_FORMAT)}")
         
    finally:
        if s:    
            print(f"  [CLIENT {name}] Fechando socket...")
            s.close()

if __name__ == "__main__":
    print("_____________________________________")
    print("    INICIALIZANDO CLIENTES TCP")

    dt = [
        ("1", "Lorem ipsum", SIZE_PREFIX_LEN),
        ("2", "Ola mundo", SIZE_PREFIX_LEN),
        ("3", "TAMANHO ERRADO", 2),
        ("4", "Ola professor", SIZE_PREFIX_LEN),
    ]

    for i in range(len(dt)) :
        try:
            name, msg, prefix_len = dt[i]
            t = threading.Thread(target=TCP_client, args=(name, msg, prefix_len))
            print(f"[MAIN] Thread para o cliente {name} criada. ({i+1}/{len(dt)})")
            t.start()
        except Exception as e:
            print(f"[MAIN] Um erro ocorreu ao iniciar a tread para o cliente: {e}")
