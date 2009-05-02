
import web

def update(id, info):
	pass

def get(q, db):
	if not q:
		return []
	pq = [t.strip() for t in q.split(' ') if len(t.strip())!=0]
	pq = '%' + '%'.join(pq) + '%'
	files = db.query('select * from ms_files where filename like $q', vars={'q':pq})
	return files

