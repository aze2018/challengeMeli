#La siguiente funcion es un poco fea, pero fue implementada ya que existen ocaciones
#que en sistemas operativos Linux, cuando se pide la IP nos devuelve 127.0.0.1. Y esto
#generaria un error al momento de persistir la informacion del agente.
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP