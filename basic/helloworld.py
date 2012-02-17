import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template


class Thingy(db.Model):
  name = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)
  widget = db.StringProperty()


class MainPage(webapp.RequestHandler):
  def get(self):
    thingy_query = Thingy.all().order('-date')
    thingies = thingy_query.fetch(10)

    template_values = {
      'thingies': thingies,
    }

    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    self.response.out.write(template.render(path, template_values))

class AddThingyPage(webapp.RequestHandler):
  def post(self):
    thingy_name = self.request.get('thingyname')
    c = Thingy()
    c.name = thingy_name
    c.put()
    self.redirect('/')

class AddWidgetPage(webapp.RequestHandler):
  def post(self):
    thingy_name = self.request.get('thingyname')
    widget_name = self.request.get('widgetname')
    thingy_query = Thingy.all().filter('name =', thingy_name)
    c = thingy_query.fetch(1)[0]

    if c:
      c.widget = widget_name
      c.put()
    self.redirect('/')

class DestroyThingyPage(webapp.RequestHandler):
  def post(self):
    thingy_name = self.request.get('thingyname')

    thingy_query = Thingy.all()
    thingy_query.filter("name =", thingy_name)
    thingy_query.order('-date')

    thingies = thingy_query.fetch(1)
    db.delete(thingies)
    self.redirect('/')


application = webapp.WSGIApplication(
  [('/', MainPage),
    ('/addthingy', AddThingyPage),
    ('/addwidget', AddWidgetPage),
   ('/destroythingy', DestroyThingyPage)],
  debug=True)


def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()