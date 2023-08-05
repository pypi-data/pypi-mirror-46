import gzip
import re

from collections import defaultdict

class JinoLog:

	LOGFILE_EXTENSION = 'gz'
	EMAIL_REGEX = r"""(?:[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
	SENT = 'status=sent'
	EMPTY = '<>'
	SENDER = 'from='
	SENDER_EMPTY = SENDER + EMPTY

	def __new__(cls, log_file):
		log_file_ext = log_file.split('.')[1]
		if log_file_ext != cls.LOGFILE_EXTENSION:
			raise Exception('Log file must be gzipped')
		return super().__new__(cls)

	def __init__(self, log_file):
		self.log_file = log_file
		self.file = None
		self.raw_message_id_and_emails = defaultdict(list)
		self.emails_not_sended = defaultdict(int)
		self.emails_sended = defaultdict(list)
		self.emails_sened_total = 0

	def __enter__(self):
		lines = []
		self.file = gzip.open(self.log_file, 'r')
		for line in self.file.readlines():
			new_line = re.findall(r':\s\w+: .*\n', line.decode('UTF-8'), re.DOTALL)
			message_id = None
			try:
				message_id = re.findall(r'message-id=<', new_line[0], re.DOTALL)[0]
			except:
				pass
			if new_line and message_id is None:
				lines.append(new_line)
		self.log_lines = lines
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.file.close()

	def iterate_through_lines_and_classify_emails_by_sent_status(self):
		for line in self.log_lines:
			line_ = line[0].split(':')
			line_.remove(line_[0])
			other_data = ','.join(line_[1:])
			if other_data is not None:
				if self.has_number(line_[0]) and 'uid' not in other_data \
				and self.SENDER in other_data and self.SENDER in other_data \
				and self.SENDER_EMPTY not in other_data:
					try:
						self.raw_message_id_and_emails[line_[0]].append(
							{'to': re.search(
								self.EMAIL_REGEX, 
								self.from_email(other_data)
								).group(0)
							}
							)
					except:
						pass
				if self.has_number(line_[0]) and self.SENT in other_data \
				and self.SENDER not in other_data:
					try:
						self.raw_message_id_and_emails[line_[0]].append(
							{'from': re.search(
								self.EMAIL_REGEX, 
								self.to_email(other_data)
								).group(0)
							}
							)
					except:
						pass
		for k, v in self.raw_message_id_and_emails.items():
			if v.__len__() > 1:
				try:
					sended_emails = [m for m in v[::-1][1:]]
					self.emails_sended[v[::-1][0]['from']] = sended_emails
				except:
					pass
			else:
				self.emails_not_sended['not_sended'] += 1
		for k_, v_ in self.emails_sended.items():
			self.emails_sened_total += v_.__len__()
			print(k_, v_.__len__())
		print('Успешно отправлено писем: {}'.format(self.emails_sened_total))
		print('Писем не отправлено: {}'.format(self.emails_not_sended['not_sended']))


	@staticmethod
	def has_number(string):
		s = [s.isdigit() for s in string]
		if True in s:
			return True
		return False

	def from_email(self, data):
		return re.search('from=<' + self.EMAIL_REGEX + '>', data).group(0)

	def to_email(self, data):
		return re.search('to=<' + self.EMAIL_REGEX + '>', data).group(0)

with JinoLog('maillog.gz') as log:
	log.iterate_through_lines_and_classify_emails_by_sent_status()
