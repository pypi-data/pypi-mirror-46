#
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4:
#

# -- essential utils
import os
import sys

from ruamel.yaml import YAML
import logging
import pprint

# -- read a yml dict
def readConf(file):
    with open(file,"rb") as fp:
        d=fp.read()
        yaml=YAML(typ='safe')   # default, if not specfied, is 'rt' (round-trip)
        cdict=yaml.load(d)
        return cdict

def ppr(cdict):
    pp=pprint.PrettyPrinter(indent=1)
    pp.pprint(cdict)

def ppf(cdict):
    pp=pprint.PrettyPrinter(indent=1)
    return pp.pformat(cdict)


# -- print a message and exit
def die(msg,exitCode=1):
    progname = os.path.basename(sys.argv[0])
    sys.stderr.write(("{}: {}\n".format(progname,msg)))
    sys.exit(exitCode)

# -- generate all words in file
def words(file):
    with open(file,'r') as f:
        if os.stat((f.name)).st_size == 0:
            logging.error("Log file '{}' is empty".format(f.name))
        for line in f:
            if (line.strip().isdigit()):
                logging.debug("Fetching results for process with pid-id : {}".format(line))
                for word in line.split():
                    yield word.strip()
            else:
                logging.error("'{}' file should include only integer values. Value {} is not acceptable".format(f.name, line))
                continue
