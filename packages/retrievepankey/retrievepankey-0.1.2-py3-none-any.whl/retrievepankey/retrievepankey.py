import os.path


def read_key_file(host, pwfile='.panconfkeystore', splitchar=":", searchpos=0, retpos=1, includehomedir=True):
    if includehomedir == True:
        pathstring = os.path.expanduser('~') + "/" + str(pwfile)
    else:
        pathstring = pwfile
    with open(os.path.expanduser('~') + "/" + str(pwfile)) as f:
        for line in f.readlines():
            if line.split(":")[0] == host:
                return line.split(":")[1].strip()
    raise Exception("Unable to find firewall in file, exiting now.")


if __name__ == '__main__':
    main()
