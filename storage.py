
import web

def db_save(info, db):
	return db.insert('ms_files', filename=info['FILENAME'], 
		album=info['ALBUM'], artist=info['ARTIST'], 
		title=info['TITLE'], year=info['YEAR'])

def add_missing_fields(info):
	if not 'ALBUM' in info:
		info['ALBUM'] = ''
	if not 'ARTIST' in info:
		info['ARTIST'] = ''
	if not 'TITLE' in info:
		info['TITLE'] = ''
	if not 'YEAR' in info:
		info['YEAR'] = 0
	return info

def save(info, fp, db):
	info = add_missing_fields(info)
	id = db_save(info, db)
	dest = "static/upload/%d.mp3" % id
	f = open(dest, 'w')
	fp.seek(0)
	f.write(fp.read())
	f.close()
	return id

