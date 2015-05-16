#!/usr/bin/python

import os, urllib, re


def fetch_url(filename):
	url = 'http://mirrors.ibiblio.org/%s' % (filename.replace('maven/','maven2/'),)
	print 'Fetching ... %s' % (url,)

	__dir = os.path.dirname(filename)

	if not os.path.exists(__dir):
		print 'Creating ... %s' % (__dir,)
		os.makedirs(__dir)

	urllib.urlretrieve(url, filename)
	print 'Downloading to ... %s' % (filename,)


def get_file_directory(filename):
	idx = filename.find('maven/')
	return filename.strip()[idx:]


def same_file_size(filename):
	size_match = re.search('[ ]+([0-9]+) [A-Z]', filename)
	file_size = os.path.getsize(get_file_directory(filename))

	if size_match:
		parsed_size = int(size_match.group(1))

		if file_size == parsed_size:
			return True
		else:
			print '%s: %d != %d' % (get_file_directory(filename), file_size, parsed_size)
			return False
	
	print 'ERROR: Could not get size of %s' % (filename,)
	
	return False


def main():
	file_count = 0
	dir_count = 0
	download_count = 0

	fp = open('maven.list.text','r')

	for f in fp:		
		pf = get_file_directory(f.strip())

		if pf.endswith('/'):
			print '[%d]: Entering ... %s' % (file_count, pf)
			dir_count += 1
			continue

		file_count += 1

		if not os.path.exists(pf):
			fetch_url(pf)
			download_count += 1

		if not same_file_size(f.strip()):
			print 'WARNING: Possibly corrupted %s' % (pf,)

	fp.close()

	print '%d files found, %d directories, %d downloads' % (file_count, dir_count, download_count)


if __name__ == '__main__':
	main()