import json
import re
from datetime import datetime
import time

from multiprocessing import Pool, Process

from MongoClient import DBManager

from loggerFormatter import setupLogger

logger = setupLogger("JsonConfigedParser")

class JsonConfigedParser(Process):
    """get message from server and save into mongo DB"""
    def __init__(self, config, queue):
        super(JsonConfigedParser, self).__init__()

        self.config = config
        self.tableName = config['tableName']
        self.fields = config['fields'] # dict : key - field Name to be extracted, value - reg rule for extracting the filed
        self.colNames = list(config['fields'].keys())
        self.queue = queue

        

    def run(self):
        #to do : create mongo DB table
        try:
            self.db = DBManager(dbName = 'elastic', collection = self.tableName,
                host = 'mongodb://202.121.179.53', port = 27017)
            queue = self.queue
            patterns = self.buildPatterns()
            colNames = self.colNames
            while True:
                task = queue.get()
                if task is None:
                    break
                self.extractFieldsFromMessages(task, patterns, colNames)
        except Exception as e:
            logger.exception(e)


    @staticmethod
    def fromJsonFile(fileName : str):
        with open(fileName, 'r') as fsrc:

            config = json.load(fsrc)
        return JsonConfigedParser(config)

    @staticmethod
    def compileRegex(pattern):
        # pattern = re.escape(pattern)
        return re.compile(pattern)



    def buildPatterns(self):
        patterns = self.fields.copy()
        for k in patterns.keys():
            patterns[k] = JsonConfigedParser.compileRegex(patterns[k])
        return patterns


    def extractFieldsFromMessages(self, msgs, patterns, colNames):
        '''
            extracting in serial manner
        '''
        
        res = []
        for msg in msgs:
            try:
                row = dict()
                msg = msg["_source"]["message"]
                for col in colNames:
                    match = patterns[col].search(msg).group(1)
                    row[col] = match
                res.append(row)
            except Exception as e:
                logger.exception(e)
                logger.debug(msg)
        self.db.insertMany(res)


if __name__ == '__main__':
    parser = JsonConfigedParser.fromJsonFile('config.json')
    parser.extractFieldsFromMessages(["Sep 18 00:21:18 mailstore21 mailboxlog 2018-09-18 00:21:18,787 INFO [ImapServer-138] [name=djd123@sjtu.edu.cn;ip=202.121.179.31;oip=220.181.15.247;via=iPhone Mail/(null),202.112.26.54(nginx/1.2.0-zimbra);ua=Zimbra/8.6.0_GA_1229;] imap - user djd123@sjtu.edu.cn authenticated, mechanism=LOGIN", "Sep 18 00:21:19 mailstore22 mailboxlog 2018-09-18 00:21:16,499 INFO [ImapServer-726] [name=sjtu_yzh@sjtu.edu.cn;ip=202.121.179.31;oip=180.158.38.21;via=202.112.26.54(nginx/1.2.0-zimbra);ua=Zimbra/8.6.0_GA_1229;] imap - user sjtu_yzh@sjtu.edu.cn authenticated, mechanism=LOGIN path:/data/zimbra/mailbox.log @timestamp:September 18th 2018, 00:21:16.499"])
    print(time.mktime(datetime.strptime("2018-09-18 00:21:18,787", '%Y-%m-%d %H:%M:%S,%f').timetuple()))
