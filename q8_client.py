from joao_ramos_constants import *
import socket

def UDP_client(message, timeout=1, max_attempts=10):
    print("_________________________________________")
    print("    EXECUTANDO CLIENTE UDP CONFIAVEL")
    attempts = 0
    success = False
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        
        while not success and attempts < max_attempts:
            attempts += 1
            print(f"[CLIENT] ({attempts}/{max_attempts}) Tentando enviar mensagem: '{message}'")
            s.sendto(message.encode(DEFAULT_DECODE_FORMAT), ADDR)
            
            try:
                data, server = s.recvfrom(DEFAULT_BUFFER_SIZE)
                print(f"[CLIENT] Confirmation recieved: {data.decode()}")
                success = True
            except socket.timeout:
                print(f"[CLIENT] [ERROR] Confirmation not recieved")

        if success:
            print("[CLIENT] Mensagem enviada com sucesso")     
        else:
            print("[CLIENT] Numero maximo de tentaivas exedidas")     
    finally:
        if socket:    
            print("[CLIENT] Fechando socket")
            s.close()
    return success

if __name__ == "__main__":
    UDP_client("Mensagem lorem ipsum")