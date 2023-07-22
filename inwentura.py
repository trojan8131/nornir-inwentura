from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get
from tabulate import tabulate
import re
from pprint import pprint
import csv



tablica_inwentura=[]


def inwentura(task):
    try:
        informacje=task.run(task=napalm_get,getters=["get_interfaces_ip","get_facts","get_snmp_information"])
        #print_result(informacje)
    except:
        tablica_inwentura.append([task.host.hostname,"failed","failed","failed","failed","failed","failed","failed"])
        return
    facts=informacje.result["get_facts"]
    version=facts["os_version"]
    regex=r"(Version\s\d+\.\d+)"
    matches=re.search(regex,version)
    if matches:
        version=matches.group(1)
    #print(version)

    ip_prefix_list=[]

    for interface,data in informacje.result["get_interfaces_ip"].items():
        try:
            for address,prefix in data["ipv4"].items():
                ip_prefix_list.append(f"{interface}: {address}/{prefix['prefix_length']}")
        except:
            pass
    ip_prefix_string=' , '.join(ip_prefix_list)
    #print(ip_prefix_string)

    tablica_inwentura.append([facts["hostname"],facts["uptime"],facts["model"],facts["vendor"],version,informacje.result["get_snmp_information"]["location"],ip_prefix_string])





nr=InitNornir(config_file="config.yaml")


result=nr.run(task=inwentura)

print(tabulate(tablica_inwentura))

with open("inwentura.csv",mode="w",newline="") as csv_file:
    writer=csv.writer(csv_file,delimiter=";")
    for row in tablica_inwentura:
        writer.writerow(row)

