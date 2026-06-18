import nmap
from joao_ramos_constants import *

def main():
    print("_______________________________")
    print("    INICIANDO VARREDURA DE PORTS")

    nm = nmap.PortScanner()
    print(f"Iniciando scan em: {IP}")

    nm.scan(hosts=IP)

    print(f" | HOST \t| PORT \t| STATE\t| PROTOCOL \t| SERVICE")
    for h in nm.all_hosts():
        for p in nm[h].all_protocols():
            ports = nm[h][p].keys()
            for port in sorted(ports):
                state = nm[h][p][port]['state']
                program = nm[h][p][port]['name']
                print(f" | {h} \t| {port} \t| {state} \t| {p}   \t| {program}")

if __name__ == "__main__":
    main()