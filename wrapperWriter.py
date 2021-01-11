# ---Develop-by-KynaB--- #
import argparse
from argparse import RawTextHelpFormatter
import subprocess
import os

def __file_choices(choices,fname):
    ext = os.path.splitext(fname)[1][1:]
    if ext not in choices:
       parser.error("file doesn't end with one of {}".format(choices))
    return fname

parser = argparse.ArgumentParser(description='develop by ittipon.bangudsareh@krungsri.com')
subparsers = parser.add_subparsers(help='sub-commands help')
registry_parser = subparsers.add_parser('registry', help='Registry for connect DB', description="REGISTRY MODE:\n\tpython wrapperWriter.py registry --ip 172.17.0.1 --port 8080 --usr ittipon --pwd 1234", formatter_class=RawTextHelpFormatter)
registry_parser.add_argument("--ip", dest='ip', help='*IP address to DB', required=True, type=str)
registry_parser.add_argument("--port", dest='port', help='port to DB (default: blank)', required=False, type=str)
registry_parser.add_argument("--usr", dest='usr', help='*Username for sign-in DB', required=True, type=str)
registry_parser.add_argument("--pwd", dest='pwd', help='*Password for sign-in DB', required=True, type=str)
registry_parser.add_argument("--exp", dest='exp', help='expire for config file (default: 5 mintues)', required=False, type=str)
generate_parser = subparsers.add_parser('generate', help='Run script and generate output file', description="SCRIPT MODE:\n\tpython wrapperWriter.py generate --script sql_test.sql sql_test.sql --db edwprd_semvrs_imgivr --usr EDW_AU_ALTERYX --ip 192.168.33.122 --header true\n\nCOMMAND MODE:\n\tpython wrapperWriter.py generate --command \"SELECT CALL_ID, LENGTH(CAST(CALL_ID AS varchar(20))) AS LEN_CALL_ID, PRODUCT_CODE, INCOMING_VDN, TRANSFERRED_VDN, CALLER_ID, STARTTIME, ENDTIME, START_DATE, END_DATE FROM edwprd_semvrs_imgivr.IVR_FACT_CALL WHERE STARTTIME BETWEEN '2020-06-01 00:00:00' AND '2020-06-02 23:59:59' AND LEN_CALL_ID = 18\" --db edwprd_semvrs_imgivr --usr EDW_AU_ALTERYX --ip 192.168.33.122 --header true", formatter_class=RawTextHelpFormatter)
generate_parser.add_argument("--script", dest='run', help='(*)Script file mode', required=False, type = lambda s: __file_choices(('sql','hql', 'hq'), s),  nargs = '+' )
generate_parser.add_argument("--command", dest='run', help='(*)Command line mode', required=False, type=str)
generate_parser.add_argument("--db", dest='db', help='*Database', required=True, type=str)
generate_parser.add_argument("--usr", dest='usr', help='*Username', required=True, type=str)
generate_parser.add_argument("--ip", dest='ip', help='*Ip address', required=True, type=str)
generate_parser.add_argument("--out", dest='out', help='Output file (support .xlsx .csv .txt and .dat)', required=False, type = lambda s: __file_choices(('xlsx','csv', 'txt', 'dat'), s))
generate_parser.add_argument("--header", dest='header', help='Display name\'s header (default: false)', required=False, type=bool)
generate_parser.add_argument("--encoding", dest='encoding', help='Encoding (default: utf-8)', required=False, type=str)
generate_parser.add_argument("--delimeter", dest='delimeter', help='Delimeter (default: |)', required=False, type=str)

options = parser.parse_args()
kvOptions = dict(options._get_kwargs())
listKoptions = list(kvOptions.keys())
if 'run' in listKoptions:
    print('GENERATE-----')
    listVoptions = list(kvOptions.values())
    if kvOptions['run']:
        listCmd = ['python generateData.py']
        if isinstance(kvOptions['run'], list):
            chgRun = 'script'
        else:
            chgRun = 'command'
        for i, j in enumerate(list(kvOptions.keys())):
            j = j.replace('run', chgRun)
            if listVoptions[i]:
                if isinstance(listVoptions[i], list):
                    listCmd.append( '--' + j + ' ' + ' '.join(listVoptions[i]) )
                else:
                    listCmd.append( '--' + j + ' \"' + str(listVoptions[i]) + '\"' )
        cmd = ' '.join(listCmd)
        # print(cmd)
        subprocess.run(cmd)
    else:
        print('Something wrong')
elif 'ip' in listKoptions:
    print('REGISTRY-----')
    listVoptions = list(kvOptions.values())
    if kvOptions['ip']:
        listCmd = ['python registryXML.py']
        for i, j in enumerate(list(kvOptions.keys())):
            if listVoptions[i]:
                listCmd.append( '--' + j + ' \"' + str(listVoptions[i]) + '\"' )
        cmd = ' '.join(listCmd)
        # print(cmd)
        subprocess.run(cmd)
    else:
        print('Something wron')
else:
    print('Please run help command: python wrapperWriter.py -h')