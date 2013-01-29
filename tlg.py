import webapp2

from api import tlg_add

TLG_ADD = tlg_add.TLG_ADD()



class MainPage(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.write('Hello, webapp2 World!')
      
      
class APIHandler(webapp2.RequestHandler):
  def get(self):
      self.response.headers['Content-Type'] = 'text/plain'
      self.response.write('APIHandler')
      
  def post(self):
	self.operation = self.request.get('operation')
	self.input = self.request.get('request')
    
    #GET
    
    #EDIT
    
    #ADD
	if self.operation == 'add_tlgUser':
		self.response.out.write(TLG_ADD.addUser())
		return
	    
	#REMOVE
	
	
app = webapp2.WSGIApplication([
								('/', MainPage),
								('/api', APIHandler) 
								
								], debug=True)