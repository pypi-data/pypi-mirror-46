import os
import logging
import yaml
import json

import fiddler.cli_utils


class ExecuteCmd:

    def __init__(self, args):
        self.org = args.org
        self.api_endpoint = args.api_endpoint
        self.auth_key = args.auth_key
        self.data = args.data
        self.project = args.project
        self.model = args.model

    def run(self):
        input_values = {}
        message = 'Not a model directory {}. Rerun this ' \
                  'command from a model directory'
        if not (self.project and self.model and self.data):
            cwd = os.getcwd()
            if not os.path.isfile('model.yaml'):
                print(message.format(cwd))
                return
            path_items = cwd.split(os.sep)
            length = len(path_items)
            if length < 2:
                print(message.format(cwd))
                return

            self.model = path_items[length-1]
            self.project = path_items[length-2]
            print('Executing {}/{}/{}'.format(
                self.org, self.project, self.model))
            logging.info('Executing {}/{}/{}'.format(
                self.org, self.project, self.model))
            with open('model.yaml') as model_file:
                model_yaml = yaml.load(model_file)
                inputs = model_yaml['model']['inputs']
                if not self.data:
                    if inputs:
                        print('Please enter input values')

                    for arg in inputs:
                        prompt = '{} ({}):'.format(
                            arg['column-name'], arg['data-type'])
                        value = input(prompt)
                        input_values[arg['column-name']] = value
        return self.call_endpoint(input_values)

    def call_endpoint(self, input_values):
        if self.data:
            input_json = self.data
        else:
            input_json = json.dumps({'data': input_values})
        url = '{}/execute/{}/{}/{}'.format(
            self.api_endpoint, self.org, self.project, self.model)
        response = fiddler.cli_utils.req_post(self.auth_key, url, input_json)
        fiddler.cli.process_response(response)
        if not self.data:
            logging.info(
                'To rerun this call:\n    fidl execute --data \'{}\''.format(
                    input_json))
        return response
