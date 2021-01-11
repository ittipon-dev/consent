# ---Develop-by-KynaB--- #
import os
import argparse
from argparse import RawTextHelpFormatter
import re
import pandas as pd
import configXML
import datetime, base64

# DB
import teradata
import psycopg2
import jaydebeapi

def __file_choices(choices,fname):
    ext = os.path.splitext(fname)[1][1:]
    if ext not in choices:
       parser.error("file doesn't end with one of {}".format(choices))
    return fname

def __connectDB(auth, dbtype, db):
    if dbtype == 'teradata':
        return teradata.UdaExec(
            appName="test", 
            version="1.0", 
            logConsole=False).connect(
                method="odbc", 
                system=auth['ip'], 
                username=auth['usr'], 
                password=auth['pwd'], 
                driver='Teradata Database ODBC Driver 16.20'
            )
    elif dbtype == 'hawq':
        return psycopg2.connect(
            host=auth['ip'],
            port=auth['port'],
            database=db,
            user=auth['usr'],
            password=auth['pwd']
        )
    elif dbtype == 'hive':
        return jaydebeapi.connect(
            "com.cloudera.hive.jdbc41.HS2Driver",
            "jdbc:hive2://{0}:{1};AuthMech=3;DatabaseName={2}".format(auth['ip'], auth['port'], db),
            [auth['usr'], auth['pwd']],
            "/hdfs/dev/lib/HiveJDBC41.jar")

def __queryDB(conn, cmd):
    curs = conn.cursor()
    return curs.execute(str(cmd))

def __centerWH(auth, cmd, header, out, dbtype, db, isWrite, encoding, delimeter):
    conn = __connectDB(auth, dbtype=dbtype, db=db)
    print('CONNECT DONE')
    df = __handleFrame(__queryDB(conn, cmd), header)
    conn.close()
    if isWrite:
        print('WRITE FRAME')
        __write2(df, out, encoding, header, delimeter)
    else:
        print('ECHO FRAME')
        print(df)

def __handleFrame(curs, header):
    cols = []
    df = None
    if header:
        for i in curs.description:
            col_name = i[0]
            cols.append(col_name)
        record = curs.fetchall()
        df = pd.DataFrame(record)
        df.columns = cols
    else:
        record = curs.fetchall()
        df = pd.DataFrame(record)
    curs.close()
    return df

def __write2(df, out, encode, header, delimeter):
    out, ftype = os.path.splitext(out)
    ftype = ftype.replace('.', '')
    out = r'.'.join(['_'.join( [out, base64.b64encode(str(datetime.datetime.now()).encode('utf-8')).decode('utf-8')] ), ftype])
    print('OUT:', out)
    if ftype == 'xlsx':
        return df.to_excel(out, encoding=encode, index=False, header=header)
    elif ftype == 'csv':
        return df.to_csv(out, encoding=encode, index=False, header=header)
    else:
        return df.to_csv(out, sep=str(delimeter), encoding=encode, index=False, header=header)

parser = argparse.ArgumentParser(description="SCRIPT MODE:\n\tpython generateData.py --script sql_test.sql sql_test.sql --db edwprd_semvrs_imgivr --usr EDW_AU_ALTERYX --ip 192.168.33.122 --out ./test.xlsx\n\nCOMMAND MODE:\n\tpython generateData.py --command \"SELECT CALL_ID, LENGTH(CAST(CALL_ID AS varchar(20))) AS LEN_CALL_ID, PRODUCT_CODE, INCOMING_VDN, TRANSFERRED_VDN, CALLER_ID, STARTTIME, ENDTIME, START_DATE, END_DATE FROM edwprd_semvrs_imgivr.IVR_FACT_CALL WHERE STARTTIME BETWEEN '2020-06-01 00:00:00' AND '2020-06-02 23:59:59' AND LEN_CALL_ID = 18\" --db \"edwprd_semvrs_imgivr\" --usr \"EDW_AU_ALTERYX\" --ip \"192.168.33.122\" --header true", formatter_class=RawTextHelpFormatter)
parser.add_argument("--script", dest='run', help='(*)Script file mode', required=False, type=argparse.FileType('r'), nargs = '+' )
parser.add_argument("--command", dest='run', help='(*)Command line mode', required=False, type=str, default='')
parser.add_argument("--db", dest='db', help='*Database', required=True, type=str)
parser.add_argument("--usr", dest='username', help='*Username', required=True, type=str)
parser.add_argument("--ip", dest='ip', help='*Ip address', required=True, type=str)
parser.add_argument("--out", dest='out', help='Output file (support .xlsx .csv .txt and .dat)', required=False, type = lambda s: __file_choices(('xlsx','csv', 'txt', 'dat'), s))
parser.add_argument("--header", dest='header', help='Display name\'s header (default: false)', required=False, type=bool, default=False)
parser.add_argument("--encoding", dest='encode', help='Encoding (default: utf-8)', required=False, type=str, default='utf-8')
parser.add_argument("--delimeter", dest='deli', help='Delimeter (default: |)', required=False, type=str, default='|')

options = parser.parse_args()
kvOptions = dict(options._get_kwargs())
listKoptions = list(kvOptions.keys())
if 'run' in listKoptions:
    listVoptions = list(kvOptions.values())
    if kvOptions['run']:
        # print(type(kvOptions['run']))
        objcgXML = configXML.cgXML()
        readConfig = objcgXML.readXML(objcgXML.initFile)
        dataInit = {
            'ip': options.ip,
            'usr': options.username
        }
        [auth, isHave] = objcgXML.verifyXML(dataInit, readConfig)
        if isHave:
            if isinstance(kvOptions['run'], list):
                print('SCRIPT MODE')
                for f in options.run:
                    print('RUNNING FILE:', f.name)
                    if options.out:
                        __centerWH(auth=auth, cmd=f.read(), header=options.header, out=options.out, dbtype='teradata', db=options.db, isWrite=True, encoding=options.encode, delimeter=options.deli)
                    else:
                        __centerWH(auth=auth, cmd=f.read(), header=options.header, out=options.out, dbtype='teradata', db=options.db, isWrite=False, encoding=options.encode, delimeter=options.deli)
            else:
                print('COMMAND MODE')
                if options.out:
                    __centerWH(auth=auth, cmd=kvOptions['run'], header=options.header, out=options.out, dbtype='teradata', db=options.db, isWrite=True, encoding=options.encode, delimeter=options.deli)
                else:
                    __centerWH(auth=auth, cmd=kvOptions['run'], header=options.header, out=options.out, dbtype='teradata', db=options.db, isWrite=False, encoding=options.encode, delimeter=options.deli)
        else:
            print('AUTH IS NOT MATCH')
    else:
        print('NEED PARAMETER SCRIPT/COMMAND.')
else:
    print('SOMETHING WRONG')
#     sys.exit("Not found config file.")