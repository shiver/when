import pytz
import sys
import re
from pytz import datetime
from datetime import timedelta
import parsedatetime.parsedatetime as pdt

def until(dt_now, dt_then):
	diff = dt_now - dt_then
	ts = diff.total_seconds()

	m, s = divmod(ts, 60)
	h, m = divmod(m, 60)

	tense = None
	tense = 'past' if ts > 0 else tense
	tense = 'future' if ts < 0 else tense

	return int(abs(h)), int(abs(m)), int(abs(s)), tense

def current_tz():
	with open('/etc/timezone', 'r') as f:
		return pytz.timezone(f.read().strip())

def str_to_time(s):
	re.compile(r'\d{4}', re.IGNORECASE).match(s)

def compile_abbrev():
	_cache = {}
	now = datetime.datetime.now(pytz.utc)
	for t in pytz.all_timezones:
		tz = pytz.timezone(t)
		abbrev = now.astimezone(tz).tzname()

		if abbrev not in _cache:
			_cache[abbrev] = []

		_cache[abbrev].append(tz.zone)

if __name__ == '__main__':
	cal = pdt.Calendar()
	sys.stdout.write('{}\n'.format(cal.parse(sys.argv[1])))
	local = current_tz()
	now = datetime.datetime.now(local)
	other_tz = pytz.timezone('US/Pacific')
	now_utc = now.astimezone(pytz.utc) 

	then_parsed = datetime.datetime(*cal.parse(sys.argv[1])[0][:6])
	then = other_tz.localize(then_parsed)

	h, m, s, t = until(now_utc, then.astimezone(pytz.utc))

	sys.stdout.write('It is currently {} in {}.\n'.format(
		now.strftime('%d %b %H:%M:%S %Z'), local.zone))
	sys.stdout.write('It is currently {} in {}.\n'.format(
		now.astimezone(other_tz).strftime('%d %b %H:%M:%S %Z'), other_tz.zone))

	sys.stdout.write('Time until {}: '.format(
		then.strftime('%d %b %H:%M:%S %Z')))

	if h > 0:
		sys.stdout.write('{} hours '.format(h))
	sys.stdout.write('{} minutes {} seconds '.format(m, s))

	if t is not None:
		sys.stdout.write('in the {}'.format(t))

	sys.stdout.write('.\n')
	
	
