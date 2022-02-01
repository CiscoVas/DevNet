import requests 
import os
import sys

#SET OS VARIABLES TO MAKE SCRIPT WORK
#export APIC_URL=https://oc-apic1.btsdapps.net/   (or your apic https url)
#export APIC_LOGIN=enter_apic_username
#export APIC_PASSWORD=enter_apic_username_password


#api/node/class/fvAEPg.json   --- all EPGs with tenant && AP (need to parse dn attribute)
#api/node/class/fvAp.json     --- all Application Profiles 
#api/node/class/fvTenant.json --- all Tenants (name param)
#url3 = os.environ.get("APIC_URL") + "api/node/class/fvRsPathAtt.json" --- all STATIC PORTS for EPGs
#https://oc-apic1.btsdapps.net/api/node/class/fvRsPathAtt.json?query-target-filter=wcard(fvRsPathAtt.tDn, "VPC_SRV31-2_INTPG")--- filter if you some snippets of tDn 

#https://oc-apic1.btsdapps.net/api/node/mo/uni/tn-common/ap-SHARED_INFRA_AP/epg-INFRA_CEPH_MGNT_EPG.json
#https://oc-apic1.btsdapps.net/api/node/mo/uni/tn-common/ap-SHARED_INFRA_AP/epg-INFRA_CEPH_CLUSTER_EPG.json
#https://oc-apic1.btsdapps.net/api/node/mo/uni/tn-common/ap-SHARED_INFRA_AP/epg-INFRA_CEPH_PUBLIC_EPG.json


if len(sys.argv) != 2 : 
    print("Send only one text value as argument of the script and try again!!!")
    exit()

if os.environ.get("APIC_URL") == "" or os.environ.get("APIC_LOGIN") == "" or os.environ.get("APIC_PASSWORD") == "":
    print('Set values for all of the OS environment variables "APIC_URL" or "APIC_LOGIN" or "APIC_PASSWORD"!!!')
    exit()

url = os.environ.get("APIC_URL") + "api/aaaLogin.json"
login = os.environ.get("APIC_LOGIN")
password = os.environ.get("APIC_PASSWORD")
vpc_path = sys.argv[1]


payload = {
    "aaaUser" : {
        "attributes" : {
            "name" : login,
            "pwd" : password
        }
    }
}

print("**************************")
print("**************************")
print()
resp = requests.post(url, json=payload, verify=False)

info = resp.json()
token = (info['imdata'][0]['aaaLogin']['attributes']['token'])
print(token)
cookies={
    'APIC-Cookie' : token
}


# url = os.environ.get("APIC_URL"+"/api/node/mo/uni/tn" + $tanant + "/ap-" + $ap + "/epg-" + epg + ".json")
# $APIC_URL/api/node/mo/uni/tn-$TENANT/ap-$AP/epg-$EPG.json
apic_url = os.environ.get("APIC_URL")
url2 = f'{apic_url}api/node/class/fvRsPathAtt.json?query-target-filter=wcard(fvRsPathAtt.tDn, "{vpc_path}")'
print(url2)
print("**************************************")
resp = requests.get(url2, verify=False, cookies=cookies)
info = resp.json()

#print(len(info['imdata']))

for inf in info['imdata']:
    tDn = inf['fvRsPathAtt']['attributes']['tDn'] 
    dnFull = inf['fvRsPathAtt']['attributes']['dn']
    dnParse = inf['fvRsPathAtt']['attributes']['dn'].split("/")
    
    tenant = dnParse[1].partition("tn-")[2]
    ap = dnParse[2].partition("ap-")[2]
    epg = dnParse[3].partition("epg-")[2]
    path_name = dnParse[7].partition("pathep-")[2]
    print(f'TENANT = {tenant} AP = {ap} EPG = {epg} PATH_NAME = {path_name}')
    #print(dnParse)

'''
    #url: https://oc-apic1.btsdapps.net/api/node/mo/uni/tn-common/ap-SHARED_INFRA_AP/epg-INFRA_CEPH_CLUSTER_EPG/rspathAtt-[topology/pod-1/protpaths-105-106/pathep-[VPC_SRV31-2_INTPG]].json
    #url3 = f"{apic_url}api/node/mo/uni/{tenant}/{ap}/{epg}.json"
    url3 = f"{apic_url}api/node/mo/{dnFull}.json"
    print("URL3 = " + url3)
    payload = {
        "fvRsPathAtt":{
            "attributes":{
                "dn": dnFull,
                "status":"deleted"
            },
        "children":[   ]
        }
    }
 
    print("Payload= " + str(payload))
    print("**************************************")

    resp = requests.post(url3, verify=False, cookies=cookies, json=payload)
    print(resp.text)
    break
'''

'''
#PARSE dn to get tenant, application profile, epg
for inf in info['imdata']:
    epg_item = inf['fvAEPg']['attributes']['dn'].split("/")
    #url3 = os.environ.get("APIC_URL") + "api/node/mo/uni/tn-" + tanant_item + ".json"
    #url3 = os.environ.get("APIC_URL") + "api/node/class/fvAp.json"
    print("Tenant = " + epg_item[1].partition("tn-")[2])
    print("AP = " + epg_item[2].partition("ap-")[2])
    print("EPG = " + epg_item[3].partition("epg-")[2])

    tenant = epg_item[1]
    ap = epg_item[2]
    epg = epg_item[3]
    #url3=f"{apic_url}api/node/mo/uni/{tenant}/{ap}/{epg}.json"
    url3 = os.environ.get("APIC_URL") + "api/node/class/fvRsPathAtt.json"
    print(url3)
    print(epg_item)
    print("**************************************")
    print()
    resp = requests.get(url3, verify=False, cookies=cookies)
    info = resp.json()
    print(info)

    break
'''