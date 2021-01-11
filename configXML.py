# ---Develop-by-KynaB--- #
import xml.etree.cElementTree as cET
import xml.etree.ElementTree as rET
import base64
import datetime
class cgXML:

    initFile = r'.xml'
    @staticmethod
    def __decodeBody(body, dcode, dsep):
        yield base64.b85decode(body.split(' ')[-1]).decode(dcode).split(dsep)

    @staticmethod
    def normFormat(dataInit):
        gen_date = datetime.datetime.now()
        exp_date = gen_date + datetime.timedelta(minutes=int(dataInit['exp']))
        dataInit['exp'] = str(exp_date)
        regist_encode = '|'.join(list(dataInit.values())).encode("utf-16")
        return [base64.b85encode(regist_encode).decode('utf-8'), str(gen_date), str(exp_date)]

    @staticmethod
    def createXML(*args):
        root = cET.Element("xml", version="1.0", encoding="utf-16", signature="ittipon.bangudsareh")
        parent = cET.SubElement(root, "header")
        cET.SubElement(parent, "column", id="1", type="string").text = "ip"
        cET.SubElement(parent, "column", id="2", type="string").text = "pwd"
        cET.SubElement(parent, "column", id="3", type="string").text = "port"
        cET.SubElement(parent, "column", id="4", type="string").text = "usr"
        cET.SubElement(parent, "column", id="5", type="float").text = "exp"
        parent = cET.SubElement(root, "body", delimeter="|")
        cET.SubElement(parent, "auth", gen=args[1]).text = "Basic " + args[0]
        tree = cET.ElementTree(root)
        tree.write(".xml")

    @staticmethod
    def readXML(initFile):
        root = rET.parse(initFile).getroot()
        dcode = root.get('encoding')
        dsep = root.find('body').get('delimeter')
        header = [ i.text for i in root.findall('header/column') ]
        auth_values = [ cgXML().__decodeBody(i.text, dcode, dsep) for i in root.findall('body/auth') ]
        auth_keys = header
        auth = []
        for i in auth_values:
            auth.append(dict(zip(auth_keys, next(i))))
        return auth

    @staticmethod
    def validateExp(exp):
        currect_sec = str(datetime.datetime.now())
        current = datetime.datetime.strptime(currect_sec,'%Y-%m-%d %H:%M:%S.%f').timestamp()
        expire = datetime.datetime.strptime(exp,'%Y-%m-%d %H:%M:%S.%f').timestamp()
        return expire < current

    @staticmethod
    def appendXML(initFile, dataInit):
        [regist_encode, gen_date, exp_date] = cgXML().normFormat(dataInit)
        # Create the root of the ElementTree from file
        xml_tree = rET.parse(initFile)
        subgroup_element = xml_tree.find('body')
        row = rET.Element('auth')
        row.attrib['gen'] = gen_date
        row.text = 'Basic ' + regist_encode
        subgroup_element.append(row)
        new_xml_tree_string = rET.tostring(xml_tree.getroot())
        # print(new_xml_tree_string)
        with open(initFile, "wb") as f:
            f.write(new_xml_tree_string)
        f.close()

    @staticmethod
    def verifyXML(dataInit, config):
        isHave = False
        for i in config:
            if dataInit['usr'] in i['usr'] and dataInit['ip'] in i['ip']:
                return [i, True]
        if not isHave:
            return [dataInit, False]