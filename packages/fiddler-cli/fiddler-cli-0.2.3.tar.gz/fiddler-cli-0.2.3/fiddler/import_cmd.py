import os
import fiddler.cli_utils


class ImportCmd:

    def __init__(self, args):
        self.org = args.org
        self.api_endpoint = args.api_endpoint
        self.auth_key = args.auth_key

    def run(self):
        message = 'Not a dataset directory {}. Rerun this ' \
                  'command from a dataset directory'
        cwd = os.getcwd()
        dataset = cwd.split(os.sep)[-1]
        if not os.path.isfile('{}.yaml'.format(dataset)):
            print(message.format(cwd))
            return

        path_items = cwd.split(os.sep)
        length = len(path_items)
        if length < 2:
            print(message.format(cwd))
            return

        url = '{}/import_dataset/{}/{}'.format(
            self.api_endpoint,
            self.org,
            dataset
        )
        print('Calling {}\n'.format(url))
        resp = fiddler.cli_utils.req_get(self.auth_key, url)
        fiddler.cli.process_response(resp)
        return resp
