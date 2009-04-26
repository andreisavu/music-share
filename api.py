
class do_about:
	def GET(self):
		return render.api.about(title='Api Documentation')

class do_search:
	def GET(self, format):
		if not format:
			format = '.json'
		query = ''
			
		return 'search api' + format + ' q=' + query 


