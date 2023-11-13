import requests
import time
from datetime import datetime

namemc_url = "https://api.namemc.com/server/{server_ip}/likes"
laby_url = "https://laby.net/api/user/{uuid}/get-names"
headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; discord-blockplacer4/1.0; +blockplacer4)'
}

uuid_file = 'uuid_list.txt'
valid_uuid_file = 'valid_uuids.txt'
server_ips_file = 'server_ips.txt'

def get_last_known_username(data):
    last_username = None
    for entry in data:
        if entry.get('username'):
            last_username = entry['username']
    return last_username

def get_uuids_from_response(response_data):
    return response_data if isinstance(response_data, list) else []

def check_uuids(uuid_list):
    for uuid in uuid_list:
        uuid = uuid.strip()
        response = requests.get(laby_url.format(uuid=uuid), headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            last_username = get_last_known_username(data)
            if last_username:
                now = datetime.now()
                print(f"{now} | Invalid | {uuid} | {last_username} | {server_ip}")
                time.sleep(2)
            else:
                print(f"{now} | Valid | {uuid} | {server_ip}")
                with open(valid_uuid_file, 'a') as valid_file:
                    valid_file.write(uuid + '\n')
                    time.sleep(1.7)
        else:
            print(f"Failed UUID: {uuid}")

def remove_server_from_file(server_ip):
    with open('server_ips.txt', 'r') as file:
        lines = file.readlines()
    with open('server_ips.txt', 'w') as file:
        for line in lines:
            if line.strip() != server_ip:
                file.write(line)

with open(server_ips_file, 'r') as server_ips_file:
    server_ips_list = server_ips_file.readlines()

uuid_list = []
for server_ip in server_ips_list:
    server_ip = server_ip.strip()
    response = requests.get(namemc_url.format(server_ip=server_ip), headers=headers)
    
    if response.status_code == 200:
        likes_data = response.json()
        uuid_list = get_uuids_from_response(likes_data)
        uuid_list = list(set(uuid_list))
        check_uuids(uuid_list)
        remove_server_from_file(server_ip)
    else:
        print(f"Error for server IP: {server_ip}")
        time.sleep(5)
