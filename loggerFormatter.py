import logging
from datetime import datetime
import sys

def setupLogger(name, print_level = logging.DEBUG):
	pass
	formater = logging.Formatter(
		fmt="%(levelname)6s %(name)s[%(filename)s.%(lineno)-3d %(asctime)s] %(message)s",
		datefmt='%H:%M:%S',
	)
	time_now = datetime.now().strftime("%Y_%m_%d")
	stream_handler = logging.StreamHandler(sys.stdout)
	stream_handler.setFormatter(formater)
	stream_handler.setLevel(print_level)
	try:
		os.mkdir('log')
	except Exception as e:
		pass
	file_handler = logging.FileHandler('log/{}.{}.log'.format(time_now, name))
	file_handler.setFormatter(formater)
	logger = logging.getLogger(name)
	logger.addHandler(stream_handler)
	logger.addHandler(file_handler)
	logger.setLevel(logging.DEBUG)
	return logger