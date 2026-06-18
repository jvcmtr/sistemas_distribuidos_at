import random
import socket
from joao_ramos_constants import *

def UDP_server(success_rate=0.5):
    print("_______________________________")
    print(f"    INICIANDO SOCKET UDP COM {success_rate*100}% FALHAS")

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(ADDR)
        print(f"[SERVER] Socket ativo em: {ADDR}")

        while True:
            try:
                data, client = s.recvfrom(DEFAULT_BUFFER_SIZE)
                print("_______________________________")
                print(f"[SERVER] Conexão estabelecida: {client}")
                print(f"[SERVER] Mensagem recebida: {data.decode(DEFAULT_DECODE_FORMAT)}")

                if random.random() > 0.5:
                    s.sendto(data, client)
                    print(f"[SERVER] [ACK_ENVIADO] Enviando resposta para {client}")
                else:
                    print(f"[SERVER] [ACK_DESCARTADO] Descartando mensagem de {client}")

            except Exception as e:
                print(f"\t[SERVER] [ERROR] Uma falha ocorreu ao processar uma mensagem: {e}")
    finally:
        if s:    
            print("[SERVER] Fechando socket")
            s.close()
    return success


if __name__ == "__main__":
    UDP_server()