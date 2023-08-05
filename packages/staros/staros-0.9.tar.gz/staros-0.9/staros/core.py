#!/usr/bin/python

from connection import _getsshdata
import connection
import outputparsing
import threadingfind
import datetime
import json


class StarClient:
    def __init__(self, username, password, host, port):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

    def get_subs_msisdn(self, msisdn):
        data = connection._getsshdata3(self.host, self.port, self.username, self.password, "show subscribers msisdn " + msisdn+"\n")
        return outputparsing._getsubscribermsisdn(str(data))

    def get_subs_session_main(self):
        data = connection._getsshdata1(self.host, self.port, self.username, self.password, "show subscribers summary\n")
        return outputparsing._parseshowsess(str(data))

    def get_subs_full_imsi(self,imsi):
        data = _getsshdata(self.host, self.port, self.username, self.password, "show subscribers msisdn " + imsi + "\n")

    def get_enodeb_associat_num(self):
        data = connection._getsshdata2(self.host, self.port, self.username, self.password, "show mme-service enodeb-association summary\n")
        return outputparsing._parseEnodebAssoc(str(data))

    def clear_subs_msisdn(self, msisdn):
        data = connection._getsshdata1(self.host, self.port, self.username, self.password, "clear subscribers msisdn "+msisdn+" -noconfirm\n")
        return outputparsing._parseClearSubsc(str(data))

    def clear_subs_imsi(self, imsi):
        data = connection._getsshdata1(self.host, self.port, self.username, self.password, "clear subscribers imsi "+imsi+" -noconfirm\n")
        return outputparsing._parseClearSubsc(str(data))

    def get_device_info(self):
        data = connection._getsshdata2(self.host, self.port, self.username, self.password, "show version\n")
        return outputparsing._parse_device_info(str(data))

    def get_subs_full_msisdn(self,msisdn):
        data = connection._getsshdata3(self.host, self.port, self.username, self.password, "show subscribers full msisdn " + msisdn + "\n")
        try:
            outputparsing._get_full_subs_sess_info(str(data))
        except:
            return "Subscriber offline"
        #print data

    def clear_dns_cache_all_Gn(self):
        data = connection._getsshdata4dnsClearContextGn(self.host, self.port, self.username, self.password)
        ddd = outputparsing._clear_dns_gn_parse(data)
        if ddd == True:
            return "DNS cache cleared successful"
        else:
            return "Failed"

    def find_subs_core_list(self, msisdn, ggsnlist):
        ooo = threadingfind.find2(self.port, self.username, self.password, msisdn, ggsnlist)
        return ooo

    def find_subs_core_list_imsi(self, imsi, ggsnlist):
        start = datetime.datetime.now()
        ooo = threadingfind.find2imsi(self.port, self.username, self.password, imsi, ggsnlist)
        end = datetime.datetime.now()
        res = end-start
        ooo.update({"seconds": res.total_seconds()})
        return ooo
