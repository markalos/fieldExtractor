import json
import sys
from pydoc import locate

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

	queueClass = locate(config["queue"]["script"])
	queue = queueClass(config["queue"]["arguments"], numOfConcurrentWorker)

	producerClass = locate(config["producer"]["script"])
	producerClass(config["producer"]["arguments"], queue).start()

	consumerClass = locate(config["consumer"]["script"])
	for i in range(numOfConcurrentWorker):
		consumerClass(config["consumer"]["arguments"], queue).start()

if __name__ == '__main__':
	main()

