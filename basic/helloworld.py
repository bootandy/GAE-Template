import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import os
#os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

#from google.appengine.dist import use_library
#use_library('django', '1.2')


class BlogPost(db.Model):
  title = db.StringProperty(multiline=True)
  body = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)

class MainPage(webapp.RequestHandler):
  def get(self):
    blog_post_query = BlogPost.all().order('-date')
    posts = blog_post_query.fetch(10)

    template_values = {
      'posts': posts,
    }

    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
    self.response.out.write(template.render(path, template_values))

class AddPostPage(webapp.RequestHandler):
  def post(self):
    title = self.request.get('title')
    body = self.request.get('body')
    post = BlogPost()
    post.title = title
    post.body = body
    post.put()
    self.redirect('/')


class DestroyPostPage(webapp.RequestHandler):
  def post(self):
    post_key = self.request.get('post_key')
    db.delete(post_key)
    self.redirect('/')

class StartEditPage(webapp.RequestHandler):
  def post(self):
    post_key = self.request.get('post_key')
    post = db.get(post_key)

    template_values = {
      'title':post.title,
      'body':post.body,
      'key':post_key,
    }
    path = os.path.join(os.path.dirname(__file__), 'templates/edit.html')
    self.response.out.write(template.render(path, template_values))

class FinishEditPage(webapp.RequestHandler):
  def post(self):
    title = self.request.get('title')
    body = self.request.get('body')
    post_key = self.request.get('key')
    post = db.get(post_key)
    post.title = title
    post.body = body
    post.put()
    self.redirect('/')


application = webapp.WSGIApplication(
  [('/', MainPage),
    ('/add', AddPostPage),
    ('/start_edit', StartEditPage),
    ('/finish_edit', FinishEditPage),
    ('/destroy', DestroyPostPage)],
  debug=True)


def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()