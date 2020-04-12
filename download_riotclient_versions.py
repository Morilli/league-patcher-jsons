import requests
import os
import json
from multiprocessing.pool import ThreadPool

patchlines = ["KeystoneFoundationLiveWin", "KeystoneFoundationBetaWin"]

urls = [(f"Riot Client/{patchline}", f"https://clientconfig.rpg.riotgames.com/api/v1/config/public?version=11.0.0.3165706&patchline={patchline}&app=Riot Client&namespace=keystone.self_update") for patchline in patchlines]

def download_jsons(entry):
    path, url = entry
    # print(path) # Uncomment for testing
    json_file = requests.get(url)
    if json_file.status_code == 200:
        # print(path) # Uncomment for testing
        level = json.loads(json_file.content)["keystone.self_update.level"]
        manifest_url = json.loads(json_file.content)["keystone.self_update.manifest_url"][-25:-9]
        os.makedirs(path, exist_ok=True)
        try:
            with open(f"{path}/{manifest_url}_{level}.json", "xb") as out_file:
                out_file.write(json_file.content)
        except FileExistsError:
            pass

any(ThreadPool(2).imap_unordered(download_jsons, urls))
