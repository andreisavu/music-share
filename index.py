
import web, cgi, settings
import storage, search, db
import simplejson
from lib import is_mp3, get_mp3_info

urls = (
    '^/$', 'do_index',						
	'^/about[/]?$', 'do_about',			
	'^/search[/]?$', 'do_search',			
	'^/upload[/]?$', 'do_upload',
	'^/upload/error[/]?$', 'do_upload_error',		
	'^/api/about[/]?$', 'do_api_about',	
	'^/api/search(.*)$', 'do_api_search',
	'^/api/upload(.*)$', 'do_api_upload',	
	'^/media/(\d+)$', 'do_media',
	'^/view/(\d+)$', 'do_view'
)

app = web.application(urls, globals())

render = web.template.render(settings.TEMPLATE_FOLDER, base='base')

class do_index:        
    def GET(self):
		files = db.slave.select('ms_files', order='date desc', limit=5)
		return render.index(files)

class do_about:
	def GET(self):
		return render.about(title='About')

class do_search:
	def GET(self):
		input = web.input(q='')
		files = search.get(input.q, db.slave)
		return render.search(files, query=input.q, title='Search')

class do_upload_error:
	def GET(self):
		return render.upload_error(title='Upload error')

class do_upload:
	def GET(self):
		return render.upload(title='Upload')

	def POST(self):
		cgi.maxlen = settings.MAX_UP_FILE_SIZE

		input = web.input(file={})
		if input.file.file:
			if not is_mp3(input.file.file):
				raise web.seeother('/upload/error')
			try:
				info = get_mp3_info(input.file.file)
				info['FILENAME'] = input.file.filename
			except:
				raise web.seeother('/upload/error')
			id = storage.save(info, input.file.file, db.master)
			search.update(id, info)
		raise web.seeother('/')

class do_media:
	def GET(self, id):	
		path = "/%s" % storage.get_path(int(id))
		raise web.seeother(path)

class do_view:
	def GET(self, id):
		f = search.get_by_id(id, db.slave)
		if f.title and f.artist:
			title = "%s : %s" % (f.artist, f.title)
			related = search.get(f.artist, db.slave)
		else:
			title = f.filename
			import re
			q = re.sub('[^a-zA-Z ]+', ' ', f.filename[:-4])
			q = [t[:5] for t in q.split(' ') if t.strip()]
			if len(q) > 2:
				q = "%s %s" % (q[0], q[1])
			else:
				q = ' '.join(q)
			related = search.get(q, db.slave)

		related = [x for x in related if x.id != int(id)]
		return render.view(f, related, title)

class do_api_about:
	def GET(self):
		return render.api.about(title='Api Documentation')

class do_api_search:
	def GET(self, format):
		if not format:
			format = '.json'
		input = web.input(q='')
		res = search.get(input.q, db.slave)
		files = []
		for f in res:
			del(f['date'])
			files.append(f)
		return simplejson.dumps(files)

class do_api_upload:
	def POST(self, format):
		cgi.maxlen = settings.MAX_UP_FILE_SIZE
		if not format:
			format = '.json'

		input = web.input(file={})
		if input.file.file:
			if not is_mp3(input.file.file):
				return simplejson.dumps({'code':1, 'error':'Check file format and try again'})
			try:
				info = get_mp3_info(input.file.file)
				info['FILENAME'] = input.file.filename
			except:
				return simplejson.dumps({'code':2, 'error':'Error getting file information'})
			id = storage.save(info, input.file.file, db.master)
			search.update(id, info)
		return simplejson.dumps({'code':0})

def notfound():
	return web.notfound(render.notfound(render))
app.notfound = notfound


def internalerror():
	return web.internalerror(render.internalerror(render))
app.internalerror = internalerror
	
if __name__ == "__main__":
    app.run()

