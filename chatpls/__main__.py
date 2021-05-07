from structures import Server
import servers


server = Server('0.0.0.0', 80, '', '')
server.http_start()
def shutdown(*args, **kwargs):
    server.stop()
    exit()


signal.signal(signal.SIGINT, shutdown)