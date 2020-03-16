import re
import xmltodict

def get_dict_from_xml(xml_string):

    return xmltodict.parse(xml_string)
