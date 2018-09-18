from multiprocessing import Queue


class MessageQueue(object):
	def __init__(self, size, numOfWorkers):
		super(MessageQueue, self).__init__()
		self.size = size
		self.queue = Queue(size)
		self.numOfWorkers = numOfWorkers

	def close(self):
		for i in range(self.numOfWorkers):
			self.queue.put(None)
		self.queue.close()

	def put(self, obj):
		self.queue.put(obj)

	def get(self):
		return self.queue.get()

def main():
	mq =MessageQueue(3)
	mq.put(4)
	print(mq.get())
	mq.close()
	try:
		mq.put(4)
	except AssertionError as e:
		print(e)

if __name__ == '__main__':
	main()
		