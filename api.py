
class do_about:
	def GET(self):
		return render.api.about(render)

class do_search:
	def GET(self, format):
		if not format:
			format = '.json'
		query = None
		try:
			query = web.input('q').q
		except Exception,e:
			pass
			
		return 'search api' + format + ' q=' + query 


