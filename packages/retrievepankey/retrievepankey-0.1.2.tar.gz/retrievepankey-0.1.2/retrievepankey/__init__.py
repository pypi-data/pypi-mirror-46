import os.path


def read_key_file(host, pwfile='.panconfkeystore', splitchar=":", searchpos=0, retpos=1, includehomedir=True):
    if includehomedir == True:
        pathstring = os.path.expanduser('~') + "/" + str(pwfile)
    else:
        pathstring = pwfile
    with open(os.path.expanduser('~') + "/" + str(pwfile)) as f:
        for line in f.readlines():
            if line.split(":")[searchpos] == host:
                return line.split(":")[retpos].strip()
    raise Exception("Unable to find firewall in file, exiting now.")
