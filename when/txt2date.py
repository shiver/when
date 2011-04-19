from datetime import datetime, timedelta
from difflib import get_close_matches
import locale

try:
	import pytz
except ImportError:
	pass

class Txt2Date(object):
	def __init__(self):
		self._months = []
		self._days = []
		locale.setlocale(locale.LC_ALL, '')

	@property
	def months(self):
		if len(self._months) == 0:
			self._months.extend([locale.nl_langinfo(
				locale.__getattribute__('MON_' + str(i+1))).lower() \
					for i in xrange(12)])
		return self._months

	@property
	def days(self):
		if len(self._days) == 0:
			self._days.extend([locale.nl_langinfo(
				locale.__getattribute__('DAY_' + str(i+1))).lower() \
					for i in xrange(7)])
		return self._days

	def match_month(self, txt):
		# try simple match first
		for m in self.months:
			if m.startswith(txt.lower()):
				return m

		matches = get_close_matches(txt.lower(), self.months, 1, 0.7)

		if len(matches) == 0:
			raise ValueError('No matching month found in text: "{}"'.format(
				txt))

		return matches[0]

	def match_day(self, txt):
		# try simple match first
		for d in self.days:
			if d.startswith(txt.lower()):
				return d

		matches = get_close_matches(txt.lower(), self.days, 1, 0.7)

		if len(matches) == 0:
			raise ValueError('No matching day found in text: "{}"'.format(
				txt))
		return matches[0]
