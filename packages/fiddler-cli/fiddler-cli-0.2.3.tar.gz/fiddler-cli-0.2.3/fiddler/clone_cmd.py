import logging
import os
import subprocess


class CloneCmd:

    def __init__(self, org, auth):
        self.org = org
        self.auth = auth

    def run(self):
        print('Cloning into repo: {}'.format(self.org))

        proc = subprocess.run('git --version', capture_output=True,
                              shell=True, text=True)
        if proc.returncode != 0:
            logging.error('Failed to run `git` command. '
                          'Please ensure git is installed.')
            return 'git-not-found'
        version = proc.stdout.split(' ')[2:3]
        if not version or version[0] < '2.1':
            logging.error('git version needs to be upgraded. '
                          'Please ensure it is 2.1 or newer.')
            return 'git-version-is-too-old'

        if os.path.exists(self.org):
            logging.info('org exists locally, cannot clone')
            return 'org-exists'

        subprocess.call(['git', 'config', '--global', '--unset-all',
                        'http.http://repo.fiddler.ai.extraheader'])
        subprocess.call(['git', 'config', '--global', '--add',
                         'http.http://repo.fiddler.ai.extraheader',
                         'Authorization: Bearer {}'.format(self.auth)])
        logging.info('Done configuring git')
        if subprocess.call(
            ['git', 'clone',
             'http://repo.fiddler.ai/{}.git'.format(self.org)]) != 0:
            logging.error('\'git clone\' command failed')
            return 'git-clone-failed'
        logging.info('Done cloning git repo')
