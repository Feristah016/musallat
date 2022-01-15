import requests as req

data = {"nm":"asdasd"}
r = req.get("https://musallat.zgretin.repl.co/gidecekbilgi")

print(r.text)