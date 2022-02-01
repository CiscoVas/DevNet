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
    print("Send only one text value as argument of the script and try again to DELETE paths!!!")
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

if len(info['imdata']) == 0:
    print("Nothing to delete!")
    exit()

for inf in info['imdata']:
    #tDn = inf['fvRsPathAtt']['attributes']['tDn'] 
    dnParse = inf['fvRsPathAtt']['attributes']['dn'].split("/")
    
    tenant = dnParse[1].partition("tn-")[2]
    ap = dnParse[2].partition("ap-")[2]
    epg = dnParse[3].partition("epg-")[2]
    path_name = dnParse[7].partition("pathep-")[2]

    print(f'TENANT = {tenant} AP = {ap} EPG = {epg} PATH_NAME = {path_name}  --- candidate to delete')

deleteChose = str(input('Do you realy want to delete paths above?!? Enter "Y"/"y" to delete: '))
if deleteChose != "Y" and deleteChose != "y":
    print("Delete operartion CANCELED!!!")
    exit()

for inf in info['imdata']:
    dnFull = inf['fvRsPathAtt']['attributes']['dn']
    dnParse = inf['fvRsPathAtt']['attributes']['dn'].split("/")
    
    tenant = dnParse[1].partition("tn-")[2]
    ap = dnParse[2].partition("ap-")[2]
    epg = dnParse[3].partition("epg-")[2]
    path_name = dnParse[7].partition("pathep-")[2]

    url3 = f"{apic_url}api/node/mo/{dnFull}.json"
    print("URL3 = " + url3)
    
'''
    payload = {
        "fvRsPathAtt":{
            "attributes":{
                "dn": dnFull,
                "status":"deleted"
            },
        "children":[   ]
        }
    }
 
    resp = requests.post(url3, verify=False, cookies=cookies, json=payload)
    print(f'TENANT = {tenant} AP = {ap} EPG = {epg} PATH_NAME = {path_name}  --- DELETED')
'''
    
    
