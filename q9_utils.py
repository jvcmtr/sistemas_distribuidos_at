from joao_ramos_constants import *
import datetime
import os

# --------- CONTROL CONSTANTS ----------------
LOG_FILE = "q9.log"
PORT = 8080 # Override do port declarado em joao_ramos_constants para o port http
STATUS = {
    200 : "OK",
    404 : "NOT FOUND"
}
ACCEPTED_LANG = ["pt", "en"]
NOT_FOUND = "<html><body><h1>404 Not Found</h1></body></html>"
PATHS = {
    "/home": {
        "pt":"<html><body><h1>PAGINA PRINCIPAL</h1></body></html>",
        "en":"<html><body><h1>HOME</h1></body></html>",
    },
    "/contato":{
        "pt":"<html><body><h1>CONTATO</h1></body></html>",
        "en":"<html><body><h1>CONTACT</h1></body></html>",
    }
}

# --------- UTILS ----------------
def http_response(content, status, encode=DEFAULT_DECODE_FORMAT):
    content_length = len(content.encode(encode))
    return (
        f"HTTP/1.1 {status} {STATUS[status]}\r\n"
        "Content-Type: text/html\r\n"
        f"Content-Length: {content_length}\r\n" 
        + "Connection: close\r\n"
        + "\r\n"
        +f"{content}").encode(encode)

def log_columns(prop=None):
    dt = {
        "timestamp":0,
        "status-code":1,
        "status":2,
        "client":3,
        "method":4,
        "path":5,
    }
    if prop==None: return dt
    else: return dt[prop]

def _filter_log(lines, column, match):
    return [x for x in lines if len(x)>0 and f"{match}" in x.split("\t")[log_columns(column)]]

def log(addr, method, path, status):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "timestamp":timestamp,
            "status-code":status,
            "status":STATUS[status],
            "client":addr,
            "method":method,
            "path":path,
        }

        ordered_keys = sorted( log_columns().keys(), key=lambda k: log_columns(k)) 
        ln = "\t".join( f"{data[k]}" for k in ordered_keys ) + "\n"
        with open(LOG_FILE, "a") as f:
            f.write(ln)
    except Exception as e:
        print(f"[ERRO] Um erro ocorreu ao salvar em {LOG_FILE}")
        raise e

def read_log(filters=[]):
    lines = ""
    try:
        with open(LOG_FILE, "r") as f:
            lines= f.read().split("\n")
    except:
        return []
    for col, match in filters:
        lines = _filter_log(lines, col, match)
    return lines


def get_http_details(data):
    lines = data.split('\r\n')
    method, path, version = lines.pop(0).split(" ")
    headers = { l.split(": ")[0] : l.split(": ")[1] for l in lines if l }
    
    return {
        "method":method,
        "path":path,
        "version":version,
        **headers
    }