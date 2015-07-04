import cgi
import os
import urllib


from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(autoescape=True, loader = jinja2.FileSystemLoader(template_dir))

default_guestbook_name = 'default_guestbook'

error =""

def guestbook_key(guestbook_name=default_guestbook_name):
    
    return ndb.Key('Guestbook', guestbook_name)

class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)    

class Greeting(ndb.Model):
    
    title = ndb.StringProperty(indexed = False)
    content = ndb.StringProperty(indexed = False)
    date = ndb.DateTimeProperty(auto_now_add = True)    


class Link(ndb.Model):
    
    name = ndb.StringProperty(indexed=False)
    linkurl = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
                
        lessons=["Stage 5 Notes"]
            
        subheadings=["JavaScript"]
        subheadings1=["APIs"]
        subheadings2=["Responsive Web Design"]
        subheadings3=["Relational Database"]
        
        subheadings_list=["JavaScript is the most popular programming language in the world. It can change HTML content, change HTML Attributes, and it can change HTML style (CSS). JavaScript and Java are completely different languages, both in concept and design. JavaScript is commonly used to create interactive effects within web browsers. JavaScipt runs natively in the browser, it allows us to run an inspector code very easily. JavaScript gives us a way of saving data in the form of variables. Console.log will print any information it receives to the browser console, which is a useful trick for debugging code. Arrays in JavaScript are just like lists, which are lists of values. Start with the syntax of VAR and then the name of the array, followed by and equals sign. The Arrays are define by the square brackets with items inside seperated by commas. JavaScript gives us a way of accessing properties about arrays. There are no classes in JavaScript there are only objects. Objects are defined with in the curly braces. A useful tool for making sure your data is formatted properly which relies on object literal notation, is JSON, JavaScript Object Notation."]    
        subheadings1_list=["API stands for Application Programing Interface. APIs allow our web sites to communicate not just with browsers but with other computers as well. When interacting with browsers we use HTML, however if we want to send or receive data from servers we use formats like XML or JSON, which are similar to HTML but designed to be read by computers. If we don't have the information, our website can still send HTTP request to a number other servers out there and fetch the information our user needs by getting response containing XML or JSON and then sending it back to our user. This is done by, importing the urllib and urllib2 libraries. Then we open a url connection to the server of our choice using the urllib2 function urlopen() and we give the address as a parameter (for example: urllib2.urlopen(http://www.example.com)). Once we are connected to server of our choice we send a request with the information we need. The third party server returns a XML or JSON document to our request. In order to use the information we have to parse this document and get the data we need. Parsing XML: First we have to import another library: from xml.dom import minidom. After we import the library we can parse the the XML we already have by calling the function minidom.parseString(our XML file as parameter). Once we parse our XML document then we can access different elements within, by using the minidom function getElementsByTagName(the tag element we want to access). XMLs have tree like structure and by calling getElementsByTagName we can see child elements of the element of our choice. To see what's inside the child elements we call XML.getElementsByName(first element)[child element index](note: indexes of child elements start from 0 just like in lists). Calling the last function will return the child elements of the child element and so on until we reach a child element storing some value. We can retrieve this one by calling XML.getElementsByName(element_name)[n].childNodes[n].nodeValue (note:XML is our XML document and n being the index of the child element). Parsing JSON: JSON serves the same purpose as XML. It's a nice kind of computer and human readable way to exchange data in a consistent format. JSON is JavaScript Object Notation. The content of a JSON document is very similar to a dictionary with keys. To parse a JSON we have to import json library. Then we run the function json.loads(name_of_our_json_document). When we run this, Python returns a dictionary. If we store that to a variable we can then manipulate this variable as a dictionary. After we have this data as a dictionary we can browse by getting key value or getting list of keys within keys using the .keys() method. APIs allow web developers to build their websites on top of already existing sites."]  
        subheadings2_list=["Responsive Web Design, which just means making web pages that look good on any device. By designing a site to be responsive, it will look good and work well no matter what device your users have in front of them. There is NO RIGHT solution to Responsive Web Design. This is concidered an art not science. There is a link to wikipedia for further definition of Responsive Web Design in the Extra Links Tab. There is also a link to the Udacity Course as well called Responsive Web Design Fundamentals."]
        subheadings3_list=["A Relational Database is a digital database whose organization is based on the relational model of data. There is a link in the Extra Links Tab to Wikipedia for further definition. There is also an link to Udacity for a course on Relational Databases."]
       
        
        items = self.request.get_all("word")
        self.render("div-list.html", items = items, lessons=lessons, subheadings=subheadings,subheadings1=subheadings1, subheadings2=subheadings2, subheadings3=subheadings3,  subheadings_list=subheadings_list, subheadings1_list=subheadings1_list, subheadings2_list=subheadings2_list, subheadings3_list=subheadings3_list)
        
class codepenHandler(webapp2.RequestHandler):
    def get(self):
        template_values={
            'title': 'Notes To Intro Programming',
                }

        template=jinja_env.get_template('codepen.html',)

        self.response.out.write(template.render(template_values))

        

class indexHandler(webapp2.RequestHandler):
    def get(self):
        template_values={
            'title': 'Notes To Intro Programming',
                }
        template=jinja_env.get_template('index.html',)

        self.response.out.write(template.render(template_values))        

class guestbookHandler(Handler):
    def get(self):
        guestbook_name = self.request.get('guestbook_name',
                                          default_guestbook_name)

        
        notes_query = Greeting.query(
            ancestor = guestbook_key(guestbook_name)).order(-Greeting.date)
        notes = notes_query.fetch(2)

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user' : user ,
            'notes' : notes ,
            'url' : url ,
            'url_linktext' : url_linktext ,
            'error' : error             
        }

        template = jinja_env.get_template('guestbook.html')
        self.response.write(template.render(template_values))

class Validation(webapp2.RequestHandler):
    def post(self):
        guestbook_name = self.request.get('guestbook_name',
                                         default_guestbook_name)
        note = Greeting(parent = guestbook_key(default_guestbook_name))

        
        if not (self.request.get('content') and self.request.get('title')):
            global error
            error = " You forgot to enter a  Name and Message!!!"
        else:
            global error
            error = ""
            note.content = self.request.get('content')
            note.title = self.request.get('title')
            note.put()

        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/guestbook.html?' + urllib.urlencode(query_params))

app=webapp2.WSGIApplication([('/', MainPage),
    ('/codepen.html', codepenHandler),
    ('/guestbook.html', guestbookHandler),
    ('/index.html', indexHandler),
    ('/notes', Validation),
    
    ], 
    debug=True)
