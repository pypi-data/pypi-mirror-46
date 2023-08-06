from ConfigParser import SafeConfigParser
from . import const
import sys
import os

def getConfig(section, key, dataType=str):
    if not os.path.exists(const.SETTING_FILE):
        print "Please run gacrawler-init first"
        sys.exit("Exit: No Configuration File Found")
    parser = SafeConfigParser()
    parser.read(const.SETTING_FILE)
    try:
        if dataType == int:
            return parser.getint(section, key)
        elif dataType == float:
            return parser.getfloat(section, key)
        else:
            return parser.get(section, key)
    except Exception as ex:
        sys.exit('Error Reading Configuration: ' + str(ex))