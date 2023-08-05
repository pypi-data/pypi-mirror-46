#!/usr/bin/python

import connection
import re



def mac_parse(mac):
    a = mac.upper()
    pos = a[0] + a[1]
    if pos == "01":
        subscribers_mac = a[2] + a[3] + ":" + a[5] + a[6] + ":" + a[7] + a[8] + ":" + a[10] + a[11] + ":" + a[12] + a[13] + ":" + a[15] + a[16]
    else:
        subscribers_mac = a[0] + a[1] + ":" + a[2] + a[3] + ":" + a[5] + a[6] + ":" + a[7] + a[8] + ":" + a[10] + a[11] + ":" + a[12] + a[13]
    return subscribers_mac


def get_binding_by_ip(ipaddr, host, user, password):

    GET_BINDING = """
           <filter>
              <config-format-text-cmd>
                 <text-filter-spec>| include Remote</text-filter-spec>
              </config-format-text-cmd>
              <oper-data-format-text-block>
                 <exec>show ip dhcp binding """ + ipaddr + """</exec>
              </oper-data-format-text-block>
           </filter>
    """

    with connection.csr_connect(host, port=22, user=user, password=password) as m:
        mac = ""
        hostname = ""
        ssid = ""
        accessinterface = ""
        j = 1
        c = m.get(GET_BINDING)
        c = str(c)
        ccc = c[:c.find('</response>')]
        e7 = re.search(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\s{1,20}(\w{2,4}.\w{2,4}.\w{2,4}.\w{2,4})|\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}\s{1,20}(\w{4}.\w{4}.\w{4})', ccc)
        e8 = re.search(r'Remote id :\s(\S{2,100})', ccc)
        e9 = re.search(r'Active\s{2,40}(\S{2,40})|Selecting\s{2,40}(\S{2,40})', ccc)
        e10 = re.search(r'Circuit id :\s(\S{2,100})', ccc)
        try:
            if e7.group(1) != None:
                mac = mac_parse(e7.group(1))
            else:
                mac = mac_parse(e7.group(2))
        except:
            mac = "Unknown"

        try:
            if e9.group(1) != None:
                accessinterface = e9.group(1)
            else:
                accessinterface = e9.group(2)
        except:
            accessinterface = "Unknown"

        try:
            a1 = e8.group(1).split(":")
            hostname = a1[0]
            ssid = a1[1]
        except:
            try:
                if e8.group(1) != None:
                   if "wireless_public_interface" in e8.group(1):
                       hostname = e10.group(1)
                       ssid ="Unknown"
                   else:
                       hostname = e8.group(1)
                       ssid ="Unknown"
                else:
                   ssid = "Unknown"
                   hostname = "Unknown"
            except:
                ssid = "Unknown"
                hostname = "Unknown"
        answer = {"mac": mac, "iwaginterface": accessinterface, "aphostname": hostname, "SSID": ssid}
        return answer
