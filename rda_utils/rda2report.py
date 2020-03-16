import os
import xmlutil
import strutil
import json
import re

def get_raw_files(rda_path, extension):

    files = []

    for dirpath, dirnames, filenames in os.walk(rda_path):
        for filename in filenames:
            if filename.endswith(extension):
                full_path = os.path.join(dirpath, filename)
                with open(full_path, 'r') as f:
                    raw_file = f.read()
                    files.append(raw_file)

    return files

def get_domain_report(rda_path):

    result = {
        'rda-path': rda_path,
        'domains': []
    }

    xml_main_config_list = get_raw_files(rda_path, 'config_xml.txt')
    xml_jms_config_list = get_raw_files(rda_path, 'jms_xml.txt')
    xml_jdbc_config_list = get_raw_files(rda_path, 'jdbc_xml.txt')

    for xml_text in xml_main_config_list:
        try:
            domain_data = xmlutil.get_dict_from_xml(
                    strutil.get_enclosed_text(xml_text, '<domain', '</domain>')
            )['domain']
        except ValueError:
            continue
        
        domain_name = domain_data['name']

        domain_data['jms-modules'] = []
        for xml_text in xml_jms_config_list:
            if "domains/" + domain_name + "/config" in xml_text:
                module_name_search = re.search('---\+ Display of (.*)-jms\.xml File', xml_text, re.IGNORECASE)

                module_name = None
                if module_name_search:
                    module_name = module_name_search.group(1)

                module_data = xmlutil.get_dict_from_xml(
                    strutil.get_enclosed_text(xml_text, '<weblogic-jms', '</weblogic-jms>')
                )['weblogic-jms']
                module_data['name'] = module_name
                domain_data['jms-modules'].append(
                    module_data
                )

        domain_data['jdbc-datasources'] = []
        for xml_text in xml_jdbc_config_list:
            if "domains/" + domain_name + "/config" in xml_text:
                domain_data['jdbc-datasources'].append(
                    xmlutil.get_dict_from_xml(
                        strutil.get_enclosed_text(xml_text, '<jdbc-data-source', '</jdbc-data-source')
                    )['jdbc-data-source']
                )

        result['domains'].append(domain_data)

    return result

