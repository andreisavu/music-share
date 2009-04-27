
import web, cgi, settings
import api, storage, search 
import lib.mp3 as mp3

urls = (
    '^/$', 'do_index',						
	'^/about[/]?$', 'do_about',			
	'^/search[/]?$', 'do_search',			
	'^/upload[/]?$', 'do_upload',
	'^/upload/error[/]?', 'do_upload_error',		
	'^/api/about[/]?$', 'api.do_about',	
	'^/api/search(.*)$', 'api.do_search',	
	'^/media/(\d+)$', 'do_media'	
)

app = web.application(urls, globals())

db = web.database(dbn = settings.DB_TYPE,
	host = settings.DB_HOST,
	db = settings.DB_NAME,
	user = settings.DB_USER,
	pw = settings.DB_PASSW)

api.render = render = web.template.render(settings.TEMPLATE_FOLDER, base='base')

class do_index:        
    def GET(self):
		files = db.select('ms_files', order='date desc', limit=5)
		return render.index(files)

class do_about:
	def GET(self):
		return render.about(title='About')

class do_search:
	def GET(self):
		input = web.input(q=None)
		q = input.q
		files = []
		if q:
			pq = [t.strip() for t in q.split(' ') if len(t.strip())!=0]
			pq = '%' + '%'.join(pq) + '%'
			files = db.query('select * from ms_files where filename like $q', vars={'q':pq})
		else:
			q = ''
		return render.search(files, query=q, title='Search')

class do_upload_error:
	def GET(self):
		return render.upload_error(title='Upload error')

class do_upload:
	def GET(self):
		return render.upload(title='Upload')

	def get_mp3_info(self, file):
		file.seek(0)
		info = mp3.mp3info(fp=file)
		file.seek(0)
		info.update(mp3.get_mp3tag(fp=file))
		return info

	def POST(self):
		cgi.maxlen = settings.MAX_UP_FILE_SIZE

		input = web.input(file={})
		if input.file.file:
			try:
				info = self.get_mp3_info(input.file.file)
				info['FILENAME'] = input.file.filename
			except:
				raise web.seeother('/upload/error')

			id = storage.save(info, input.file.file, db)
			search.update(id, info)

		raise web.seeother('/')

class do_media:
	def GET(self, id):	
		path = "/static/upload/%d.mp3" % int(id)
		raise web.seeother(path)


def notfound():
	return web.notfound(render.notfound(render))
app.notfound = notfound


def internalerror():
	return web.internalerror(render.internalerror(render))
app.internalerror = internalerror
	
if __name__ == "__main__":
    app.run()

