#!/usr/bin/python
import re
from additionalparse import _get_subs_info_parse


def _parseshowsess(data):
    a1 = re.search(r'Active:\s{2,100}(\d{1,20})', data)
    a2 = re.search(r'sgw-gtp-ipv4:\s{2,100}(\d{1,20})', data)
    a3 = re.search(r'mme:\s{2,100}(\d{1,20})', data)
    a4 = re.search(r'ggsn-pdp-type-ipv4:\s{2,100}(\d{1,20})', data)
    a5 = re.search(r'sgsn:\s{2,100}(\d{1,20})', data)
    a6 = re.search(r'sgsn-pdp-type-ipv4:\s{2,100}(\d{1,20})', data)
    a7 = re.search(r'pgw-gtp-ipv4:\s{2,100}(\d{1,20})', data)
    a8 = re.search(r'Total\sSubscribers:\s{2,100}(\d{1,20})', data)
    res = {"total": {"Total Subscribers": a8.group(1),
                     "active":a1.group(1)},
           "utran": {"sgsn": a5.group(1),
                     "sgsn-pdp-type-ipv4": a6.group(1),
                     "ggsn-pdp-type-ipv4": a4.group(1)
                     },
           "eutran": {"mme": a3.group(1),
                      "sgw-gtp-ipv4": a2.group(1),
                      "pgw-gtp-ipv4": a7.group(1)
                      }
           }
    return res


def _parseEnodebAssoc(data):
    a1 = re.search(r'Total ENodeB Associations\s{2,100}:\s{1,10}(\d{1,20})', data)
    resp ={"Total ENodeB" : a1.group(1)}
    return resp


def _parseClearSubsc(data):
    a1 = re.search(r'No\ssubscribers\smatch\sthe\sspecified\scriteria', data)
    a2 = re.search(r'Number of subscribers cleared:\s{1,10}(\d{1,20})', data)
    if a1:
        return 'Not found'
    else:
        return 'Cleared: '+a2.group(1)


def _getsubscribermsisdn(data):
    #
    a1 = re.findall(r'.{6}\s\w{8}\s\d{9,20}\s\S+\s+\S+\s+\w{9}', data)
    #a2 = re.findall(r'.{6}\s\w{8}\s\d{9,20}\s\d{5,15}\s+\S+\s+\w{9}', data)
    #a2=[]
    i = 1
    num = 0
    resout={}
    for elem in a1:
        el = re.findall(r'\b\S{3,50}', elem)
        type = _get_subs_info_parse(el[0])
        res = {i: {"sesstype":type,
                          "callid": el[1],
                          "imsi": el[2],
                          "msisdn": el[3],
                          "ip-address": el[4]}}
        num = i
        i+=1
        resout.update(res)

    #for elem1 in a2:
    #    el1 = re.findall(r'\b\S{3,50}', elem1)
    #    type1 = _get_subs_info_parse(el1[0])
    #    res1 = {i: {"sesstype":type1,
    #                        "callid": el1[1],
    #                        "imsi": el1[2],
    #                        "msisdn": el1[3],
    #                        "ip-address": el1[4]}}
    #    num = i
    #    i += 1
    #    resout.update(res1)

    resout.update({"sessnum":num})
    return resout


def _parse_device_info(data):
    a1 = re.search(r'\sImage\sVersion:\s{5,70}(\d{1,3}.\d{1,3}.\d{1,3})', data)
    a2 = re.search(r'\sImage Build Number:\s{3,100}(\d{1,20})', data)
    return {"Image Version":a1.group(1), "Image Build Number":a2.group(1)}


def _get_full_subs_sess_info(data):
    a1 = data.split("CAE Server Address")
    resout1 = {}
    num1=1
    for sess in a1:
        e1 = re.search(r'Username:\s(\d{5,20})|Username:\s{1,3}(.{3})', sess)
        user = ""
        if e1.group(1) is not None:
            user = e1.group(1)
        else:
            user = e1.group(2)
        e2 = re.search(r'source context:\s{1,3}(\S{1,20})', sess)
        e3 = re.search(r'destination context:\s{1,3}(\S{1,20})', sess)
        e4 = re.search(r'ip address:\s{1,3}(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})', sess)
        e5 = re.search(r'Nat ip address:\s{1,3}(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})', sess)
        natip = None
        try:
            natip = e5.group(1)
        except:
            natip = None
        e6 = re.search(r'ip pool name:\s{1,3}(\S{2,40})', sess)
        ippool = None
        try:
            ippool = e6.group(1)
        except:
            ippool = None
        e7 = re.search(r'\smsid:\s{1,3}(\d{5,20})', sess)
        res ={num1:
                  {
                      "Username" : user,
                      "source context" : e2.group(1),
                      "destination context" : e3.group(1),
                      "ip address" : e4.group(1),
                      "Nat ip address" : natip,
                      "ip pool name" : ippool,
                      "msid": e7.group(1),
                  }
              }
        num1+=1
        print res

    a2 = re.search(r'\sImage Build Number:\s{3,100}(\d{1,20})', data)
    #return {"Image Version":a1.group(1), "Image Build Number":a2.group(1)}


def _clear_dns_gn_parse(data):
    if re.search(r'(Cache cleared for the specificied criteria)', data).group(1) == 'Cache cleared for the specificied criteria':
        return True
    else:
        return False


def _parse_hostname(data):
    return re.search(r'.local.(\S{3,20})#', data).group(1)
