import os
import re
import requests
import time

infection_pattern = re.compile(r'^Sign of "(.+?)" has been found in "(.+?)" file.$')
pending_payloads = []

def send_infection_data(payload):
	print 'Reporting ', payload['infection'], ' from ', payload['filename']

	r = requests.post('http://192.168.56.101/vmhost/report_infection', payload)
	if r.status_code is 200:
		return True

	return False


def process_infection_queue():
	global pending_payloads # oh no

	unprocessed_payloads = []
	for payload in pending_payloads:
		if not send_infection_data(payload):
			unprocessed_payloads.append(payload)

	pending_payloads = unprocessed_payloads


def add_infection_to_queue(payload):
	pending_payloads.append(payload)


def process_infected_line(line):
	cols = line.split("\t")
	timestamp = cols[2]
	message = cols[5]

	infection_data = list(infection_pattern.findall(message)[0])
	infection = infection_data[0]
	filename = infection_data[1]

	payload = {'timestamp': timestamp, 'infection': infection, 'filename': filename}
	add_infection_to_queue(payload)


def process_file_line(line):
	line = line.strip()
	sign_index = line.find('Sign of "')
	if sign_index is not -1:
		process_infected_line(line)


def process_file_lines(content):
	for line in content:
		process_file_line(line)


def process_file(filename):
	with open(filename) as f:
		content = f.readlines()
		process_file_lines(content)

	os.remove(filename)


def poll_changes(filename):
	if os.path.isfile(filename):
		process_file(filename)


def main():
	while True:
		logfile = '/Program Files/Alwil Software/Avast4/DATA/log/Warning.log'
		poll_changes(logfile)
		process_infection_queue()

		time.sleep(1)


if __name__ == '__main__':
	main()
