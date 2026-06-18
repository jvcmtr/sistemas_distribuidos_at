import socket
from joao_ramos_constants import *
from q9_utils import *


def handle_http_request(conn, client):
    print("[SERVER] Recebendo nova requisição")
    request = conn.recv(DEFAULT_BUFFER_SIZE).decode(DEFAULT_DECODE_FORMAT)
    if not request: return
    
    details = get_http_details(request)
    print(f"[SERVER] Request details: { ''.join([f'\n\t{k} : {v}' for k, v in details.items()][:5]) }")
    
    lang = ACCEPTED_LANG[0]
    if details.get("Accept-Language"):
        for l in ACCEPTED_LANG[::-1]:
            if l in details.get("Accept-Language"): lang = l
    print(f"[SERVER] lang: {lang}")
    
    content, status = NOT_FOUND, 404
    if PATHS.get(details['path']):
        content, status = PATHS[details['path']][lang], 200 

    print(f"[SERVER] status: {status}")
    log(client, details['method'], details['path'], status)    

    conn.sendall(http_response(content, status))
    conn.close()


def main():
    print("_______________________________")
    print("    INICIANDO SERVIDOR HTTP ")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((IP, PORT))
        s.listen()
        print(f"- Servidor rodando em http://{IP}:{PORT}")

        while True:
            try:
                conn, client = s.accept()
                handle_http_request(conn, client)
            except KeyboardInterrupt:
                print("...Fechando conexões abertas ")
                if conn: conn.close()
                break
            except Exception as e:
                print(f"\t[ERRO] Uma falha ocorreu ao processar uma requisição:")
                print(f"{e}")
                if conn: conn.close()
    finally:
        print("...Fechando socket")
        if s: s.close()

if __name__ == "__main__":
    main()