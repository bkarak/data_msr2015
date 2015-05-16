#!/usr/bin/python

import os


MAVEN_REPO='maven/'

def delete_file(filename):
	print 'Deleting %s' % (filename,)
	os.remove(filename)

def main():
	md5_count = 0
	sha1_count = 0
	file_count = 0
	asc_count = 0

	for (root, dirs, names) in os.walk(MAVEN_REPO):
		for n in names:
			full_name = os.path.join(root, n)

			if full_name.endswith('.md5'):
				md5_count += 1
				delete_file(full_name)
			elif full_name.endswith('.sha1'):
				sha1_count += 1
				delete_file(full_name)
			elif full_name.endswith('.asc'):
				asc_count += 1
				delete_file(full_name)

			file_count += 1

	print '%d files, %d md5 files, %d sha1 files. %d asc files' % (file_count, md5_count, sha1_count, asc_count)


if __name__ == '__main__':
	main()