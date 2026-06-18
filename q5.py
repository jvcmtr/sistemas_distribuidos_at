import dns.resolver

def _group_trace_messages(trace):
    lines = trace.split("\n")

    dt = {"info":[], "send":[], "recieved":[], "send_data":[], "recieved_data":[]}
    key = "info"
    for l in lines:
        if "== Info:" in l:
            key = "info"
        elif "=> Send header, " in l:
            key = "send"
            continue # Para não incluir a propria linha
        elif "=> Send data, " in l:
            key = "send_data"
            continue # Para não incluir a propria linha
        elif "<= Recv header, " in l:
            key = "recieved"
            continue # Para não incluir a propria linha
        elif "<= Recv data, " in l:
            key = "recieved_data"
            continue # Para não incluir a propria linha
        dt[key].append(l)
    return dt

def _get_between(lines, prefix, sufix=None, offset=0):
    """
    Recebe um conjunto de linhas, seleciona a primeira que possui head e 
    Retorna a substring entre prefix e sufix.
    """
    s = [l for l in lines if prefix in l ]
    if not s:
        return None
    if sufix:
        return s[0][len(prefix)+offset: s[0].index(sufix)]
    else:
        return s[0][len(prefix)+offset:]

def get_trace_data(file_path):

    with open(file_path, 'r') as f:
        content = f.read()
        dt = _group_trace_messages(content)
    
    if not dt: return

    offset = len("0000: ")
    print(f"método HTTP: { _get_between(dt['send'], "0000: ", "HTTP")}")
    print(f"host: { _get_between(dt['send'], "Host: ", None, offset)}")
    print(f"status Code: {_get_between(dt['recieved'], "HTTP/1.1 ", None, offset)}")
    print(f"headers recebidos:")

    for h in dt["recieved"]:
        s = _get_between([h], "0000: ")
        if s:
            print(f"\t - {s}")

    print(f"IP remoto utilizado na conexão: {_get_between(dt['info'], "== Info: IPv4: ", ", ")}")


def get_dns_records(dominio):
    types = ["A", "AAAA"]
    print(f"Verificando registros { ', '.join(types)} para o dominio {dominio}")

    for t in types:
        results = dns.resolver.resolve(dominio, t)
        for r in results:
            print(f"\t- [{t}] {r.address}")


if __name__ == "__main__":

    print("_________________________")
    print("Questão 5.2 - Informações do trace")
    get_trace_data('q5.1.txt')

    print("_________________________")
    print("Questão 5.3 - registros do dominio")
    get_dns_records("example.com")
