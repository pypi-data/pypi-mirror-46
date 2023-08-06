import os
def check():
    for i in ['lspci','dmidecode']:
        if not os.path.exists(os.path.join('/usr/bin',i)):
            print('missing {}'.format(i))
            raise Exception('Missing {}'.format(os.path.join('/usr/bin',i)))
check()
