import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

DISPLAY_MODE_MAP = {'IP':0, 'TARGET':1, 'TEMP':2}

def get_display_mode(display_mode_file):
    file = open(display_mode_file,'r')

    display_mode_str = file.read().strip()

    return DISPLAY_MODE_MAP.get(display_mode_str,-1)

