import threading
import connection
import outputparsing

out = {}

def gethostname(host,port,username,password):
    data = connection._getsshdata5(host, port, username, password, "show version\n")
    return outputparsing._parse_hostname(data)


def daemon(host, port, username, password, msisdn):
    #print "start 1"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    #print data
    ppp = outputparsing._getsubscribermsisdn(str(data))
    #print str(hoho) + " "+ str(ppp)
    if ppp.__len__()>1:
        hoho = gethostname(host, port, username, password)
        out.update({hoho : ppp})

    #print "stop 1"


def daemon1imsi(host, port, username, password, imsi):
    #print "start 1"
    data = connection._getsshdata3(host, port, username, password, "show subscribers imsi " + imsi + "\n")
    #print data
    ppp = outputparsing._getsubscribermsisdn(str(data))
    #print str(hoho) + " "+ str(ppp)
    if ppp.__len__()>1:
        hoho = gethostname(host, port, username, password)
        out.update({hoho : ppp})

    #print "stop 1"

def daemon1(host,port,username,password,msisdn):
    #print "start 2"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    ppp1 = outputparsing._getsubscribermsisdn(str(data))
    hoho1 = gethostname(host,port,username,password)
    if ppp1['sessnum']!=0:
        out.update({hoho1: ppp1})
    #print "stop 2"


def daemon2(host,port,username,password,msisdn):
    #print "start 3"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    ppp2 = outputparsing._getsubscribermsisdn(str(data))
    hoho2 = gethostname(host,port,username,password)
    if ppp2['sessnum']!=0:
        out.update({hoho2: ppp2})
    #print "stop 3"

def daemon3(host,port,username,password,msisdn):
    #print "start 4"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    ppp3 = outputparsing._getsubscribermsisdn(str(data))
    hoho3 = gethostname(host,port,username,password)
    if ppp3['sessnum']!=0:
        out.update({hoho3: ppp3})
    #print "stop 4"


def daemon4(host,port,username,password,msisdn):
    #print "start 5"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    ppp4 = outputparsing._getsubscribermsisdn(str(data))
    hoho4 = gethostname(host,port,username,password)
    if ppp4['sessnum']!=0:
        out.update({hoho4: ppp4})
    #print "stop 5"

def daemon5(host,port,username,password,msisdn):
    #print "start 6"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    ppp5 = outputparsing._getsubscribermsisdn(str(data))
    hoho5 = gethostname(host,port,username,password)
    if ppp5['sessnum']!=0:
        out.update({hoho5: ppp5})
    #print "stop 6"

def daemon6(host,port,username,password,msisdn):
    #print "start 7"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    ppp6 = outputparsing._getsubscribermsisdn(str(data))
    hoho6 = gethostname(host,port,username,password)
    if ppp6['sessnum']!=0:
        out.update({hoho6: ppp6})
    #print "stop 7"

def daemon7(host,port,username,password,msisdn):
    #print "start 8"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    ppp7 = outputparsing._getsubscribermsisdn(str(data))
    hoho7 = gethostname(host,port,username,password)
    if ppp7['sessnum']!=0:
        out.update({hoho7: ppp7})
    #print "stop 8"


def daemon8(host,port,username,password,msisdn):
    #print "start 9"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    ppp8 = outputparsing._getsubscribermsisdn(str(data))
    hoho8 = gethostname(host,port,username,password)
    if ppp8['sessnum']!=0:
        out.update({hoho8: ppp8})
    #print "stop 9"


def daemon9(host,port,username,password,msisdn):
    #print "start 10"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    ppp9 = outputparsing._getsubscribermsisdn(str(data))
    hoho9 = gethostname(host,port,username,password)
    if ppp9['sessnum']!=0:
        out.update({hoho9: ppp9})
    #print "stop 10"

def daemon10(host,port,username,password,msisdn):
    #print "start 11"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    ppp10 = outputparsing._getsubscribermsisdn(str(data))
    hoho10 = gethostname(host,port,username,password)
    if ppp10['sessnum']!=0:
        out.update({hoho10: ppp10})
    #print "stop 11"


def daemon11(host,port,username,password,msisdn):
    #print "start 12"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    ppp11 = outputparsing._getsubscribermsisdn(str(data))
    hoho11 = gethostname(host,port,username,password)
    if ppp11['sessnum']!=0:
        out.update({hoho11: ppp11})
    #print "stop 12"


def daemon12(host,port,username,password,msisdn):
    #print "start 13"
    data = connection._getsshdata3(host, port, username, password, "show subscribers msisdn " + msisdn + "\n")
    ppp12 = outputparsing._getsubscribermsisdn(str(data))
    hoho12 = gethostname(host,port,username,password)
    if ppp12['sessnum']!=0:
        out.update({hoho12: ppp12})
    #print "stop 13"


def find(port,username,password,msisdn,ggsnlist):
    num = len(ggsnlist)

    if num == 1:
        a = threading.Thread(name='daemon', target=daemon(ggsnlist[0],port,username,password,msisdn))
        a.setDaemon(True)
        a.start()
        a.join()
    elif num == 2:
        a = threading.Thread(name='daemon', target=daemon, args=(ggsnlist[0],port,username,password,msisdn))
        b = threading.Thread(name='daemon1', target=daemon1, args=(ggsnlist[1],port,username,password,msisdn))
        a.setDaemon(True)
        b.setDaemon(True)
        a.start(),b.start()
        a.join(),b.join()
    elif num ==3:
        a = threading.Thread(name='daemon', target=daemon, args=(ggsnlist[0],port,username,password,msisdn))
        b = threading.Thread(name='daemon1', target=daemon1, args=(ggsnlist[1],port,username,password,msisdn))
        c = threading.Thread(name='daemon2', target=daemon2, args=(ggsnlist[2],port,username,password,msisdn))
        a.setDaemon(True),b.setDaemon(True),c.setDaemon(True)
        a.start(),b.start(),c.start()
        a.join(),b.join(),c.join()
    elif num ==4:
        a = threading.Thread(name='daemon', target=daemon, args=(ggsnlist[0],port,username,password,msisdn))
        b = threading.Thread(name='daemon1', target=daemon1, args=(ggsnlist[1],port,username,password,msisdn))
        c = threading.Thread(name='daemon2', target=daemon2, args=(ggsnlist[2],port,username,password,msisdn))
        d = threading.Thread(name='daemon3', target=daemon3, args=(ggsnlist[3],port,username,password,msisdn))
        a.setDaemon(True),b.setDaemon(True),c.setDaemon(True),d.setDaemon(True)
        a.start(),b.start(),c.start(),d.start()
        a.join(),b.join(),c.join(),d.join()
    elif num ==5:
        a = threading.Thread(name='daemon', target=daemon, args=(ggsnlist[0],port,username,password,msisdn))
        b = threading.Thread(name='daemon1', target=daemon1, args=(ggsnlist[1],port,username,password,msisdn))
        c = threading.Thread(name='daemon2', target=daemon2, args=(ggsnlist[2],port,username,password,msisdn))
        d = threading.Thread(name='daemon3', target=daemon3, args=(ggsnlist[3],port,username,password,msisdn))
        e = threading.Thread(name='daemon4', target=daemon4, args=(ggsnlist[4],port,username,password,msisdn))
        a.setDaemon(True),b.setDaemon(True),c.setDaemon(True),d.setDaemon(True),e.setDaemon(True)
        a.start(),b.start(),c.start(),d.start(),e.start()
        a.join(),b.join(),c.join(),d.join(),e.join()
    elif num ==6:
        a = threading.Thread(name='daemon', target=daemon, args=(ggsnlist[0],port,username,password,msisdn))
        b = threading.Thread(name='daemon1', target=daemon1, args=(ggsnlist[1],port,username,password,msisdn))
        c = threading.Thread(name='daemon2', target=daemon2, args=(ggsnlist[2],port,username,password,msisdn))
        d = threading.Thread(name='daemon3', target=daemon3, args=(ggsnlist[3],port,username,password,msisdn))
        e = threading.Thread(name='daemon4', target=daemon4, args=(ggsnlist[4],port,username,password,msisdn))
        f = threading.Thread(name='daemon5', target=daemon5, args=(ggsnlist[5],port,username,password,msisdn))
        a.setDaemon(True),b.setDaemon(True),c.setDaemon(True),d.setDaemon(True),e.setDaemon(True),f.setDaemon(True)
        a.start(),b.start(),c.start(),d.start(),e.start(),f.start()
        a.join(),b.join(),c.join(),d.join(),e.join(),f.join()
    elif num ==7:
        a = threading.Thread(name='daemon', target=daemon, args=(ggsnlist[0],port,username,password,msisdn))
        b = threading.Thread(name='daemon1', target=daemon1, args=(ggsnlist[1],port,username,password,msisdn))
        c = threading.Thread(name='daemon2', target=daemon2, args=(ggsnlist[2],port,username,password,msisdn))
        d = threading.Thread(name='daemon3', target=daemon3, args=(ggsnlist[3],port,username,password,msisdn))
        e = threading.Thread(name='daemon4', target=daemon4, args=(ggsnlist[4],port,username,password,msisdn))
        f = threading.Thread(name='daemon5', target=daemon5, args=(ggsnlist[5],port,username,password,msisdn))
        g = threading.Thread(name='daemon6', target=daemon6, args=(ggsnlist[6],port,username,password,msisdn))
        a.setDaemon(True),b.setDaemon(True),c.setDaemon(True),d.setDaemon(True),e.setDaemon(True),f.setDaemon(True),g.setDaemon(True)
        a.start(),b.start(),c.start(),d.start(),e.start(),f.start(),g.start()
        a.join(),b.join(),c.join(),d.join(),e.join(),f.join(),g.join()
    elif num ==8:
        a = threading.Thread(name='daemon', target=daemon, args=(ggsnlist[0],port,username,password,msisdn))
        b = threading.Thread(name='daemon1', target=daemon1, args=(ggsnlist[1],port,username,password,msisdn))
        c = threading.Thread(name='daemon2', target=daemon2, args=(ggsnlist[2],port,username,password,msisdn))
        d = threading.Thread(name='daemon3', target=daemon3, args=(ggsnlist[3],port,username,password,msisdn))
        e = threading.Thread(name='daemon4', target=daemon4, args=(ggsnlist[4],port,username,password,msisdn))
        f = threading.Thread(name='daemon5', target=daemon5, args=(ggsnlist[5],port,username,password,msisdn))
        g = threading.Thread(name='daemon6', target=daemon6, args=(ggsnlist[6],port,username,password,msisdn))
        h = threading.Thread(name='daemon7', target=daemon7, args=(ggsnlist[7],port,username,password,msisdn))
        a.setDaemon(True),b.setDaemon(True),c.setDaemon(True),d.setDaemon(True),e.setDaemon(True),f.setDaemon(True),g.setDaemon(True),h.setDaemon(True)
        a.start(),b.start(),c.start(),d.start(),e.start(),f.start(),g.start(),h.start()
        a.join(),b.join(),c.join(),d.join(),e.join(),f.join(),g.join(),h.join()
    elif num ==9:
        a = threading.Thread(name='daemon', target=daemon, args=(ggsnlist[0],port,username,password,msisdn))
        b = threading.Thread(name='daemon1', target=daemon1, args=(ggsnlist[1],port,username,password,msisdn))
        c = threading.Thread(name='daemon2', target=daemon2, args=(ggsnlist[2],port,username,password,msisdn))
        d = threading.Thread(name='daemon3', target=daemon3, args=(ggsnlist[3],port,username,password,msisdn))
        e = threading.Thread(name='daemon4', target=daemon4, args=(ggsnlist[4],port,username,password,msisdn))
        f = threading.Thread(name='daemon5', target=daemon5, args=(ggsnlist[5],port,username,password,msisdn))
        g = threading.Thread(name='daemon6', target=daemon6, args=(ggsnlist[6],port,username,password,msisdn))
        h = threading.Thread(name='daemon7', target=daemon7, args=(ggsnlist[7],port,username,password,msisdn))
        i = threading.Thread(name='daemon8', target=daemon8, args=(ggsnlist[8],port,username,password,msisdn))
        a.setDaemon(True),b.setDaemon(True),c.setDaemon(True),d.setDaemon(True),e.setDaemon(True),f.setDaemon(True),\
        g.setDaemon(True),h.setDaemon(True),i.setDaemon(True)
        a.start(),b.start(),c.start(),d.start(),e.start(),f.start(),g.start(),h.start(),i.start()
        a.join(),b.join(),c.join(),d.join(),e.join(),f.join(),g.join(),h.join(),i.join()
    elif num ==10:
        a = threading.Thread(name='daemon', target=daemon, args=(ggsnlist[0],port,username,password,msisdn))
        b = threading.Thread(name='daemon1', target=daemon1, args=(ggsnlist[1],port,username,password,msisdn))
        c = threading.Thread(name='daemon2', target=daemon2, args=(ggsnlist[2],port,username,password,msisdn))
        d = threading.Thread(name='daemon3', target=daemon3, args=(ggsnlist[3],port,username,password,msisdn))
        e = threading.Thread(name='daemon4', target=daemon4, args=(ggsnlist[4],port,username,password,msisdn))
        f = threading.Thread(name='daemon5', target=daemon5, args=(ggsnlist[5],port,username,password,msisdn))
        g = threading.Thread(name='daemon6', target=daemon6, args=(ggsnlist[6],port,username,password,msisdn))
        h = threading.Thread(name='daemon7', target=daemon7, args=(ggsnlist[7],port,username,password,msisdn))
        i = threading.Thread(name='daemon8', target=daemon8, args=(ggsnlist[8],port,username,password,msisdn))
        j = threading.Thread(name='daemon9', target=daemon9, args=(ggsnlist[9],port,username,password,msisdn))
        a.setDaemon(True),b.setDaemon(True),c.setDaemon(True),d.setDaemon(True),e.setDaemon(True),f.setDaemon(True),\
        g.setDaemon(True),h.setDaemon(True),i.setDaemon(True),j.setDaemon(True)
        a.start(),b.start(),c.start(),d.start(),e.start(),f.start(),g.start(),h.start(),i.start(),j.start()
        a.join(),b.join(),c.join(),d.join(),e.join(),f.join(),g.join(),h.join(),i.join(),j.join()
    elif num ==11:
        a = threading.Thread(name='daemon', target=daemon, args=(ggsnlist[0],port,username,password,msisdn))
        b = threading.Thread(name='daemon1', target=daemon1, args=(ggsnlist[1],port,username,password,msisdn))
        c = threading.Thread(name='daemon2', target=daemon2, args=(ggsnlist[2],port,username,password,msisdn))
        d = threading.Thread(name='daemon3', target=daemon3, args=(ggsnlist[3],port,username,password,msisdn))
        e = threading.Thread(name='daemon4', target=daemon4, args=(ggsnlist[4],port,username,password,msisdn))
        f = threading.Thread(name='daemon5', target=daemon5, args=(ggsnlist[5],port,username,password,msisdn))
        g = threading.Thread(name='daemon6', target=daemon6, args=(ggsnlist[6],port,username,password,msisdn))
        h = threading.Thread(name='daemon7', target=daemon7, args=(ggsnlist[7],port,username,password,msisdn))
        i = threading.Thread(name='daemon8', target=daemon8, args=(ggsnlist[8],port,username,password,msisdn))
        j = threading.Thread(name='daemon9', target=daemon9, args=(ggsnlist[9],port,username,password,msisdn))
        k = threading.Thread(name='daemon10', target=daemon10, args=(ggsnlist[10],port,username,password,msisdn))
        a.setDaemon(True),b.setDaemon(True),c.setDaemon(True),d.setDaemon(True),e.setDaemon(True),f.setDaemon(True),\
        g.setDaemon(True),h.setDaemon(True),i.setDaemon(True),j.setDaemon(True),k.setDaemon(True)
        a.start(),b.start(),c.start(),d.start(),e.start(),f.start(),g.start(),h.start(),i.start(),j.start(),k.start()
        a.join(),b.join(),c.join(),d.join(),e.join(),f.join(),g.join(),h.join(),i.join(),j.join(),k.join()
    elif num ==12:
        a = threading.Thread(name='daemon', target=daemon, args=(ggsnlist[0],port,username,password,msisdn))
        b = threading.Thread(name='daemon1', target=daemon1, args=(ggsnlist[1],port,username,password,msisdn))
        c = threading.Thread(name='daemon2', target=daemon2, args=(ggsnlist[2],port,username,password,msisdn))
        d = threading.Thread(name='daemon3', target=daemon3, args=(ggsnlist[3],port,username,password,msisdn))
        e = threading.Thread(name='daemon4', target=daemon4, args=(ggsnlist[4],port,username,password,msisdn))
        f = threading.Thread(name='daemon5', target=daemon5, args=(ggsnlist[5],port,username,password,msisdn))
        g = threading.Thread(name='daemon6', target=daemon6, args=(ggsnlist[6],port,username,password,msisdn))
        h = threading.Thread(name='daemon7', target=daemon7, args=(ggsnlist[7],port,username,password,msisdn))
        i = threading.Thread(name='daemon8', target=daemon8, args=(ggsnlist[8],port,username,password,msisdn))
        j = threading.Thread(name='daemon9', target=daemon9, args=(ggsnlist[9],port,username,password,msisdn))
        k = threading.Thread(name='daemon10', target=daemon10, args=(ggsnlist[10],port,username,password,msisdn))
        l = threading.Thread(name='daemon11', target=daemon11, args=(ggsnlist[11],port,username,password,msisdn))
        a.setDaemon(True),b.setDaemon(True),c.setDaemon(True),d.setDaemon(True),e.setDaemon(True),f.setDaemon(True),\
        g.setDaemon(True),h.setDaemon(True),i.setDaemon(True),j.setDaemon(True),k.setDaemon(True),l.setDaemon(True)
        a.start(),b.start(),c.start(),d.start(),e.start(),f.start(),g.start(),h.start(),i.start(),j.start(),k.start(),l.start()
        a.join(),b.join(),c.join(),d.join(),e.join(),f.join(),g.join(),h.join(),i.join(),j.join(),k.join(),l.join()
    return out


def find2(port,username,password,msisdn,ggsnlist):
    num = len(ggsnlist)

    threads = []

    for val in range(0, num):
        thread1 = threading.Thread(target=daemon, args=(ggsnlist[val], port, username, password, msisdn))
        #thread1.setDaemon(True)
        thread1.start()
        threads.append(thread1)

    for thread in threads:
        thread.join()

    return out


def find2imsi(port,username,password,imsi,ggsnlist):
    num = len(ggsnlist)

    threads = []

    for val in range(0, num):
        thread1 = threading.Thread(target=daemon1imsi, args=(ggsnlist[val], port, username, password, imsi))
        #thread1.setDaemon(True)
        thread1.start()
        threads.append(thread1)

    for thread in threads:
        thread.join()

    return out

