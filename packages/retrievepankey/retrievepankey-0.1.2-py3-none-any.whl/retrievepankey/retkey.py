import os


def read_key_file(host):
    pwfile = '.panconfkeystore'
    f = open(os.path.expanduser('~') + "/" + str(pwfile))
    for line in f.readlines():
        if line.split(":")[0] == host:
            f.close()
            return line.split(":")[1].strip()
    raise Exception("Unable to find firewall in file, exiting now.")
