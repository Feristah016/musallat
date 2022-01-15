import requests as req
import threading
from time import sleep

kesendata = {"nm":"nul"}
def gelenebak():

    while True:
        gelen = req.get("https://musallat.zgretin.repl.co/gelenbilgi")


        if gelen.text != "nul":
            print(f"---{gelen.text}")

            # işlemler

            req.post("https://musallat.zgretin.repl.co/gelenbilgi", data=kesendata)
        else:
            sleep(0.5)

a_thread = threading.Thread(target = gelenebak)
a_thread.start()

while True:
    i = input("gidecekbilgi: ")
    data = {"nm":i}
    r = req.post("https://musallat.zgretin.repl.co/gidecekbilgi", data=data)
