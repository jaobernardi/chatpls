from structures import Server, Config
import servers
import events

events.call_event("startup")
config = Config()
server = Server(config.host, config.port, config.certificate, config.private_key)
server.http_start()
def shutdown(*args, **kwargs):
    server.stop()
    exit()


signal.signal(signal.SIGINT, shutdown)