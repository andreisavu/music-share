
import web, re, os

def db_save(info, db):
	""" Save data in database """
	return db.insert('ms_files', filename=info['FILENAME'], 
		album=info['ALBUM'], artist=info['ARTIST'], 
		title=info['TITLE'], year=info['YEAR'])

def clean(v):
	""" Remove any not visible chars """
	return re.sub('[^\w.\'" ]+', '', v)

def add_missing_fields(info):
	""" Add to the info structure the missing fields """
	if not 'ALBUM' in info:
		info['ALBUM'] = ''
	if not 'ARTIST' in info:
		info['ARTIST'] = ''
	if not 'TITLE' in info:
		info['TITLE'] = ''
	if not 'YEAR' in info:
		info['YEAR'] = 0

	info['ALBUM'] = clean(info['ALBUM'])
	info['ARTIST'] = clean(info['ARTIST'])
	info['TITLE'] = clean(info['TITLE'])

	return info

def save_file(id, fp):
	folder = get_folder(id)
	if not os.path.exists(folder):
		os.makedirs(folder)

	dest = "%s/%d.mp3" % (folder, id)
	f = open(dest, 'w')
	fp.seek(0)
	f.write(fp.read())
	f.close()

def get_folder(id):
	return "static/upload/%d/%d" % ((id / 10) % 10, id % 10)

def get_path(id):
	return "%s/%d.mp3" % (get_folder(id), id)

def save(info, fp, db):
	""" Save track info in database """
	info = add_missing_fields(info)
	id = db_save(info, db)
	save_file(id, fp)
	return id

