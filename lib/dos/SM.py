from lib.dos import _dos
Dos = _dos.Dos
class Run(Dos):
    def __init__(self, source: tuple, victim: tuple, count: int, message: str):
        self.source_ip, self.source_port = source[0], source[1]
        self.victim_ip, self.victim_ports = victim[0], victim[1]
        self.count, self.message = count, message
        self.dos(False, False, count)
