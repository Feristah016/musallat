from flask import Flask, render_template, url_for, redirect, request
from threading import Thread
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import csv
import pandas as pd
from sklearn.svm import SVR
import datetime
import requests
import json
import plotly
import pandas_datareader as web
from pandas_datareader import data
import scipy as sp
from sympy import *
from scipy.integrate import quad
from scipy.integrate import cumulative_trapezoid

app = Flask('')

@app.route('/')
def home():
  print("home")
  return render_template("index2.html")

@app.route("/sjsj")
def sjsj():
  return render_template("sjsj.html")

@app.route("/test")
def test():
  return render_template("test.html")

@app.route("/test2")
def test2():
  return render_template("test2.html")

@app.route("/eth")
def abbas():
  

  url = "https://www.cryptodatadownload.com/cdd/Binance_ETHUSDT_d.csv"
  myfile = requests.get(url, verify = False)
  with open("testcsv.csv", "wb") as f:
      f.write(myfile.content)

  dates=[]
  prices=[]
  z = []

  dat = pd.read_csv("testcsv.csv", header=1)
  print(dat.head())
  print(dat["date"])
  print(dat)
  yeni=[]
  def numOfDays(date1, date2):
      return int((date2-date1).days)
  for i in dat["date"]:
      i = i.replace(" 00:00:00", "")
      i = i.split("-")
      tarih = datetime.date(int(i[0]), int(i[1]), int(i[2]))
      şuan = datetime.datetime.now().strftime("%Y-%m-%d")
      şuan = şuan.split("-")
      şuan = datetime.date(int(şuan[0]), int(şuan[1]), int(şuan[2]))


      if numOfDays(tarih, şuan) <= numOfDays(datetime.date(2021,1,1),şuan):
          yeni.append(numOfDays(tarih, şuan))
          print(tarih,"tarih")
          print(numOfDays(tarih, şuan), "numofdays")

  x = yeni[-1] + 1
  tahminx = x
  yeni.reverse()
  slicee=int(len(yeni))
  xx = yeni
  print(yeni, "yeni şeyleri")
  yeni = np.reshape(yeni,(-1,1))
  newprice=dat["open"][:slicee]
  print(dat["open"][:slicee], "open seyleri")

  print(newprice, "newprice")

  rbf1e3 = SVR(kernel="rbf", C=1e6, gamma=0.01)
  rbf1e4 = SVR(kernel="rbf", C=1e4, gamma=0.1)
  rbf1e5 = SVR(kernel="rbf", C=1e5, gamma=0.1)
  rbf1e4g = SVR(kernel="rbf", C=1e4, gamma=0.05)
  rbf1e5g = SVR(kernel="rbf", C=1e5, gamma=0.05)
  test = SVR(kernel="rbf", C=1e5, gamma=0.01)
  print(dat["open"])
  rbf1e3.fit( yeni, newprice)
  rbf1e4.fit( yeni, newprice)
  rbf1e5.fit( yeni, newprice)
  rbf1e4g.fit(yeni, newprice)
  rbf1e5g.fit(yeni, newprice)
  test.fit(   yeni, newprice)
  x = np.reshape(x, (1,1))

  uzunx = np.reshape(xx, (-1, 1))


  print(xx,"xx")
  print("\n",uzunx)


  print("1e6g0.01", rbf1e3.predict(x)[0])
  print("1e4", rbf1e4.predict(x)[0])
  print("1e5", rbf1e5.predict(x)[0])
  print("1e4g", rbf1e4g.predict(x)[0])
  print("1e5g", rbf1e5g.predict(x)[0])
  print("1e5g0.01", test.predict(x)[0])
  print("\n", (rbf1e3.predict(x)[0]+rbf1e5g.predict(x)[0]+rbf1e4.predict(x)[0])/3)
  print("\n", (test.predict(x)[0] + rbf1e4.predict(x)[0]) / 2)
  print("\n", (rbf1e3.predict(x)[0] + rbf1e5g.predict(x)[0] + rbf1e4.predict(x)[0]+rbf1e5.predict(x)[0]+rbf1e4g.predict(x)[0]+test.predict(x)[0])/6)
  print("asıl tahmin","\n", (rbf1e4.predict(x)[0]+rbf1e4g.predict(x)[0])/2)
  fig = px.line(dat, x=xx, y=[rbf1e3.predict(uzunx), rbf1e4.predict(uzunx), rbf1e5.predict(uzunx), rbf1e4g.predict(uzunx), rbf1e5g.predict(uzunx),  test.predict(uzunx)],
                labels=["e6g0.01", "e4", "e5", "e4g0.05", "e5g0.05", "1e5g0.01"])
  #px.line(dat, x=xx,y=["open", "close"]).show()
  #px.scatter_3d(dat, x=xx,y="open", z="close", color="open").show()
  fig2 = px.scatter(dat, x=xx, y=newprice)
  fig2.update_traces(marker=dict(size=6,
                                line=dict(width=2,
                                          color='DarkSlateGrey')),
                    selector=dict(mode='markers'))

  fig4 = px.scatter(x=[tahminx,tahminx,tahminx,tahminx,tahminx,tahminx], y=[rbf1e3.predict(x)[0],
                          rbf1e4.predict(x)[0],
                          rbf1e5.predict(x)[0],
                          rbf1e4g.predict(x)[0],
                          rbf1e5g.predict(x)[0],
                          test.predict(x)[0]], color=["e6g0.01", "e4", "e5", "e4g0.05", "e5g0.05", "1e5g0.01"])
  fig4.update_traces(marker=dict(size=10,
                                line=dict(width=1,
                                          )),
                    selector=dict(mode='markers'))


  fig3 = go.Figure(data=fig.data + fig2.data + fig4.data)
  graphJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
  header="ETH-USD"
  description = """
    abbas bilir.
    """
  #fig3.show()

  return render_template("abbas.html", graphJSON=graphJSON, header=header,description=description)

@app.route("/eth2")
def abbas2():
  url = "https://www.cryptodatadownload.com/cdd/Binance_ETHUSDT_d.csv"
  myfile = requests.get(url, verify = False)
  with open("testcsv.csv", "wb") as f:
      f.write(myfile.content)

  dates=[]
  prices=[]
  z = []

  dat = pd.read_csv("testcsv.csv", header=1)
  print(dat.head())
  print(dat["date"])
  print(dat)
  yeni=[]
  def numOfDays(date1, date2):
      return int((date2-date1).days)
  for i in dat["date"]:
      i = i.replace(" 00:00:00", "")
      i = i.split("-")
      tarih = datetime.date(int(i[0]), int(i[1]), int(i[2]))
      şuan = datetime.datetime.now().strftime("%Y-%m-%d")
      şuan = şuan.split("-")
      şuan = datetime.date(int(şuan[0]), int(şuan[1]), int(şuan[2]))


      if numOfDays(tarih, şuan) <= 30:
          yeni.append(numOfDays(tarih, şuan))
          print(tarih,"tarih")
          print(numOfDays(tarih, şuan), "numofdays")

  x = yeni[-1] + 1
  tahminx = x
  yeni.reverse()
  slicee=int(len(yeni))
  xx = yeni
  print(yeni, "yeni şeyleri")
  yeni = np.reshape(yeni,(-1,1))
  newprice=dat["open"][:slicee]
  print(dat["open"][:slicee], "open seyleri")

  print(newprice, "newprice")

  rbf1e3 = SVR(kernel="rbf", C=1e6, gamma=0.01)
  rbf1e4 = SVR(kernel="rbf", C=1e4, gamma=0.1)
  rbf1e5 = SVR(kernel="rbf", C=1e5, gamma=0.1)
  rbf1e4g = SVR(kernel="rbf", C=1e4, gamma=0.05)
  rbf1e5g = SVR(kernel="rbf", C=1e5, gamma=0.05)
  test = SVR(kernel="rbf", C=1e5, gamma=0.01)
  print(dat["open"])
  rbf1e3.fit( yeni, newprice)
  rbf1e4.fit( yeni, newprice)
  rbf1e5.fit( yeni, newprice)
  rbf1e4g.fit(yeni, newprice)
  rbf1e5g.fit(yeni, newprice)
  test.fit(   yeni, newprice)
  x = np.reshape(x, (1,1))

  uzunx = np.reshape(xx, (-1, 1))


  print(xx,"xx")
  print("\n",uzunx)


  print("1e6g0.01", rbf1e3.predict(x)[0])
  print("1e4", rbf1e4.predict(x)[0])
  print("1e5", rbf1e5.predict(x)[0])
  print("1e4g", rbf1e4g.predict(x)[0])
  print("1e5g", rbf1e5g.predict(x)[0])
  print("1e5g0.01", test.predict(x)[0])
  print("\n", (rbf1e3.predict(x)[0]+rbf1e5g.predict(x)[0]+rbf1e4.predict(x)[0])/3)
  print("\n", (test.predict(x)[0] + rbf1e4.predict(x)[0]) / 2)
  print("\n", (rbf1e3.predict(x)[0] + rbf1e5g.predict(x)[0] + rbf1e4.predict(x)[0]+rbf1e5.predict(x)[0]+rbf1e4g.predict(x)[0]+test.predict(x)[0])/6)
  print("asıl tahmin","\n", (rbf1e4.predict(x)[0]+rbf1e4g.predict(x)[0])/2)
  fig = px.line(dat, x=xx, y=[rbf1e3.predict(uzunx), rbf1e4.predict(uzunx), rbf1e5.predict(uzunx), rbf1e4g.predict(uzunx), rbf1e5g.predict(uzunx),  test.predict(uzunx)],
                labels=["e6g0.01", "e4", "e5", "e4g0.05", "e5g0.05", "1e5g0.01"])
  #px.line(dat, x=xx,y=["open", "close"]).show()
  #px.scatter_3d(dat, x=xx,y="open", z="close", color="open").show()
  fig2 = px.scatter(dat, x=xx, y=newprice)
  fig2.update_traces(marker=dict(size=6,
                                line=dict(width=2,
                                          color='DarkSlateGrey')),
                    selector=dict(mode='markers'))

  fig4 = px.scatter(x=[tahminx,tahminx,tahminx,tahminx,tahminx,tahminx], y=[rbf1e3.predict(x)[0],
                          rbf1e4.predict(x)[0],
                          rbf1e5.predict(x)[0],
                          rbf1e4g.predict(x)[0],
                          rbf1e5g.predict(x)[0],
                          test.predict(x)[0]], color=["e6g0.01", "e4", "e5", "e4g0.05", "e5g0.05", "1e5g0.01"])
  fig4.update_traces(marker=dict(size=10,
                                line=dict(width=1,
                                          )),
                    selector=dict(mode='markers'))


  fig3 = go.Figure(data=fig.data + fig2.data + fig4.data)
  graphJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
  header="ETH-USD"
  description = """
    abbas bilir.
    """
  #fig3.show()

  return render_template("abbas.html", graphJSON=graphJSON, header=header,description=description)


@app.route("/dolar")
def abbas3():
  crypto_currancy = "USD"
  against_currancy = "TRY"
  start = datetime.datetime(2021,10,15)
  end = datetime.datetime.now()
  #data = web.DataReader(f"{crypto_currancy}-{against_currancy}", "yahoo", start, end)
  #url = "https://query1.finance.yahoo.com/v7/finance/download/USDTRY=X?period1=1605770761&period2=1637306761&interval=1d&events=history&includeAdjustedClose=true"
  #myfile = requests.get(url, verify = False)
  
  dat = data.DataReader('USDTRY=X', 'yahoo', start, end)["Close"]
  print(dat)
  #dat.drop(dat.tail(1).index,inplace=True)
  print(dat)
  #with open("testcsv.csv", "w") as f:
  #  f.write(dat.content)
  dates=[]
  prices=[]
  z = []

  #dat = pd.read_csv("testcsv.csv", header=0)
  yeni= list(range(1, len(dat)+1))
  #def numOfDays(date1, date2):
  #    return int((date2-date1).days)
  #for i in dat:
  #    i = i.replace(" 00:00:00", "")
  #    i = i.split("-")
  #    tarih = datetime.date(int(i[0]), int(i[1]), int(i[2]))
  #    şuan = datetime.datetime.now().strftime("%Y-%m-%d")
  #    şuan = şuan.split("-")
  #    şuan = datetime.date(int(şuan[0]), int(şuan[1]), int(şuan[2]))


  #    if numOfDays(tarih, şuan) <= 30:
  #        yeni.append(numOfDays(tarih, şuan))
  #        print(tarih,"tarih")
  #        print(numOfDays(tarih, şuan), "numofdays")

  x = yeni[-1] + 1
  
  tahminx = x
  slicee=int(len(yeni))
  
  xx = yeni
  print(yeni, "yeni şeyleri")
  yeni = np.reshape(yeni,(-1,1))
  newprice=dat[:slicee]
  print(dat[:slicee], "Close seyleri")

  print(newprice, "newprice")

  rbf1e3 = SVR(kernel="rbf", C=1e6, gamma=0.01)
  rbf1e4 = SVR(kernel="rbf", C=1e4, gamma=0.1)
  rbf1e5 = SVR(kernel="rbf", C=1e5, gamma=0.1)
  rbf1e4g = SVR(kernel="rbf", C=1e4, gamma=0.05)
  rbf1e5g = SVR(kernel="rbf", C=1e5, gamma=0.05)
  test = SVR(kernel="rbf", C=1e5, gamma=0.01)
  print(dat)
  rbf1e3.fit( yeni, newprice)
  rbf1e4.fit( yeni, newprice)
  rbf1e5.fit( yeni, newprice)
  rbf1e4g.fit(yeni, newprice)
  rbf1e5g.fit(yeni, newprice)
  test.fit(   yeni, newprice)
  x = np.reshape(x, (1,1))

  uzunx = np.reshape(xx, (-1, 1))


  print(xx,"xx")
  print("\n",uzunx)


  print("1e6g0.01", rbf1e3.predict(x)[0])
  print("1e4", rbf1e4.predict(x)[0])
  print("1e5", rbf1e5.predict(x)[0])
  print("1e4g", rbf1e4g.predict(x)[0])
  print("1e5g", rbf1e5g.predict(x)[0])
  print("1e5g0.01", test.predict(x)[0])
  print("\n", (rbf1e3.predict(x)[0]+rbf1e5g.predict(x)[0]+rbf1e4.predict(x)[0])/3)
  print("\n", (test.predict(x)[0] + rbf1e4.predict(x)[0]) / 2)
  print("\n", (rbf1e3.predict(x)[0] + rbf1e5g.predict(x)[0] + rbf1e4.predict(x)[0]+rbf1e5.predict(x)[0]+rbf1e4g.predict(x)[0]+test.predict(x)[0])/6)
  print("asıl tahmin","\n", (rbf1e4.predict(x)[0]+rbf1e4g.predict(x)[0])/2)
  tahmin1 = (rbf1e4g.predict(x)[0]+rbf1e3.predict(x)[0]+test.predict(x)[0])/3
  tahmin2 = (test.predict(x)[0] + rbf1e4.predict(x)[0]) / 2
  tahmin3 = (rbf1e3.predict(x)[0] + rbf1e5g.predict(x)[0] + rbf1e4.predict(x)[0]+rbf1e5.predict(x)[0]+rbf1e4g.predict(x)[0]+test.predict(x)[0])/6
  sıltahmin = (rbf1e4.predict(x)[0]+rbf1e4g.predict(x)[0])/2



  fig = px.line(dat, x=xx, y=[rbf1e3.predict(uzunx), rbf1e4.predict(uzunx), rbf1e5.predict(uzunx), rbf1e4g.predict(uzunx), rbf1e5g.predict(uzunx),  test.predict(uzunx)],
                labels=["e6g0.01", "e4", "e5", "e4g0.05", "e5g0.05", "1e5g0.01"])
  #px.line(dat, x=xx,y=["open", "close"]).show()
  #px.scatter_3d(dat, x=xx,y="open", z="close", color="open").show()
  fig2 = px.scatter(dat, x=xx, y=newprice)
  fig2.update_traces(marker=dict(size=6,
                                line=dict(width=2,
                                          color='DarkSlateGrey')),
                    selector=dict(mode='markers'))

  fig4 = px.scatter(x=[tahminx,tahminx,tahminx,tahminx,tahminx,tahminx], y=[rbf1e3.predict(x)[0],
                          rbf1e4.predict(x)[0],
                          rbf1e5.predict(x)[0],
                          rbf1e4g.predict(x)[0],
                          rbf1e5g.predict(x)[0],
                          test.predict(x)[0]], color=["e6g0.01", "e4", "e5", "e4g0.05", "e5g0.05", "1e5g0.01"])
  fig4.update_traces(marker=dict(size=10,
                                line=dict(width=1,
                                          )),
                    selector=dict(mode='markers'))


  fig3 = go.Figure(data=fig.data + fig2.data + fig4.data)
  graphJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
  header="TRY-USD"
  description = """
    abbas bilir.
    """
  #fig3.show()

  return render_template("abbas.html", graphJSON=graphJSON, header=header,description=description, tahmin1=tahmin1, tahmin2=tahmin2, tahmin3=tahmin3, sıltahmin=sıltahmin)

@app.route("/ethbase", methods=['POST', 'GET'])
def ethbase():
  if request.method == 'POST':
    #version 1:
    #opt1 = request.form.to_dict()
    #for key in opt1:
    #    if key == "tarih":
    #        string = opt1[key]
    #print(string)
    #version 2:
    tarih = request.form["tarih"]
    krip = request.form["krip"]
    # if you need float : floatvar = float(float2)
    #print(float2)
    print(tarih)
    print(krip)

    return abbas4(tarih, krip)
  else:
    return render_template('eterbase.html')


@app.route("/plot", methods=['POST', 'GET'])
def plottest():
  if request.method == 'POST':
    #version 1:
    #opt1 = request.form.to_dict()
    #for key in opt1:
    #    if key == "tarih":
    #        string = opt1[key]
    #print(string)
    #version 2:
    xs = float(request.form["xs"])
    xe = float(request.form["xe"])
    ns = float(request.form["ns"])
    ne = float(request.form["ne"])
    samples = int(request.form["samples"])
    # if you need float : floatvar = float(float2)
    #print(float2)

    return plotlyy(xs,xe,ns,ne,samples)
    #return plotlyy(0, 10, 0, 3, 200)
  else:
    return render_template('plotwait.html')
def f(t, amplitude, frequency):
  return t**frequency*np.exp(-t*amplitude)
def integrall(t, amplitude, frequency):
  yyy = t**frequency*np.exp(-t*amplitude)
  return cumulative_trapezoid(yyy, t, initial=0)

@app.route("/plotdone")
def plotlyy(xs, xe, ns, ne, samples):

  x = np.linspace(xs, xe, samples)
  n = np.linspace(ns, ne, samples)
  X, N = np.meshgrid(x, n)

  sy = f(np.ravel(X), 1, np.ravel(N))
  y = sy.reshape(X.shape)

  syinteg = integrall(X, 1, N)
  yinteg = syinteg.reshape(X.shape)


  #fig = go.Figure(data=[go.Surface(x=xx,y=yx,z=zx)])
  fig = go.Figure(data=[go.Surface(x=X,y=N,z=y), go.Surface(x=X,y=N,  z=yinteg, opacity=0.1)])
  #fig = go.Figure(data=[go.Surface(z=z_data)])

  fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                    highlightcolor="limegreen",   project_z=False), contours_y=dict  (show=True, usecolormap=False,
                                    highlightcolor="black",   project_y=False))
  fig.update_layout(autosize=True,
                    width=1200, height=1000,
                    margin=dict(l=0, r=10, b=290, t=0))

  fig3 = go.Figure(data=fig.data)
  graphJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
  header="test"
  description = """
    a
    """
  #fig3.show()

  return render_template("plotdone.html", graphJSON=graphJSON, header=header,description=description)


@app.route("/eth3")
def abbas4(tarih, kripto):
  kripto = kripto.upper()
  print(kripto)
  crypto_currancy = kripto
  against_currancy = "USD"
  tarih = tarih.split(" ")
  for i in range(len(tarih)):
    tarih[i] = int(tarih[i])

  start = datetime.datetime(tarih[0],tarih[1],tarih[2])
  end = datetime.datetime.now()
  #data = web.DataReader(f"{crypto_currancy}-{against_currancy}", "yahoo", start, end)
  #url = "https://query1.finance.yahoo.com/v7/finance/download/USDTRY=X?period1=1605770761&period2=1637306761&interval=1d&events=history&includeAdjustedClose=true"
  #myfile = requests.get(url, verify = False)
  
  dat = web.DataReader(f"{crypto_currancy}-{against_currancy}", "yahoo", start, end)["Close"]
  #dat.drop(dat.tail(1).index,inplace=True)
  print(dat)
  #with open("testcsv.csv", "w") as f:
  #  f.write(dat.content)
  dates=[]
  prices=[]
  z = []

  #dat = pd.read_csv("testcsv.csv", header=0)
  yeni= list(range(1, len(dat)+1))
  #def numOfDays(date1, date2):
  #    return int((date2-date1).days)
  #for i in dat:
  #    i = i.replace(" 00:00:00", "")
  #    i = i.split("-")
  #    tarih = datetime.date(int(i[0]), int(i[1]), int(i[2]))
  #    şuan = datetime.datetime.now().strftime("%Y-%m-%d")
  #    şuan = şuan.split("-")
  #    şuan = datetime.date(int(şuan[0]), int(şuan[1]), int(şuan[2]))


  #    if numOfDays(tarih, şuan) <= 30:
  #        yeni.append(numOfDays(tarih, şuan))
  #        print(tarih,"tarih")
  #        print(numOfDays(tarih, şuan), "numofdays")

  x = yeni[-1] + 1
  tahminx = x
  slicee=int(len(yeni))
  xx = yeni
  print(yeni, "yeni şeyleri")
  yeni = np.reshape(yeni,(-1,1))
  newprice=dat[:slicee]
  print(dat[:slicee], "Close seyleri")

  print(newprice, "newprice")

  rbf1e3 = SVR(kernel="rbf", C=1e6, gamma=0.01)
  rbf1e4 = SVR(kernel="rbf", C=1e4, gamma=0.1)
  rbf1e5 = SVR(kernel="rbf", C=1e5, gamma=0.1)
  rbf1e4g = SVR(kernel="rbf", C=1e4, gamma=0.05)
  rbf1e5g = SVR(kernel="rbf", C=1e5, gamma=0.05)
  test = SVR(kernel="rbf", C=1e5, gamma=0.01)
  print(dat)
  rbf1e3.fit( yeni, newprice)
  rbf1e4.fit( yeni, newprice)
  rbf1e5.fit( yeni, newprice)
  rbf1e4g.fit(yeni, newprice)
  rbf1e5g.fit(yeni, newprice)
  test.fit(   yeni, newprice)
  x = np.reshape(x, (1,1))

  uzunx = np.reshape(xx, (-1, 1))


  print(xx,"xx")
  print("\n",uzunx)


  print("1e6g0.01", rbf1e3.predict(x)[0])
  print("1e4", rbf1e4.predict(x)[0])
  print("1e5", rbf1e5.predict(x)[0])
  print("1e4g", rbf1e4g.predict(x)[0])
  print("1e5g", rbf1e5g.predict(x)[0])
  print("1e5g0.01", test.predict(x)[0])
  print("\n", (rbf1e3.predict(x)[0]+rbf1e5g.predict(x)[0]+rbf1e4.predict(x)[0])/3)
  print("\n", (test.predict(x)[0] + rbf1e4.predict(x)[0]) / 2)
  print("\n", (rbf1e3.predict(x)[0] + rbf1e5g.predict(x)[0] + rbf1e4.predict(x)[0]+rbf1e5.predict(x)[0]+rbf1e4g.predict(x)[0]+test.predict(x)[0])/6)
  print("asıl tahmin","\n", (rbf1e4.predict(x)[0]+rbf1e4g.predict(x)[0])/2)
  tahmin1 = (rbf1e4g.predict(x)[0]+rbf1e3.predict(x)[0]+test.predict(x)[0])/3
  tahmin2 = (test.predict(x)[0] + rbf1e4.predict(x)[0]) / 2
  tahmin3 = (rbf1e3.predict(x)[0] + rbf1e5g.predict(x)[0] + rbf1e4.predict(x)[0]+rbf1e5.predict(x)[0]+rbf1e4g.predict(x)[0]+test.predict(x)[0])/6
  sıltahmin = (rbf1e4.predict(x)[0]+rbf1e4g.predict(x)[0])/2



  fig = px.line(dat, x=xx, y=[rbf1e3.predict(uzunx), rbf1e4.predict(uzunx), rbf1e5.predict(uzunx), rbf1e4g.predict(uzunx), rbf1e5g.predict(uzunx),  test.predict(uzunx)],
                labels=["e6g0.01", "e4", "e5", "e4g0.05", "e5g0.05", "1e5g0.01"])
  #px.line(dat, x=xx,y=["open", "close"]).show()
  #px.scatter_3d(dat, x=xx,y="open", z="close", color="open").show()
  fig2 = px.scatter(dat, x=xx, y=newprice)
  fig2.update_traces(marker=dict(size=6,
                                line=dict(width=2,
                                          color='DarkSlateGrey')),
                    selector=dict(mode='markers'))

  fig4 = px.scatter(x=[tahminx,tahminx,tahminx,tahminx,tahminx,tahminx], y=[rbf1e3.predict(x)[0],
                          rbf1e4.predict(x)[0],
                          rbf1e5.predict(x)[0],
                          rbf1e4g.predict(x)[0],
                          rbf1e5g.predict(x)[0],
                          test.predict(x)[0]], color=["e6g0.01", "e4", "e5", "e4g0.05", "e5g0.05", "1e5g0.01"])
  fig4.update_traces(marker=dict(size=10,
                                line=dict(width=1,
                                          )),
                    selector=dict(mode='markers'))


  fig3 = go.Figure(data=fig.data + fig2.data + fig4.data)
  graphJSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
  header=f"{crypto_currancy}-USD"
  description = """
    abbas bilir.
    """
  #fig3.show()

  return render_template("abbas.html", graphJSON=graphJSON, header=header,description=description, tahmin1=tahmin1, tahmin2=tahmin2, tahmin3=tahmin3, sıltahmin=sıltahmin)



def run():
  print("run")
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
  print("keep alive")
  t = Thread(target=run)
  t.start()

if __name__ == "__main__":
  print("if name")
  keep_alive()
