import logging
import logging.config
import re
import traceback


def log_exception(e, logger=None, prefix='', critical=False):
	"""sends full traceback to ERROR"""
	if not logger:
		logger = logging.getLogger('{}'.format(__name__))
	log_method = logger.critical if critical else logger.error
	log_method('{}: {}'.format(prefix, verbose_exception(e)).lstrip(': '))


def verbose_exception(e):
	return '{}: {}\n\n{}'.format(e.__class__.__name__,
								 str(e).replace('\n', ' / '), get_traceback(e))


def get_traceback(exception=None):
	if exception is not None and hasattr(exception, 'traceback'):
		return exception.traceback
	tb = traceback.format_exc()
	if tb == 'NoneType: None\n':
		tb = 'Traceback for exception not available (multiprocessing?).'
	return tb


def log_exceptions(reraise=True, exit_patterns=None, critical=False):
	"""Decorator factory."""
	if exit_patterns is not None:
		raise_regex = re.compile('|'.join(['({})'.format(i) for i in exit_patterns]))
	def decorator(f):
		"""Actual decorator. Log exceptions raised by decorated function."""
		def new_f(*args, **kwargs):
			"""New version of function that is logged."""
			try:
				return f(*args, **kwargs)
			except Exception as e:
				logger = logging.getLogger('{}.{}'.format(f.__module__, f.__name__))
				log_exception(e, logger, critical=critical)
				if reraise or (exit_patterns is not None and raise_regex.match(repr(e).lower())):
					raise
				return e
		new_f.__name__ = f.__name__
		return new_f
	return decorator


class Loggable(object):
	"""Inherit by any class that needs to be logged."""
	__logger = None

	@property
	def logger(self):
		if self.__logger is None:
			self.__logger = self.get_logger()
		return self.__logger
	
	@classmethod
	def get_logger(cls, method=''):
		return logging.getLogger('.'.join([cls.__name__, method]).rstrip('.'))

	def log_exception(self, e, logger=None, prefix='', critical=False):
		logger = self.logger if logger is None else logger
		log_exception(e, logger, prefix, critical)


try:
	from colorlog import ColoredFormatter

	class BetterColoredFormatter(ColoredFormatter):
		"""A ColoredFormatter with better defaults.
		Mainly for use in logging.ini files
		"""
		def __init__(self, *args, **kwargs):
			ColoredFormatter.__init__(self, *args, log_colors={
				'DEBUG': 'cyan',
				'INFO': 'white',
				'WARNING': 'yellow',
				'ERROR': 'red',
				'CRITICAL': 'yellow,bg_red',
			}, **kwargs)
except ImportError:
	BetterColoredFormatter = None
