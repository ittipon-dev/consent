# ---Develop-by-KynaB--- #
import os
import argparse
from argparse import RawTextHelpFormatter
import re
import configXML
objcgXML = configXML.cgXML()

def __initialConfig(dataInit):
    if not os.path.isfile(objcgXML.initFile):
        [regist_encode, gen_date, exp_date] = objcgXML.normFormat(dataInit)
        objcgXML.createXML(regist_encode, gen_date, exp_date)
        return 'create'
    else:
        return __getConfigXML()

def __getConfigXML():
    objcgXML = configXML.cgXML()
    if os.path.isfile(objcgXML.initFile):
        return objcgXML.readXML(objcgXML.initFile)
    else:
        return 'Please pass parameters: username and password for create config file'
    
def __setConfigXML(dataInit):
    objcgXML = configXML.cgXML()
    if os.path.isfile(objcgXML.initFile):
        return objcgXML.appendXML(objcgXML.initFile, dataInit)
    else:
        return 'Please pass parameters: username and password for create config file'

def __verifySetConfigXML(dataInit, config):
    isHave = False
    for i in config:
        if dataInit['usr'] in i['usr'] and dataInit['pwd'] in i['pwd'] and dataInit['ip'] in i['ip']:
            print('It\'s been auth.')
            isHave = True
            break

    if not isHave:
        print('Auth done')
        return __setConfigXML(dataInit)

parser = argparse.ArgumentParser(description="usage: python registryXML.py --ip 172.17.0.1 --port 8080 --usr ittipon --pwd 1234", formatter_class=RawTextHelpFormatter)
parser.add_argument("--ip", dest='ip', help='*IP address to DB', required=True, type=str)
parser.add_argument("--port", dest='port', help='port to DB (default: blank)', required=False, type=str, default='')
parser.add_argument("--usr", dest='username', help='*Username for sign-in DB', required=True, type=str)
parser.add_argument("--pwd", dest='password', help='*Password for sign-in DB', required=True, type=str)
parser.add_argument("--exp", dest='expire', help='expire for config file (default: 5 mintues)', required=False, type=str, default='5')

options = parser.parse_args()
sc_primary = options.ip and options.username and options.password
if sc_primary :
    dataInit = {
        'ip': options.ip,
        'pwd': options.password,
        'port': options.port,
        'usr': options.username,
        'exp': options.expire
    }
    # set config value
    config = __initialConfig(dataInit)
    if config == 'create':
        config = __getConfigXML()
        print('create', config)
    else:
        print('read', config)
        __verifySetConfigXML(dataInit, config)
else:
    print('Please pass parameter that\'s script required.')
#     sys.exit("Not found config file.")