import config
import pathlib
import os
import rda2report
import report2html
import json
from xhtml2pdf import pisa
import io
import shutil

BASE_PATH = pathlib.Path(__file__).parent.absolute()
DEFAULT_OUTPUT_PATH = os.path.join(BASE_PATH, '..','dist')

def process():
    pathlib.Path(os.path.join('..', 'dist')).mkdir(parents=True, exist_ok=True)

    output_path = DEFAULT_OUTPUT_PATH

    if not config.OUTPUT_PATH == 'dist':
        output_path = config.OUTPUT_PATH

    for rda_collection in config.COLLECTIONS:

        machine_name = rda_collection['machine-name']
        context = rda_collection['context']
        rda_path = rda_collection['path']

        print('Processing ', machine_name, context)

        machine_report = rda2report.get_domain_report(rda_path)
        for domain in machine_report['domains']:
            domain_name = domain['name']
            domain['context'] = context
            domain['machine-name'] = machine_name

            html_generic_report = report2html.get_html_generic_report(domain)

            # Save to html
            with open(os.path.join(output_path, 'rda-' + context + '-' + machine_name + '-' + domain_name + '.html'), 'w') as f:
                f.write(html_generic_report)

            # Save to json
            with open(os.path.join(output_path, 'rda-' + context + '-' + machine_name + '-' + domain_name + '.json'), 'w') as f:
                f.write(json.dumps(domain, indent = 4))

            # Save to PDF
            #pdf_result = io.BytesIO()
            #pdf = pisa.pisaDocument(html_generic_report, dest=pdf_result)
            #with open(os.path.join(output_path, 'rda-' + context + '-' + machine_name + '-' + domain_name + '.pdf'), 'wb') as f:
            #    pdf_result.seek (0)
            #    f.write(pdf_result.read())

            print('   ', domain_name, 'OK')

    print('Successful outputs saved at', output_path)

