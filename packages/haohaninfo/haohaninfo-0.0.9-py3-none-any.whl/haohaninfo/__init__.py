import json
import subprocess
import sys

from haohaninfo import GOrder
#from haohaninfo.GOrder import GOQuote
pip_list = subprocess.check_output([sys.executable, '-m', 'pip', 'list', '--outdated', '--format=json']).decode()
json_list = json.loads(pip_list)

for i in json_list:
    if(i['name'] == 'haohaninfo'):
        print('目前版本為: ' + i['latest_version'])
        
