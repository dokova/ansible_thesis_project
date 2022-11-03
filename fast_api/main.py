from fastapi import FastAPI, Response, status
import ansible_runner
import json
import ipaddress
from datetime import date
from pydantic import BaseModel

app = FastAPI()

PREFIX_FILE = r"/home/domty/ansible_thesis_project/generated_data/prefixes/prefix.json"
NMAP_INVENTORY_FILE = f"/home/domty/ansible_thesis_project/generated_data/prefix_for_nmap/{date.today()}.address"



class Prefix(BaseModel):
    name: str

def read_file(file):
    with open(file, 'r') as j:
        return json.loads(j.read())  

def write_json_file(file, data):
    with open(file, "w") as outfile:
        outfile.write(json.dumps(data, indent=4))    

def create_nmap_inventory():
    data = read_file(PREFIX_FILE)
    with open(NMAP_INVENTORY_FILE, 'w') as d:
        for prefix in data["prefix"]:
            d.write(prefix + "\n")

@app.get("/")
async def root():
    return {"message": "Welcome here. You can use /scan to start scanning. /update to update the inventory"}


@app.get("/prefixes/")
async def get_prefixes():
    return read_file(PREFIX_FILE)


@app.post("/prefixes/remove/")
async def post_prefix(prefix : Prefix, response: Response):
    data = read_file(PREFIX_FILE)
    if prefix.name not in data["prefix"]:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": "Prefix does not exist"}

    data["prefix"].remove(prefix.name)
    write_json_file(PREFIX_FILE, data)
    return data


@app.post("/prefixes/add/")
async def post_prefix(prefix : Prefix, response: Response):
    try:
        ipaddress.ip_network(prefix.name)
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"Error": str(e)}

    data = read_file(PREFIX_FILE)

    if prefix.name in data["prefix"]:
        response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        return {"Error": "Prefix already exist"}

    data["prefix"].append(prefix.name)
    print ("asd")
    with open(PREFIX_FILE, "w") as outfile:
        outfile.write(json.dumps(data, indent=4))

    return data



@app.get("/scan/")
async def scan():
    create_nmap_inventory()
    r = ansible_runner.run(private_data_dir='/home/domty/ansible_thesis_project', playbook='controller.yaml', )
    print("{}: {}".format(r.status, r.rc))
    for each_host_event in r.events:
        print(each_host_event['event'])
    return r.stats
