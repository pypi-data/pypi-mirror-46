"""
Derived from: https://gist.github.com/schlamar/7003737
MIT License

Copyright (c) 2019, Drew Nutter.
Copyright (c) 2019, Marc Schlaich.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import contextlib
import multiprocessing
import logging
import threading


class Process(multiprocessing.Process):
	"""Use in place of a normal Process, passing the log queue (mp.Queue)"""
	def __init__(self, log_queue, **kwargs):
		kwargs['args'] = (log_queue, kwargs['target']) + tuple(kwargs['args'])
		kwargs['target'] = logged_call
		multiprocessing.Process.__init__(self, **kwargs)


def daemon(log_queue):
	while True:
		try:
			record_data = log_queue.get()
			if record_data is None:
				break
			record = logging.makeLogRecord(record_data)
			logger = logging.getLogger(record.name)
			if logger.isEnabledFor(record.levelno):
				logger.handle(record)
		except (KeyboardInterrupt, SystemExit):
			raise
		except EOFError:
			break
		except:
			logging.exception('Error in log handler.')


class MPLogger(logging.Logger):
	log_queue = None

	def isEnabledFor(self, level):
		return True

	def handle(self, record):
		ei = record.exc_info
		if ei:
			# to get traceback text into record.exc_text
			logging._defaultFormatter.format(record)
			record.exc_info = None  # not needed any more
		d = dict(record.__dict__)
		d['msg'] = record.getMessage()
		d['args'] = None
		self.log_queue.put(d)


def logged_call(log_queue, func, *args, **kwargs):
	MPLogger.log_queue = log_queue
	logging.setLoggerClass(MPLogger)
	# monkey patch root logger and already defined loggers
	logging.root.__class__ = MPLogger
	for logger in logging.Logger.manager.loggerDict.values():
		if not isinstance(logger, logging.PlaceHolder):
			logger.__class__ = MPLogger
	try:
		func(*args, **kwargs)
	except Exception as e:
		logging.exception(e)
		raise


def open_queue():
	"""Use the context managed version open_safe_queue whenever possible."""
	log_queue = multiprocessing.Queue()
	daemon_thread = threading.Thread(name='log_queue', target=daemon, args=(log_queue,))
	daemon_thread.daemon = True
	daemon_thread.start()
	return log_queue


@contextlib.contextmanager
def open_safe_queue():
	"""Safer to use this since it will close the daemon if the context closes"""
	log_queue = open_queue()
	yield log_queue
	log_queue.put(None)
