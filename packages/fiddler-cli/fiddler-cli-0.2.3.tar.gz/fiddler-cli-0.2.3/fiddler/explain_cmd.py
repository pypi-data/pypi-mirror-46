import logging
import json

from fiddler.execute_cmd import ExecuteCmd
import fiddler.cli_utils


class ExplainCmd(ExecuteCmd):

    def __init__(self, args):
        super().__init__(args)

    def call_endpoint(self, input_values):
        if self.data:
            input_json = self.data
        else:
            dataset = input('Please enter the name of the dataset: ')
            explanation = input(
                'Please enter the explanation type '
                '(zero_reset|permute|shap): ')
            input_json = json.dumps({
                'data': input_values,
                'dataset': dataset,
                'explanations': [{'explanation': explanation}]
            })

        url = '{}/explain/{}/{}/{}'.format(
            self.api_endpoint, self.org, self.project, self.model)
        response = fiddler.cli_utils.req_post(self.auth_key, url, input_json)
        fiddler.cli.process_response(response)
        return response

        if not self.data:
            logging.info(
                'To rerun this call:\n    fidl explain --data \'{}\''.format(
                    input_json))
