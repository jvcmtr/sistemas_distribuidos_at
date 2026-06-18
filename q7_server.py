from joao_ramos_constants import *
import socket
import threading

def handle_client(conn, addr, idx, decode_format=DEFAULT_DECODE_FORMAT):
    ip, porta = addr

    try:
        msg = conn.recv(SIZE_PREFIX_LEN)
        if not msg: 
            print(f"  [THREAD {idx}] Não há mais bytes do cliente {addr}. Encerrando processamento")
        
        size = int(msg.decode(decode_format))
        data = conn.recv(size)

        print(f"  [THREAD {idx}] Nova mensagem recebida:"+
        f"\n    - Tamanho esperado: {size}"+
        f"\n    - Tamanho real: {len(data)}"+
        f"\n    - Mensagem: '{data.decode(decode_format)}'"
        )
        # conn.sendall(data)

    except Exception as e:
            print(f"  [THREAD {idx}] MENSAGEM NÃO CONDIZ COM O TAMANHO INDICADO\t [ERRO]")
            response = f"Prefixo da mensagem formatado incorretamente. recebido:{msg.decode(decode_format)}"
            conn.sendall(response.encode())
    finally:
        conn.close()
        print(f"  [THREAD {idx}] Conexão encerrada com o cliente: {ip}:{porta}")
    pass



def TCP_server():
    print("_______________________________")
    print("    INICIANDO SERVIDOR TCP ")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen()
    print(f"[SERVER] Socket ativo em: {ADDR[0]}:{ADDR[1]}")
    
    i = 0
    try:
        while True:
            try:
                client = s.accept()
                i += 1
                t = threading.Thread(target=handle_client, args=(*client, i))
                t.start()
                print(f"[SERVER] Nova conexão estabelecida: ID:{i} {client[1][0]}:{client[1][1]}\t [{threading.active_count()-1} conexões ativas]")
            except KeyboardInterrupt:
                 break
            except Exception as e:
                if client:
                    print(f"[SERVER] [ERRO] Um erro ocorreu ao receber a mensagem do cliente {client}.\n ERRO:{e}")
                else:
                    print(f"[SERVER] [ERRO] Não foi possivel estabelecer conexão com o cliente.\n ERRO:{e}")
    finally:
        print("[SERVER] Fechando socket...")
        s.close()
        print("[SERVER] socket fechado")


if __name__ == "__main__":
    TCP_server()