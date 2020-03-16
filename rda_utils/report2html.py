import config
import collections

def get_name_value(elem):
    name = elem.get('name')
    if name is None:
        name = elem.get('@name')
    return name

def get_html_generic_section(data):

    output = ''
    if data is None:
        output += '(Sin Valor)'
    elif len(data) == 0:
        pass
    elif isinstance(data, list):
        output += '<table border="1" style="' + config.display_table_style + '">'

        has_name_attribute = (
            (isinstance(data[0], dict) or isinstance(data[0], collections.OrderedDict))
            and 
            (   not data[0].get('name') is None
                or
                not data[0].get('@name') is None
            )
        )

        if has_name_attribute:
            # build headers with name attribute
            output += '<tr>'
            for item in sorted(data, key=get_name_value):
                output += '<th style="' + config.display_table_header_style + '">' + get_name_value(item) + '</th>'
            output += '</tr>'
            output += '<tr>'
            for item in sorted(data, key=get_name_value):
                output += '<td valign="top">' + get_html_generic_section(item) + '</td>'
            output += '</tr>'
        else:
            output += '<tr>'
            for item in data:
                output += '<td valign="top">' + get_html_generic_section(item) + '</td>'
            output += '</tr>'

        output += '</table>'

    elif isinstance(data, dict) or isinstance(data, collections.OrderedDict):
        output += '<table cellspacing="1" border="1" style="' + config.display_inner_table_style + '">'

        index = 0
        for key in data.keys():
            fill_color = '#d5f5e3'

            #if (index % 2) == 0:
            #    fill_color = '#abebc6'
            #else:
            #    fill_color = '#d5f5e3'
            #index += 1

            output += '<tr><td valign="top" bgcolor="' + fill_color + '"><b>' + key + '</b></td><td valign="top">' + get_html_generic_section(data[key]) + '</td></tr>'
            #output += '<tr><td valign="top"><div><b>' + key + '</b></div></td><td valign="top">' + get_html_generic_section(data[key]) + '</td></tr>'

        output += '</table>'
    else:
        output += str(data)

    return output

def get_html_generic_report(report):

    output = '<!DOCTYPE html><html><head><title>Generic Report</title>\n'
    output+= '''
                        <style type="text/css">
                                #customers {
                                        font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                                        border-collapse: collapse;
                                        width: 100%;
                                        }

                                #customers td, #customers th {
                                        border: 1px solid #ddd;
                                        padding: 5px;
                                        font-size: 13px;
                                        }
                                #customers tr:nth-child(even){background-color: #f2f2f2;}

                                #customers tr:hover {background-color: #ddd;}

                                #customers th {
                                        padding-top: 5px;
                                        padding-bottom: 5px;
                                        text-align: left;
                                        background-color: rgb(84, 136, 196);
                                        color: white;
                                        }

                                .title {
                                        font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                                        color:midnightblue;
                                        text-decoration: bold;
                                        text-transform: uppercase;
                                        font-size: 20px;
                                        }

                                .info {
                                        font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                                        color:midnightblue;
                                        font-size: 20px;
                                        }

                        </style>    
    '''

    output+= '</head>\n'
    output+= '<body style="' + config.display_body_style + '">\n'

    output+= '<font class="title">context: </font><font class="info">' + report['context'] + '</font>'
    output+= '<br/><br/><font class="title">machine: </font><font class="info">' + report['machine-name'] + '</font><br/>'

    for section_name in report.keys():
        if section_name in ('context', 'machine-name'):
            continue

        section_data = report[section_name]

        if not section_name.startswith('@'):
            output+= '<br/><font class="title">' + section_name + '</font>'
            if not isinstance(section_data, list) and not isinstance(section_data, dict) and not isinstance(section_data, collections.OrderedDict):
                output+= ':<font class="info"> '  + str(report[section_name]) + '</font><br/>\n'
            else:
                output+= get_html_generic_section(section_data) + '<br/>\n'

    output+= '</body></html>'

    return output
