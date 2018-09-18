import json
import sys

from MessageQueue import MessageQueue
from MsgProducer import MessageRetrieverProcess
from JsonConfigedParser import JsonConfigedParser

def jsonLoader(fileName : str):
	with open(fileName, 'r') as fsrc:
		
		config = json.load(fsrc)
	return config

def main():
	try:
		configFile = sys.argv[1]
	except Exception as e:
		configFile = 'config.json'
	print(configFile)
	return
	config = jsonLoader(configFile)
	numOfConcurrentWorker = int(config['worker'])
	queue = MessageQueue(100, numOfConcurrentWorker)
	MessageRetrieverProcess("20m", 1000, queue, config['query']).start()
	for i in range(numOfConcurrentWorker):
		JsonConfigedParser(config, queue).start()

if __name__ == '__main__':
	main()

