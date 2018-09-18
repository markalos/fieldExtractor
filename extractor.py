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
	config = jsonLoader(configFile)
	numOfConcurrentWorker = int(config['worker'])
	queue = MessageQueue(config["queue"]["arguments"], numOfConcurrentWorker)
	MessageRetrieverProcess(config["producer"]["arguments"], queue).start()
	for i in range(numOfConcurrentWorker):
		JsonConfigedParser(config["comsumer"]["arguments"], queue).start()

if __name__ == '__main__':
	main()

