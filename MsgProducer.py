# Curl logs and parse it into mongodb
import time
import re
import logging

from utils import sliceArray


from multiprocessing import Process
from pymongo import MongoClient
from elasticsearch import Elasticsearch, TransportError



logging.basicConfig()
logger = logging.getLogger('elasticsearch')
logger.setLevel(logging.ERROR)

servers = ["202.121.179.54", "202.121.179.55", "202.121.179.56", "202.121.179.57", "202.121.179.58", "202.121.179.59"]
#servers = ["202.121.179.42", "202.121.179.46", "202.121.179.47"]
esClient = Elasticsearch(
    servers,
    port=9200,
    http_compress=True,
    timeout=30
)
# Producer, used to get raw log and add to queue
class MessageRetrieverProcess(Process):
    """retrieve message from elastic search server"""
    def __init__(self, scrollTime, winSize, queue, query):
        super(MessageRetrieverProcess, self).__init__()
        self.scrollTime = scrollTime
        self.winSize = winSize
        self.queue = queue
        self.query = query

    def run(self):
        try:
            self.scanAndScroll()
        except Exception as e:
            logger.exception("scan and scroll")
        finally:
            self.exit()

    def exit(self):
        self.queue.close()

    def scanAndScroll(self):
        scrollTime = self.scrollTime
        winSize = self.winSize
        query = self.query
        winRes = esClient.search(
            q=query,
            scroll = scrollTime,
            size = winSize,
            )
        sid = winRes['_scroll_id']
        scrollSize = winRes['hits']['total']
        print('init scrollSize {}'.format(scrollSize))
        if scrollSize == 0:
            return
        else:
            msgList = sliceArray(winRes["hits"]["hits"], 100)
            for msg in msgList:
                self.queue.put(msg)
        # Start scrolling
        while True:
            try:

                perWin = esClient.scroll(scroll_id = sid, scroll = scrollTime)
                sid = perWin['_scroll_id']
                response = perWin['hits']['hits']
                #update scroll size
                if len(response) == 0 :
                    print ('producer done!!!!')
                    break
                msgList = sliceArray(response, 100)
                for msg in msgList:
                    self.queue.put(msg)
            except Exception as e:
                logger.exception("producing...")
                continue