# the import section
import webapp2
import jinja2
import os
from webapp2_extras import sessions
from models import User

# this initializes the jinja2 environment
# this will be the same in every app that uses the jinja2 templating library 
the_jinja_env = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)
# the import section 


# other functions should go above the handlers or in a separate file
def getCurrentUser(self):
  #will return None if user does not exist
  return self.session.get('user')

def login(self, id):
  self.session['user'] = id

def logout(self):
  self.session['user'] = None

def isLoggedIn(self):
  if self.session['user'] is not None:
    return True
  else:
    return False

# the handler section
class BaseHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)
    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class MainHandler(webapp2.RequestHandler):
  def get(self):  # for a get request
    welcome_template = the_jinja_env.get_template('templates/project.html')
    self.response.write(welcome_template.render())

class SignupHandler(BaseHandler):
  def get(self):  # for a get request
    welcome_template = the_jinja_env.get_template('templates/signup.html')
    self.response.write(welcome_template.render())

  def post(self):
    signup_template = the_jinja_env.get_template('templates/signup.html')
    name = self.request.get('name')
    email = self.request.get('email')
    #password = self.request.get('password')#

    user = User(name = name, email = email)
    user_id = user.put()
    login(self, name)
    variable_dict = {"name":name}
    self.response.write(signup_template.render(variable_dict))

class AccountHandler(BaseHandler):
  def get(self):  # for a get request
    acct_template = the_jinja_env.get_template('templates/account.html')
    user = getCurrentUser(self)
    if user is not None:
      user_info = User.query().filter(User.name == getCurrentUser(self)).fetch()
      variable_dict = {"name": user_info[0].name, "email": user_info[0].email}
      self.response.write(acct_template.render(variable_dict))
    else:
      #send user back to home/login if they're not signed in
      self.redirect('/')

class LogoutHandler(BaseHandler):
  def get(self):  # for a get request
    logout_template = the_jinja_env.get_template('templates/logout.html')
    user = getCurrentUser(self)
    if user is not None:
      logout(self)
      self.response.write(logout_template.render())
    else:
      self.redirect('/')

config = {}
config['webapp2_extras.sessions'] = {
   # 'secret_key': 'your-super-secret-key',
}

# the app configuration section 
# the handler section
  # the response

# the app configuration section	
app = webapp2.WSGIApplication([
  #('/', MainPage),
  ('/', MainHandler),
  ('/signup', SignupHandler),
  ('/account', AccountHandler),
  ('/logout', LogoutHandler,)
  ], debug=True)
