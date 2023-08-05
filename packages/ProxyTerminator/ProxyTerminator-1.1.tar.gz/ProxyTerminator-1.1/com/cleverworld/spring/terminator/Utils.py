
# need python > 2.7.9
# pip install pyyaml
import yaml
import os
import logging
import traceback


class Utils:

    def __init__(self):
        """
        read configuration information into global variable _conf
        """
        self.config_path = os.path.join(os.path.dirname(__file__), "conf/app.yaml")

        with open(self.config_path, 'r') as f:
            self.conf = yaml.load(f.read())

        self.initLogging()
        self.debug("init", "config file: " + self.config_path)
    #        print(temp['basic_name'])
    #        print(temp['basic_name']['test_name'])
    #        print(temp['basic_name']['selected_name'][0])

    def set(self, key, value):
        self.conf[key] = value


    def get(self, key, devValue = None):
        try:
            return self.conf[key]
        except KeyError:
            return devValue

    def save(self):
        with open(self.config_path, 'r') as f:
            yaml.dump(self.conf, f)



    def initLogging(self):
        try:
            logFileName = self.get("logger")["fileName"]
            logFileName = os.path.join(os.path.dirname(__file__), "../../../../", logFileName)
        except Exception as e:
            logFileName = ""
        logLevel = self.get("logger")["level"]
        if logLevel == "DEBUG":
            self.logLevel = logging.DEBUG
        elif logLevel == "INFO":
            self.logLevel = logging.INFO
        elif logLevel == "WARNING":
            self.logLevel = logging.WARNING
        elif logLevel == "ERROR":
            self.logLevel = logging.ERROR
        elif logLevel == "CRITICAL":
            self.logLevel = logging.CRITICAL
        else:
            self.logLevel = logging.INFO

        logFormat = self.get("logger")["format"]
        logDatefmt = self.get("logger")["datefmt"]

        if logFileName == "":
            logging.basicConfig(level=self.logLevel, format=logFormat, datefmt=logDatefmt)
        else:
            logging.basicConfig(filename=logFileName, level=self.logLevel, format=logFormat, datefmt=logDatefmt)

        self.debug("Utils", "init log success")

    def debug(self, title, msg):
        logging.getLogger().setLevel(self.logLevel)
        logging.debug("[" + title + "] " + msg)

    def info(self, title, msg):
        logging.getLogger().setLevel(self.logLevel)
        logging.info("[" + title + "] " + msg)

    def warn(self, title, msg):
        logging.getLogger().setLevel(self.logLevel)
        logging.warning("[" + title + "] " + msg)

    def error(self, title, msg):
        logging.getLogger().setLevel(self.logLevel)
        logging.error("[" + title + "] " + msg)

    def critical(self, title, msg):
        logging.getLogger().setLevel(self.logLevel)
        logging.critical("[" + title + "] " + msg)


    def printExceptMsg(self, title, msgHead, e):
        msg = self.getExceptMsg(e)
        self.error(title, "%s, %s"%(msgHead, msg))

    def getExceptMsg(self, e):
        # objlist = dir(e)
        # if "args" in objlist:
        #     return e.args[0]
        # elif hasattr(e, "strerror"):
        #     return e.strerror
        # elif hasattr(e, "reason"):
        #     return e.reason
        # elif e == None:
        #     return ""
        # else:
        #     return "can't get exception msg"
        return traceback.format_exc()