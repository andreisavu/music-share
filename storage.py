
import web

def db_save(info, db):
	return db.insert('ms_files', filename=info['FILENAME'])

def save(info, fp, db):
	id = db_save(info, db)
	dest = "static/upload/%d.mp3" % id
	f = open(dest, 'w')
	fp.seek(0)
	f.write(fp.read())
	f.close()
	return id

