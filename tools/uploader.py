#! /usr/bin/python

# http://fabien.seisen.org/python/urllib2_multipart.html

__author__ = 'Savu Andrei <contact@andreisavu.ro>'

import os, sys
import urllib2_file
import urllib2
import simplejson
import socket

def parse_cli_params():
	if len(sys.argv) != 3:
		print 'Usage: ./uploader.py <api_endpoint> <folder_or_file>'
		sys.exit(0)
	# api_endpoint should be a valid url
	if not os.path.exists(sys.argv[2]):
		print 'File or dir not found.'
		sys.exit(2)
	return sys.argv[1], sys.argv[2]

def do_file_upload(url, file):
	data = { 'file': open(file) }
	try:
		r = simplejson.loads(urllib2.urlopen(url, data).read())
		return r
	except socket.error, e:
		return {'code': 1}

def folder_scanner(folder):
    if folder[0] == '.':
        folder = os.path.join( os.getcwd(), folder[2:] )
    for f in os.listdir(folder):
        if f[0] == '.':
            continue
        f = os.path.join(folder, f)
        if os.path.isdir(f):
            for x in folder_scanner(f):
                yield x
        if os.path.isfile(f):
            yield f

def check_result(r, f):
	if r['code'] != 0:
		print 'Error:', f
	else:
		print 'Ok:', f

def is_mp3(f):
	if f[-3:] == 'mp3':
		return True
	return False

def handle_file(f):
	if is_mp3(f):
		r = do_file_upload(url, f)
		check_result(r,f)
	else:
		print 'Ignore:', f

if __name__ == '__main__':
	url, src = parse_cli_params()
	if os.path.isfile(src):
		handle_file(src)
	else:
		for f in folder_scanner(src):
			handle_file(f)
