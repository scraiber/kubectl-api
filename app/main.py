from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import subprocess
import random
import string
import os

app = FastAPI()

class Item(BaseModel):
    kube_str: str
    yaml_file: List[str]

class Response(BaseModel):
    Output: str
    Error: str

@app.get("/general/{item}", response_model=Response)
async def general_kubectl(item: str):
    if item.startswith("kubectl"):
        input = []
    else:
        input = ["kubectl"]
    input.extend(item.split(" "))
    result = subprocess.run(input, capture_output=True, text=True)
    return {"Output": result.stdout, "Error": result.stderr}


@app.get("/general_json", response_model=Response)
async def general_kubectl_json(request: Item):
    if request.kube_str.count(".yaml") + request.kube_str.count(".yml") >=2:
        return {"Output": "", "Error": "There should be only one YAML in kube_str"}
    #Generate YAML file
    file_name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=30))+".yaml"
    file_path_name = "/cache/"+ file_name
    with open(file_path_name, 'w') as f:
        for item in request.yaml_file:
            f.write("%s\n" % item)

    #Create Kubectl command line string
    if request.kube_str.startswith("kubectl"):
        input = []
    else:
        input = ["kubectl"]
    splitted_kube_str = [item if ("yaml" not in item and "yml" not in item) else file_path_name for item in request.kube_str.split(" ")]  
    input.extend(splitted_kube_str)

    #Execute and remove YAML file
    result = subprocess.run(input, capture_output=True, text=True)
    if os.path.exists(file_path_name):
        os.remove(file_path_name)
    return {"Output": result.stdout, "Error": result.stderr}