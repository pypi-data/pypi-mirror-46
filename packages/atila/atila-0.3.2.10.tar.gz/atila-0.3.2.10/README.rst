==============================
Atila Framework
==============================


Atila
===========

*Atila* is simple and minimal framework integrated with `Skitai App Engine`_. It is the easiest way to make backend API services.

.. code:: python

  @app.route ("/<int:uid>/photos", methods = ["GET", "DELETE", "POST", "OPTIONS"])
  @app.permission_required ()
  def photos (was, uid, **DATA):
    uid = uid == "me" and was.request.JWT ["uid"] or uid

    with was.db ("@mydb") as db:
      if was.request.method == "GET":            
        rows = db.select ("photo").filter (uid = uid).execute ().fetch ()
        return was.API (rows = rows) # [ {id: 1, ...}, ... ]

      elif was.request.method == "DELETE":
        db.delete ("photo").filter (uid = uid).execute ().commit ()
        return was.API ("205 No Content")

      elif was.request.method == "POST":
        if not DATA.get ("title"):
          raise was.Error ("400 Bad Request", "title required")
        DATA ["uid"] = uid
        row = db.insert ("photo").data (**DATA).returning ("id").execute ().one ()
        return was.API ("201 Created", id = row.id)

.. contents:: Table of Contents
 
.. _`Skitai App Engine`: https://pypi.org/project/skitai/
 

Installation
=========================

**Requirements**

Python 3.5+  
  
**Installation**

With pip

.. code-block:: bash

    pip3 install -U atila skitai rs4 aquests sqlphile

From git

.. code-block:: bash

    git clone https://gitlab.com/hansroh/atila.git
    cd atila
    python3 setup.py install


Basic Directory Structure
==========================

Before you begin, recommended Atila App's directory structure is like this:

- service.py: Skitai runner
- app.py: File, Main app
- static: Directory, Place static files like css, js, images. This directory should be mounted for using
- services: Directory, Module components, utils or helpers for helping app like config.py, model.py etc...
- templates: Directory, Jinaja and Chameleon template files
- resources: Directory, Various files as app need like sqlite db file. In you app, you use these files, you can access file in resources by app.get_resource ("db", "sqlite3.db") like os.path.join manner.


Request Hanlding with Atila
====================================


Before You Read
-------------------------

For using atila, 'import atila' SHOULD be imported before calling skitai.run (). Because Atila silently patches some Skitai's objects for itself.

*Note:* But atila just adds some functions related 'was' and 'response' objects, NOT alter exist Skitai functions, then you could mount any WSGI apps with Atila app safely.  

If your script contains both atila app creation and skitai.run, you don't need to care about.

Below works fine.

.. code:: python
  
  from atila import Atila  
  app = Atila(__name__)
  
  ...
  
  @app.route ("/")
  def index (was):
    ...
    return was.response ("200 OK", ...)
  
  if __name__ == "__main__":
    import skitai    
  
    pref = skitai.pref ()
    pref.use_reloader = True
      
    skitai.mount ('/', './static')
    skitai.mount ('/', app, 'app', pref)
    skitai.run ()  

But atila app exists seprated file and just mount it, you should care about that. 

.. code:: python
  
  # serve.py
 
  if __name__ == "__main__":
    import skitai  
    import atila  
  
    pref = skitai.pref ()
    pref.use_reloader = True
      
    skitai.mount ('/', './static')
    skitai.mount ('/', 'myapp/atila_app.py', pref = pref)
    skitai.run ()  


App Resource Structure
-------------------------------------

If your app is simple, it can be made into single app.py and templates and static directory.

.. code:: python
  
  from atila import Atila
  
  app = Atila(__name__)
  
  app.use_reloader = True
  app.debug = True
  
  @app.route ("/")
  def index (was):
    ...
    return was.response ("200 OK", ...)
  
  if __name__ == "__main__":
    import skitai    
  
    pref = skitai.pref ()
    pref.use_reloader = True
      
    skitai.mount ('/', './static')
    skitai.mount ('/', app, 'app', pref)
    skitai.run ()  

And run,

.. code:: bash

  python3 app.py

But Your app is more bigger, it will be hard to make with single app file. Then, you can make services directory to seperate your app into several categories.

.. code:: bash
  
  app.py
  services/
  templates/
  resources/
  static/

All sub modules app need, can be placed into services/. services/\*.py will be watched for reloading if use_reloader = True.

You can structuring any ways you like and I like this style:

.. code:: bash

  services/views.py
  services/apis.py
  services/helpers.py

All modules to mount to app in services, should have def __mount__ (app).

For example, views.py is like this,

.. code:: python
  
  from . import helpers
  
  def __mount__ (app):  
    @app.route ("/")
    def index (was):
      ...
      return was.render ("index.html")

Now you just import app decorable moduels at your app.py,

.. code:: python

  from atila import Atila
  from services import views, apis
  
  app = Atila(__name__)

That's it.

If app scale is more bigger scale, services can be expanded to sub modules. 

.. code:: bash

  services/views/index.py, regist.py, search.py, ...
  services/apis/codemap.py, 
  services/helpers/utils.py, ...

And import these from app.py,

.. code:: python

  from services.views import index, regist, ...
  from services.apis import codemap, ...

Some more other informations will be mentioned at *Mounting Resources* section again.


Runtime App Preference
-------------------------

**New in skitai version 0.26**

Usally, your app preference setting is like this:

.. code:: python
  
  from atila import Atila
  
  app = Atila(__name__)
  
  app.use_reloader = True
  app.debug = True
  app.config ["prefA"] = 1
  app.config ["prefB"] = 2
  
Skitai provide runtime preference setting.

.. code:: python
  
  import skitai
  
  pref = skitai.pref ()
  pref.use_reloader = 1
  pref.debug = 1
  
  pref.config ["prefA"] = 1
  pref.config.prefB = 2
  
  skitai.mount ("/v1", "app_v1/app.py", "app", pref)
  skitai.run ()
  
Above pref's all properties will be overriden on your app.

Runtime preference can be used with skitai initializing or complicated initializing process for your app.

You can create __init__.py at same directory with app.py. And bootstrap () function is needed.

__init__.py

.. code:: python
  
  import skitai
  from . import cronjob
  
  def bootstrap (pref):
    with open (pref.config.urlfile, "r") as f:
      pref.config.urllist = [] 
      while 1:
        line = f.readline ().strip ()
        if not line: break
        pref.config.urllist.append (line.split ("  ", 4))


Access Atila App
------------------

You can access all Atila object from was.app.

- was.app.debug
- was.app.use_reloader
- was.app.config # use for custom configuration like was.app.config.my_setting = 1

- was.app.securekey
- was.app.session_timeout = None  

- was.app.authorization = "digest"
- was.app.authenticate = False
- was.app.realm = None
- was.app.users = {}
- was.app.jinja_env

- was.app.build_url () is equal to was.ab ()

Currently was.app.config has these properties and you can reconfig by setting new value:

- was.app.config.max_post_body_size = 5 * 1024 * 1024
- was.app.config.max_cache_size = 5 * 1024 * 1024
- was.app.config.max_multipart_body_size = 20 * 1024 * 1024
- was.app.config.max_upload_file_size = 20000000


Debugging and Reloading App
-----------------------------

If debug is True, all errors even server errors is shown on both web browser and console window, otherhwise shown only on console.

If use_reloader is True, Atila will detect file changes and reload app automatically, otherwise app will never be reloaded.

.. code:: python

  from atila import Atila
  
  app = Atila (__name__)
  app.debug = True # output exception information
  app.use_reloader = True # auto realod on file changed


Kill Switch
````````````````

You you want to disable debug and use_reloader on production enveironment at once, 

.. code:: bash

  python3 app.py -d
  python3 app.py -d ---production # triple hyphens


Routing
----------

Basic routing is like this:

.. code:: python
  
  @app.route ("/hello")
  def hello_world (was):  
    return was.render ("hello.htm")

For adding some restrictions:

.. code:: python
  
  @app.route ("/hello", methods = ["GET"], content_types = ["text/xml"])
  def hello_world (was):  
    return was.render ("hello.htm")

And you can specifyt multiple routing,

.. code:: python
  
  @app.route ("/hello", mehotd = ["POST"])
  @app.route ("/")
  def hello_world (was):  
    return was.render ("hello.htm")

If method is not GET, Atila will response http error code 405 (Method Not Allowed), and content-type is not text/xml, 415 (Unsupported Content Type).

And here's a notalble routing rule.

.. code:: python
  
  @app.route ("")
  def hello_world (was):  
    return was.render ("hello.htm")

This app is mounted to "/sub" on skitai, /sub URL is valid but "/sub/" will return 404 code.

On the other hand,

.. code:: python
  
  @app.route ("/")
  def hello_world (was):  
    return was.render ("hello.htm")

"/sub" will return 301 code for "/sub/" and "/sub/" is valid URL.


Request
---------

Reqeust object provides these methods and attributes:

- was.request.method # upper case GET, POST, ...
- was.request.command # lower case get, post, ...
- was.request.uri
- was.request.version # HTTP Version, 1.0, 1.1
- was.request.scheme # http or https
- was.request.headers # case insensitive dictioanry
- was.request.body # bytes object
- was.request.args # dictionary merged with url, query string, form data and JSON
- was.request.routed_function
- was.request.routable # {'methods': ["POST", "OPTIONS"], 'content_types': ["text/xml"]}
- was.request.split_uri () # (script, param, querystring, fragment)
- was.request.json () # decode request body from JSON
- was.request.form () # decode request body to dict if content-type is form data
- was.request.dict () # decode request body as dict if content-type is compatible with dict - form data or JSON
- was.request.get_header ("content-type") # case insensitive
- was.request.get_headers () # retrun header all list
- was.request.get_body ()
- was.request.get_scheme () # http or https
- was.request.get_remote_addr ()
- was.request.get_user_agent ()
- was.request.get_content_type ()
- was.request.get_main_type ()
- was.request.get_sub_type ()

Getting Parameters
---------------------

Atila parameters are comceptually seperated 3 groups: URL, query string and body.

Below explaination may be a bit complicated but it is enough to remember 3 things:

1. Atila resource parameters can be defined as function arguments and use theses native Python function arguments.

2. Also you can access parameter groups by origin:

  - was.request.DEFAULT: default arguments of your resource
  - was.request.URL: url query string
  - was.request.FORM
  - was.request.JSON
  - was.request.DATA: automatically choosen one of was.request.FORM or was.request.JSON by content-type header of request
  - was.request.ARGS: eventaully was.request.ARGS contains all parameters of all origins including was.request.DEFAULT

Getting URL Parameters
`````````````````````````

URL Parameters should be arguments of resource.

.. code:: python

  @app.route ("/episode/<int:id>")
  def episode (was, id):
    return id
  # http://127.0.0.1:5000/episode

for fancy url building, available param types are:

- int: integers and INCLUDING 'me', 'notme' and 'new'
- path: /download/<int:major_ver>/<path>, should be positioned at last like /download/1/version/1.1/win32
- If not provided, assume as string. and all space will be replaced to "_"

At your template engine, you can access through was.request.PARAMS ["id"].

It is also possible via keywords args,

.. code:: python

  @app.route ("/episode/<int:id>")
  def episode (was, \*\*karg):
    retrun was.request.ARGS.get ("id")
  # http://127.0.0.1:5000/episode/100

You can set default value to id, 

.. code:: python

  @app.route ("/episode/<int:id>", methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"])
  def episode (was, id = None):
    if was.request.method == "POST" and id is None:
      ...
      return was.API (id = new_id)
    return ...

It makes this URL working, 

.. code:: bash

  http://127.0.0.1:5000/episode

And was.ab will behaive like as below,

.. code:: bash

  was.ab ("episode")
  >> /episode
  
 was.ab ("episode", 100)
  >> /episode/100

*Note* that this does not works for root resource,

.. code:: python

  @app.route ("/<int:id>", methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"])
  def episode (was, id = None):
    if was.request.method == "POST" and id is None:
      ...
      return was.API (id = new_id)
    return ...

By above code, http://127.0.0.1:5000/ will not work. You should define "/" route. 



Query String Parameters
``````````````````````````````

qiery string parameter can be both resource arguments but needn't be.

.. code:: python
  
  @app.route ("/hello")
  def hello_world (was, num = 8):
    return num
  # http://127.0.0.1:5000/hello?num=100  

It is same as these,
  
.. code:: python

  @app.route ("/hello")
  def hello_world (was):
    return was.request.ARGS.get ("num")
  
  @app.route ("/hello")
  def hello_world (was, **url):
    return url.get ("num")
    # of 
    return was.request.URL.get ("num)    

Above 2 code blocks have a significant difference. First one can get only 'num' parameter. If URL query string contains other parameters, Skitai will raise 508 Error. But 2nd one can be any parameters.
    
Getting Form/JSON Parameters
```````````````````````````````

Getting form is not different from the way for url parameters, but generally form parameters is too many to use with each function parameters, can take from single args \*\*form or take mixed with named args and \*\*form both.
if request header has application/json 

.. code:: python

  @app.route ("/hello")
  def hello (was, **form):
    return "Post %s %s" % (form.get ("userid", ""), form.get ("comment", ""))
    
  @app.route ("/hello")
  def hello_world (was, userid, **form):
    return "Post %s %s" % (userid, form.get ("comment", ""))

Note that for receiving request body via arguments, you specify keywords args like \*\*karg or specify parameter names of body data.

If you want just handle POST body, you can use was.request.json () or was.request.form () that will return dictionary object.
  
Getting Composed Parameters
```````````````````````````````

You can receive all type of parameters by resource arguments. Let'assume yotu resource URL is http://127.0.0.1:5000/episode/100?topic=Python.

.. code:: python
  
  @app.route ("/episode/<int:id>")
  def hello (was, id, topic):
    pass

if URL is http://127.0.0.1:5000/episode/100?topic=Python with Form/JSON data {"comment": "It is good idea"}

.. code:: python
  
  @app.route ("/episode/<int:id>")
  def hello (was, id, topic, comment):
    pass
    
Note that argument should be ordered by:

- URL parameters
- URL query string
- Form/JSON body

And note if your request has both query string and form/JSON body, and want to receive form paramters via arguments, you should receive query string parameters first. It is not allowed to skip query string.

Also you can use keywords argument.

.. code:: python
    
  @app.route ("/episode/<int:id>")
  def hello (was, id, \*\*karg):
    karg.get ('topic')

Note that \*\*karg is contains both query string and form/JSON data and no retriction for parameter names.

was.requests.args is merged dictionary for all type of parameters. If parameter name is duplicated, its value will be set to form of value list (But If parameters exist both URL and form data, form data always has priority. It means URL parameter will be ignored). 
Then simpletst way for getting parameters, use was.request.args.
    

.. code:: python
  
  @app.route ("/episode/<int:id>")
  def hello (was, id):
    was.request.args.get ('topic')

Testing Parameters
```````````````````````````````

For parameter checking,

.. code:: python

  @app.route ("/test")
  @app.test_params ("ARGS", ["id"], ints = ["id"])
  def test (was, id):         
    return was.render ("test.html")

'id' is required and sholud be int type.

Spec is,

.. code:: python

  @app.test_params (scope, required = None, ints = None, floats = None, emails = None, uuids = None, **kargs)

You can test more detail using kargs.

.. code:: python
    
    @app.route ("/1")
    @app.test_params ("ARGS", a__gte = 5, b__between = (-4, -1), c__in = (1, 2))
    def index6 (was):
        return ""

- __between
- __neq
- __gt, __gte
- __lt, __lte

Checking parameter with regular expression,

.. code:: python

    @app.route ("/2")
    @app.test_params ("ARGS", a = re.compile ("^hans"))
    def index7 (was):
        return ""

Checking parameter length, use __len:

.. code:: python

    @app.route ("/3")
    @app.test_params ("ARGS", a__len__between = (4, 8))
    def index7 (was):
        return ""


Pre-Defined Parameter Values
``````````````````````````````````````````````````````

'me', 'notme' is special prameter value used by authentication.

- 'me' can be resolved into user ID on request handling
- 'notme' can ignore specific user ID for administative search purpose, BUT for your safey, 'notme' is allowed only with "GET" request
- 'new' is dummy value especially with "POST" method. But it is not restricted by methods. Maybe you can use 'new' with 'GET' for getting newlest items.

.. code:: python

  @app.route ("/episodes/<int:uid>")
  @app.permission_required (uid = ["staff"])
  def episodes (uid):
    ...

Now paramter 'uid' is bound with permission. 

Belows are all valid URI.

- GET /episodes/me, if request user have any permission
- DELETE /episodes/me if request user have any permission
- GET /episodes/4, if request user have staff permission, else raise 403 error
- PATCH /episodes/4, if request user have staff permission, else raise 403 error
- GET /episodes/new, if request user have staff permission, else raise 403 error
- POST /episodes/new, if request user have staff permission, else raise 403 error
- GET /episodes/notme, if request user have staff permission, else raise 403 error

But belows are all invalid and HTTP 421 error will be raised for your safety reason. If these're allowed, there is lot of danger delete/update all users (or all rows of database table).

- DELETE /episodes/notme
- POST /episodes/notme
- PATCH /episodes/notme
- PUT /episodes/notme

Obviously, I am sure you already know exact resource ID for above tasks.


Make Your Own Rule
``````````````````````````

The way to get parameters is little messy. But I want to try to make more pythonic style. Even all routed method can be called by another non app functions.

Initially I want to use like this.

.. code:: python
  
  @app.route ("/pets/<kind>")
  def pets (was, kind, limit, offset = 0, **JSON):
    ...
    
It can be requested by requests.

.. code:: python

  requests.post (
    "http://localhost/pets/dog?limit=10", 
    json = {"area": "LA"}
  )
  
If you need to check the origin of parameters, test_params decorator is useful.

.. code:: python
  
  @app.route ("/pets/<kind>")
  @app.test_params ("JSON", ["area"])
  def pets (was, kind, limit, offset = 0, **JSON):
    ...  

That's just my opinion.


Response
-------------

Basically, just return contents.

.. code:: python
  
  @app.route ("/hello")
  def hello_world (was):  
    return was.render ("hello.htm")

If you need set additional headers or HTTP status,
    
.. code:: python
  
  @app.route ("/hello")
  def hello (was):  
    return was.response ("200 OK", was.render ("hello.htm"), [("Cache-Control", "max-age=60")])

  def hello (was):  
    return was.response (body = was.render ("hello.htm"), headers = [("Cache-Control", "max-age=60")])

  def hello (was):         
    was.response.set_header ("Cache-Control", "max-age=60")
    return was.render ("hello.htm")

Above 3 examples will make exacltly same result.

Sending specific HTTP status code,

.. code:: python
  
  def hello (was):  
    return was.response ("404 Not Found", was.render ("err404.htm"))
  
  def hello (was):
    # if body is not given, automaticcally generated with default error template.
    return was.response ("404 Not Found")

If app raise exception, traceback information will be displayed only app.debug = True. But you intentionally send it inspite of app.debug = False:

.. code:: python
  
  # File
  @app.route ("/raise_exception")
  def raise_exception (was):  
    try:
      raise ValueError ("Test Error")
    except:      
      return was.response ("500 Internal Server Error", exc_info = sys.exc_info ())

If you use custom error handler, you can set detail explaination to error ["detail"]. 

.. code:: python
    
  @app.default_error_handler
  def default_error_handler (was, error):
    return was.render ("errors/default.html", error = error)
  
  def error (was):
    return was.response.with_explain ('503 Serivce Unavaliable', "Please Visit On Thurse Day")
        
        
You can return various objects.

.. code:: python
  
  # File
  @app.route ("/streaming")
  def streaming (was):  
    return was.response ("200 OK", open ("mypicnic.mp4", "rb"), headers = [("Content-Type", "video/mp4")])
  
  # Generator
  def build_csv (was):  
    def generate():
      for row in iter_all_rows():
        yield ','.join(row) + '\n'
    return was.response ("200 OK", generate (), headers = [("Content-Type", "text/csv")])   


All available return types are:

- String, Bytes, Unicode
- File-like object has 'read (buffer_size)' method, optional 'close ()'
- Iterator/Generator object has 'next() or _next()' method, optional 'close ()' and shoud raise StopIteration if no more data exists.
- Something object has 'more()' method, optional 'close ()'
- Classes of skitai.lib.producers
- List/Tuple contains above objects
- XMLRPC dumpable object for if you want to response to XMLRPC

The object has 'close ()' method, will be called when all data consumed, or socket is disconnected with client by any reasons.

- was.response (status = "200 OK", body = None, headers = None, exc_info = None)
- was.response.throw (status = "200 OK"): abort handling request, generated contents and return http error immediatly

- was.API (\_\_data_dict\_\_ = None, \*\*kargs): return api response container
- was.Fault (status = "200 OK",\*args, \*\*kargs): shortcut for was.response (status, was.API (...)) if status code is 2xx and was.response (status, was.Fault (...))
- was.Fault (msg, code = 20000,  debug = None, more_info = None, exc_info = None): return api response container with setting error information
- was.response.traceback (msg = "", code = 10001,  debug = 'see traceback', more_info = None): return api response container with setting traceback info

- was.response.set_status (status) # "200 OK", "404 Not Found"
- was.response.get_status ()
- was.response.set_headers (headers) # [(key, value), ...]
- was.response.get_headers ()
- was.response.set_header (k, v)
- was.response.get_header (k)
- was.response.del_header (k)
- was.response.hint_promise (uri) # *New in skitai version 0.16.4*, only works with HTTP/2.x and will be ignored HTTP/1.x


HTTP Exception 
``````````````````````````

Abort immediatly and send HTTP eroor content.

.. code:: python

  @app.route ("/<filename>")
  def getfile (was, filename):  
    if not os.path.isfile (filename):
    	raise was.Error ("404 Not Found", "{} not exists".format (filename))    
    return was.File (filename)

    
File Stream 
`````````````

Response provides some methods for special objects.

First of all, for send a file, 

.. code:: python

  @app.route ("/<filename>")
  def getfile (was, filename):  
    return was.File ('/data/%s' % filename)    


JSON API Response
````````````````````
*New in skitai version 0.26.15.9*

In cases you want to retrun JSON API reponse,

.. code:: python
  
  # return JSON {data: [1,2,3]}
  return was.Fault ('200 OK', data = [1, 2, 3])
  # return empty JSON {}
  return was.Fault (201 Accept')
  
  # and shortcut if response HTTP status code is 200 OK,
  return was.API (data =  [1, 2, 3])
  
  # return empty JSON {}
  return was.API ()
  
For sending error response with error information,

.. code:: python
  
  # client will get, {"message": "parameter q required", "code": 10021}
  return was.Fault ('400 Bad Request', 'missing parameter', 10021)  
  
  # with additional information,
  was.Fault (
  	'400 Bad Request',
  	'missing parameter', 10021, 
    'need parameter offset and limit', # detailed debug information
    'http://127.0.0.1/moreinfo/10021', # more detail URL something    
  )

You can send traceback information for debug purpose like in case app.debug = False,

.. code:: python
  
  try:
    do something
  except:
    return was.Fault (
      '500 Internal Server Error',
      'somethig is not valid', 
      10022, 
      traceback = True
    ) 

  # client see,
  {
    "code": 10001,
    "message": "somethig is not valid",
    "debug": "see traceback", 
    "traceback": [
      "name 'aa' is not defined", 
      "in file app.py at line 276, function search"      
    ]
  }

Important note that this response will return with HTTP 200 OK status. If you want return 500 code, just let exception go.

But if your client send header with 'Accept: application/json' and app.debug is True, Skitai returns traceback information automatically.


Future / Futures Response
```````````````````````````````````````````````

* New in version 0.2*

With single thread it will be the problem using was' request services with dispatch (), It is almost works as IO blocking situation.

was.Futures returns Futures instance for delaying response until every awaitable tasks are finished and every future tasks will be executed concurrently.

*CAUTIONS:* 

1. Futures escape ealry from current requet handling thread pool and enter to main event loop. It means they will make connections to targets as possible as they can. If hundreds of clients request resource using database/upstream server, It will make error on target server like "too manty connection error". If you use Futures response, you SHOULD make sure these factors.
2. Futures might be the most efficient if it satisfy 2 conditions, a few simultaneously requesting clients, streaming data is relatively small size. Lot of clients will consume connection resources fast and large data stream make blanch coroutine advantages caused of expensive networking cost.
3. Then you could consider using was.Tasks first because Tasks is within thread pool, it will be limit number of connections by number of thread pool.  

*NOTE*: With my personal benchmark, it is not very impressive performance. I have maden 3 backend requests per client requests with weigHTTP (weigHTTP -n 3000 -c 1000 -k http://.../bench). Then was.Tasks and was.Futures are almost same performance. And was.Tasks is just 20% faster than sequencial synchronous requests. Very disappointing  results. I recoomend to use was.Tasks NOT was.Futures.    

.. code:: python

  def test_futures (app, dbpath):
    @app.route ("/")
    def index (was):
        def response (was, tasks):
            return was.API (status_code = [task.status_code for task in tasks.dispatch ()]) 
        
        reqs = [
            was.get ("@pypi/project/skitai/"),
            was.get ("@pypi/project/rs4/"),
            was.db ("@sqlite").execute ('SELECT * FROM stocks WHERE symbol=?', ('RHAT',))
        ]
        return was.Futures (reqs, timeout = 2).then (response)
    
    app.alias ("@pypi", skitai.PROTO_HTTPS, "pypi.org")    
    app.alias ("@sqlite", skitai.DB_SQLITE3, dbpath)    
    with app.test_client ("/", confutil.getroot ()) as cli:
        resp = cli.get ("/")
        assert resp.data ['status_code'] == [200, 200, 200]

Note that at callback, Futures is converted into Tasks_. Then you can use dispatch, wait, fetch ... things.

.. _Tasks: https://pypi.org/project/skitai/#tasks


Another example,

.. code:: python

  def test_futures (app, dbpath):
    @app.route ("/")
    def index (was):
        def response (was, tasks):
            tasks.stock.announcements = tasks [0].fetch ()
            return was.API (tasks.stock)
        
        stock = was.db ("@sqlite").select (stocks").get ("*").filter (symbol='RHAT').execute ().one ()        
        reqs = [was.db ("@sqlite").select (announcements").get ("*").filter (id = stock.id).execute ()]
        return was.Futures (reqs, stock = stock [0]).then (response)
    
    app.alias ("@pypi", skitai.PROTO_HTTPS, "pypi.org")    
    app.alias ("@sqlite", skitai.DB_SQLITE3, dbpath)    
    with app.test_client ("/", confutil.getroot ()) as cli:
        resp = cli.get ("/")
        resp.data

Chaining is also possible,

.. code:: python

    @app.route ("/")
    def index (was):
        def repond (was, tasks):        
            return was.API (status_code_db = [task.status_code for task in tasks.dispatch ()], b = tasks.b, status_code = tasks.status_code) 
        
        def checkdb (was, tasks):
            reqs = [was.db ("@sqlite").execute ('SELECT * FROM stocks WHERE symbol=?', ('RHAT',))]
            status_code = [rs.status_code for rs in tasks.dispatch ()]
            return was.Futures (reqs, b = tasks.a + 100, status_code = status_code).then (repond)
        
        reqs = [
            was.get ("@pypi/project/skitai/"),
            was.get ("@pypi/project/rs4/")            
        ]
        return was.Futures (reqs, a = 100).then (checkdb)
        
    app.alias ("@pypi", skitai.PROTO_HTTPS, "pypi.org")    
    app.alias ("@sqlite", skitai.DB_SQLITE3, dbpath)    
    with app.test_client ("/", confutil.getroot ()) as cli:
        resp = cli.get ("/")
        resp.data        
        >> {'b': 200, 'status_code': [200, 200], 'status_code_db': [200]}


Process / Thread Response
`````````````````````````````````````````

These are very same with Future response.

.. code:: python
  
  @app.route ('...')
  def foo ():    
    def repond (was, tasks):        
        return was.API (status_code_db = [task.status_code for task in tasks.dispatch ()], b = tasks.b, status_code = tasks.status_code)         
    return was.Process (math.sqrt, 4.0).then (respond)


Proxypass Response
```````````````````````````````````

Skitai's mounted proxypass is higher priority than WSGI app. If you want make this to lower  priority, can use was.proxypass.

.. code:: python

  @app.route ("/<path:path>")
  def proxy (was, path = None):
    return was.proxypass ("@myupstream", path)

But it is valid only if request method is GET, because it is mainly used for building integrated development environment with frontend frameworks linke Node.js.


Mounting Resources: Making Simpler & Modular App
-------------------------------------------------------------------

*New in skitai version 0.26.17*

Implicit Mount Services On Your App
````````````````````````````````````````````

I already mentioned *App Structure* section, you can split yours views and help utilties into services directory.

Assume your application directory structure is like this,

.. code:: bash

  templates/*.html  
  services/*.py # app library, all modules in this directory will be watched for reloading  
  static/images # static files
  static/js
  static/css
  
  app.py # this is starter script  

app.py
  
.. code:: python

  from services import auth
  
  app = Atila (__name__)

  app.debug = True
  app.use_reloader = True

  @app.default_error_handler
  def default_error_handler (was, e):
    return str (e)
    
services/auth.py

.. code:: python
  
  # shared utility functions used by views
  
  def titlize (s):
    ...
    return s
  
  def __mount__ (app):
    @app.login_handler      
    def login_handler (was):  
      if was.session.get ("username"):
        return
      next_url = not was.request.uri.endswith ("signout") and was.request.uri or ""    
      return was.redirect (was.ab ("signin", next_url))
      
    @app.route ("/signout")
    def signout (was):
      was.session.remove ("username")
      was.mbox.push ("Signed out successfully", "success")  
      return was.redirect (was.ab ('index'))
      
    @app.route ("/signin")
    def signin (was, next_url = None, **form):
      if was.request.args.get ("username"):
        user = auth.authenticate (was.django, username = was.request.args ["username"], password = was.request.args ["password"])
        if user:
          was.session.set ("username", was.request.args ["username"])
          return was.redirect (was.request.args ["next_url"])
        else:
          was.mbox.push ("Invalid User Name or Password", "error", icon = "new_releases")
      return was.render ("sign/signin.html", next_url = next_url or was.ab ("index"))

You just import module from services. but *def __mount__ (app)* is core in each module. Every modules can have *__mount__ (app)* in *services*, so you can split and modulize views and utility functions. __mount__ (app) will be automatically executed on starting. If you set app.use_reloader, theses services will be automatically reloaded and re-executed on file changing. Also you can make global app sharable functions into seperate module like util.py without views.

Explicit Mount Services On Your App
````````````````````````````````````````````

If you want to select services - not automatically - set app.auto_mount = False. 

.. code:: python

  from services import auth, search
  
  app = Atila (__name__)
  app.auto_mount = False
  
  app.mount (search)

Above case, auth module has mount function but will not be mounted.   


Mouning Services With Options
`````````````````````````````````````````````````

If you need additional options on decorating,

.. code:: python

  def __mount__ (app):
    @app.route ("/login")
    def login (was):
      ...

And on app, 
      
.. code:: python

  from services import auth
  
  app = Atila (__name__)
  app.mount ('/regist', auth)

Finally, route of login is "/regist/login".
  
Sometimes function names are duplicated if like you import contributed services.

.. code:: python

  from services import auth
  
  app = Atila (__name__)
  app.mount ( '/regist', auth, ns = "regist")
  
Now, you can import iport without name collision. But be careful when use was.ab () etc.

Note that options should be keyword arguments.

.. code:: python

  {{ was.ab ("regist.login") }}
      
If you want to mount only debug environment, 

.. code:: python
  
  app.mount (auth, debug_only = True)

If you want to authentify to all services, 

.. code:: python
  
  app.mount (auth, authenticate = "bearer")

Currently *reserved arguments* are:

- ns
- authenticate
- debug_only
- mount

Your custom options can be accessed by __mntopt__ in your module.

First, mount with redirect option.

.. code:: python
  
    app.mount (auth, redirect = "index")    
    # automatically set to auth.__mntopt__ = {"redirect": "index"}

then you can access in auth.py, 

.. code:: python

    @app.route ("/regist/signout")
    def signout (was):
        was.mbox.push ("Signed out successfully", "success")
        return was.redirect (was.ab (__mntopt__.get ("redirect", 'index')))
    
If you build useful services, please contribute them to `atila.services`_.


Unmounting Resources
```````````````````````````````

*New in skitai version 0.27*

Also 'umount' is avaliable for cleaning up module resource. 

.. code:: python
  
  resource = ...
  
  def __umount__ (app):
    resource.close ()
    app.someghing = None

This will be automatically called when:

- before module itself is reloading
- before app is reloading
- app unmounted from Skitai 


More About Namespace
````````````````````````````````````

If you develop reusable task modules, pay attention to namespace and URL building. 

For example, below module is mount with app.mount (auth, ns = "regist").  

.. code:: python
  
  # auth.py

  def __mount__ (app):
    @app.route ("/func1")
    def func1 (was, a):
      ...
    
    @app.route ("/func2")
    def func2 (was):
      was.ab ("func1", "hello")

This was.ab ("func1") in func2 might be dangerous, because this task modules may have namespace. Then you consider ns like this.

.. code:: python

  was.ab ("{}func1".format (__mntopt__.get ("ns") and __mntopt__ ["ns"] + "." or ""), , "hello")

But it is not pretty, so you can pretty style,

.. code:: python
  
  @app.route ("/func2")
  def func2 (was):
    was.ab (func1, "hello")


Manual Mounting
```````````````````````````

Atila automaticall mount your services which have mount () funtion, but you can disable this, and mount explicit.

*New in skitai version 0.27*

If you mount manually, set app.auto_mount = False and call mount () for each modules you want.

.. code:: python

  from services import auth, index  
  app = Atila (__name__)  
  
  app.auto_mount = False
  app.mount ("/v2", auth, index)
  app.mount ("/v2", pets)
    
  skitai.mount ("/", app)
  

.. _`atila.services`: https://gitlab.com/hansroh/atila/tree/master/atila/contrib/services


More About Websocket
--------------------------------------

*websocket design specs* can  be choosen one of 3.

WS_SIMPLE

  - Thread pool manages n websocket connection
  - It's simple request and response way like AJAX  
  - Low cost on threads resources, but reposne cost is relatvley high than the others

WS_THREADSAFE (New in version 0.26)

  - Mostly same as WS_SIMPLE
  - Message sending is thread safe
  - Most case you needn't this option, but you create uourself one or more threads using websocket.send () method you need this for your convinience
 
WS_GROUPCHAT (New in version 0.24)
  
  - Thread pool manages n websockets connection
  - Chat room model


*message_encoding*

Websocket messages will be automatically converted to theses objects. Note that option is only available with Atila WSGI container.

  - WS_MSG_JSON
  - WS_MSG_XMLRPC
  
*New in skitai version 0.26.18*

Websokect usage is already explained, but Atila provide @app.websocket decorator for more elegant way to use it.

.. code:: python

  def onopen (was):
    print ('websocket opened')

  def onclose (was):
    print ('websocket closed')
    
  @app.route ("/websocket")
  @app.websocket (skitai.WS_SIMPLE, 1200, onopen, onclose)
  def websocket (was, message):
    return 'you said: ' + message

This decorator spec is,

.. code:: python
     
  @app.websocket (
    spec, # one of skitai.WS_SIMPLE, skitai.WS_THREADSAFE and skitai.WS_GROUPCHAT	 
    timeout = 60, 
    onopen = None, 
    onclose = None 
  )

In some cases, you need additional parameter for opening/closing websocket.

.. code:: python

  @app.route ("/websocket")
  @app.websocket (skitai.WS_THREADSAFE, 1200, onopen)
  def websocket (was, message, option):
    return 'you said: ' + message

Then, your onopen function must have additional parameters except *message*.

.. code:: python

  def onopen (was):
    print ('websocket opened with', was.request.ARGS ["option"])
    
Now, your websocket endpoint is "ws://127.0.0.1:5000/websocket?option=value"

WS_NQ does not use queue or thread pool. In this case, response is more faster but if response includes IO blocking operation, entire Skitai event loop will be blocked. 
  
.. code:: python

  @app.route ("/websocket")
  @app.websocket (skitai.WS_SIMPLE | skitai.WS_NQ, 1200, onopen)
  def websocket (was, message):
    return 'you said: ' + message


Pushing Message Through Connected Client
--------------------------------------------------------------

Save websocket client id to session. 

.. code:: python
  
  def onopen (was):
    was.session.set ("WS_ID", was.websocket.client_id)
  
  def onclose (was):
    was.session.remove ("WS_ID")
  
  @app.route ("/websocket")
  @app.websocket (skitai.WS_SIMPLE | skitai.WS_FAST, 1200, onopen, onclose)
  def websocket (was, message):    
    return 'you said: ' + message

And push message to client.

.. code:: python

  @app.route ("/item_in_stock")  
  def item_in_stock (was):
    app.websocket_send (
      was.session.get ("WS_ID"),
      "Item In Stock!"
    )

*Note:*: I'm not sure it is works in all web browser.


Building URL
---------------

If your app is mounted at "/math",

.. code:: python

  @app.route ("/add")
  def add (was, num1, num2):  
    return int (num1) + int (num2)
    
  was.app.build_url ("add", 10, 40) # returned '/math/add?num1=10&num2=40'
  
  # BUT it's too long to use practically,
  # was.ab is acronym for was.app.build_url
  was.ab ("add", 10, 40) # returned '/math/add?num1=10&num2=40'
  was.ab ("add", 10, num2=60) # returned '/math/add?num1=10&num2=60'
  
  #You can use function directly as well,  
  was.ab (add, 10, 40) # returned '/math/add?num1=10&num2=40'
  
  @app.route ("/hello/<name>")
  def hello (was, name = "Hans Roh"):
    return "Hello, %s" % name
  
  was.ab ("hello", "Your Name") # returned '/math/hello/Your_Name'
  
Basically, was.ab is same as Python function call.


Building URL by Updating Parameters Partially
````````````````````````````````````````````````

**New in skitai version 0.27**

.. code:: python

  @app.route ("/navigate")
  def navigate (was, limit = 20, pageno = 1):  
    return ...
  
If this resource was requested by /naviagte?limit=100&pageno=2, and if you want to make new resource url with keep a's value (=100), you can make URL like this,

.. code:: python

  was.ab ("navigate", was.request.args.limit, 3)
  
But you can update only changed parameters partially,

.. code:: python

  was.partial ("add", pageno = 3)
  
Parameter a's value will be kept with current requested parameters. Note that was.partial can be recieved keyword arguments only except first resource name.

was.partial is used changing partial parameters (or none) based over current parameters.


Building Base URL without Parameters
````````````````````````````````````

**New in skitai version 0.27**

Sometimes you need to know just resource's base path info - especially client-side javascript URL building, then use *was.basepath*.

.. code:: python

  @app.route ("/navigate")
  def navigate (was, limit, pageno = 1):  
    return ...
  
.. code:: python

  was.basepath ("navigate")
  >> return "/navigate"

For example, in your VueJS template,
  
.. code:: html

  <a :href="'{{ was.basepath ('navigate') }}?limit=' + limit_option + '&pageno=' + (current_page + 1)">Next Page</a>

Note that base path means for fancy Url, 

.. code:: python

  @app.route ("/user/<id>")
  >> base path is "/user/"
  
  @app.route ("/user/<id>/pat")
  >> base path is "/user/"
  

Access Environment Variables
------------------------------

was.env is just Python dictionary object.

.. code:: python

  if "HTTP_USER_AGENT" in was.env:
    ...
  was.env.get ("CONTENT_TYPE")


Access Cookie
----------------

was.cookie has almost dictionary methods.

.. code:: python

  if "user_id" not in was.cookie:
    was.cookie.set ("user_id", "hansroh")    
    # or    
    was.cookie ["user_id"] = "hansroh"


*Changed in version 0.15.30*

'was.cookie.set()' method prototype has been changed.

.. code:: python

  was.cookie.set (
    key, val, 
    expires = None, 
    path = None, domain = None, 
    secure = False, http_only = False
  ) 

'expires' args is seconds to expire. 

 - if None, this cookie valid until browser closed
 - if 0 or 'now', expired immediately
 - if 'never', expire date will be set to a hundred years from now

If 'secure' and 'http_only' options are set to True, 'Secure' and 'HttpOnly' parameters will be added to Set-Cookie header.

If 'path' is None, every app's cookie path will be automaticaaly set to their mount point.

For example, your admin app is mounted on "/admin" in configuration file like this:

.. code:: python

  app = ... ()
  
  if __name__ == "__main__": 
  
    import skitai
    
    skitai.run (
      address = "127.0.0.1",
      port = 5000,
      mount = {'/admin': app}
    )

If you don't specify cookie path when set, cookie path will be automatically set to '/admin'. So you want to access from another apps, cookie should be set with upper path = '/'.

.. code:: python
  
  was.cookie.set ('private_cookie', val)
        
  was.cookie.set ('public_cookie', val, path = '/')
    
- was.cookie.set (key, val, expires = None, path = None, domain = None, secure = False, http_only = False)
- was.cookie.remove (key, path, domain)
- was.cookie.clear (path, domain)
- was.cookie.keys ()
- was.cookie.values ()
- was.cookie.items ()
- was.cookie.has_key ()


Access Session
----------------

Strictly speaking, Atila hasn't got traditional session which some data is stored on server side. And it doesn't provide any abstract classes or methods for storing.

Ailta's session is just one of cookie value which contains signature for checking alternation by any other things except Atila.


was.session has almost dictionary methods.

To enable session for app, random string formatted securekey should be set for encrypt/decrypt session values.

*WARNING*: `securekey` should be same on all skitai apps at least within a virtual hosing group, Otherwise it will be serious disaster.

.. code:: python

  app.securekey = "ds8fdsflksdjf9879dsf;?<>Asda"
  app.session_timeout = 1200 # sec
  
  @app.route ("/session")
  def hello_world (was, **form):  
    if "login" not in was.session:
      was.session.set ("user_id", form.get ("hansroh"))
      # or
      was.session ["user_id"] = form.get ("hansroh")

If you set, alter or remove session value, session expiry is automatically extended by app.session_timeout. But just getting value will not be extended. If you extend explicit without altering value, you can use touch() or set_expiry(). session.touch() will extend by app.session_timeout. session.set_expiry (timeout) will extend by timeout value.

Once you set expiry, session auto extenstion will be disabled until expiry time become shoter than new expiry time is calculated by app.session_timeout.  

- was.session.set (key, val)
- was.session.get (key, default = None)
- was.session.source_verified (): If current IP address matches with last IP accesss session
- was.session.getv (key, default = None): If not source_verified (), return default
- was.session.remove (key)
- was.session.clear ()
- was.session.keys ()
- was.session.values ()
- was.session.items ()
- was.session.has_key ()
- was.session.set_expiry (timeout)
- was.session.touch ()
- was.session.expire ()


Messaging Box
----------------

Like Flask's flash feature, Skitai also provide messaging tool.

.. code:: python  

  @app.route ("/msg")
  def msg (was):
    was.mbox.send ("This is Flash Message", "flash")
    was.mbox.send ("This is Alert Message Kept by 60 seconds on every request", "alram", valid = 60)
    return was.redirect (was.ab ("showmsg", "Hans Roh"), status = "302 Object Moved")
  
  @app.route ("/showmsg")
  def showmsg (was, name):
    return was.render ("msg.htm", name=name)
    
A part of msg.htm is like this:

.. code:: html

  Messages To {{ name }},
  <ul>
    {% for message_id, category, created, valid, msg, extra in was.mbox.get () %}
      <li> {{ mtype }}: {{ msg }}</li>
    {% endfor %}
  </ul>

Default value of valid argument is 0, which means if page called was.mbox.get() is finished successfully, it is automatically deleted from mbox.

But like flash message, if messages are delayed by next request, these messages are save into secured cookie value, so delayed/long term valid messages size is limited by cookie specificatio. Then shorter and fewer messsages would be better as possible.

'was.mbox' can be used for general page creation like handling notice, alram or error messages consistently. In this case, these messages (valid=0) is consumed by current request, there's no particular size limitation.

Also note valid argument is 0, it will be shown at next request just one time, but inspite of next request is after hundred years, it will be shown if browser has cookie values.

.. code:: python  
  
  @app.before_request
  def before_request (was):
    if has_new_item ():
      was.mbox.send ("New Item Arrived", "notice")
  
  @app.route ("/main")  
  def main (was):
    return was.render ("news.htm")

news.htm like this:

.. code:: html

  News for {{ was.g.username }},
  <ul>
    {% for mid, category, created, valid, msg, extra in was.mbox.get ("notice", "news") %}
      <li class="{{category}}"> {{ msg }}</li>
    {% endfor %}
  </ul>

- was.mbox.send (msg, category, valid_seconds, key=val, ...)
- was.mbox.get () return [(message_id, category, created_time, valid_seconds, msg, extra_dict)]
- was.mbox.get (category) filtered by category
- was.mbox.get (key, val) filtered by extra_dict
- was.mbox.source_verified (): If current IP address matches with last IP accesss mbox
- was.mbox.getv (...) return get () if source_verified ()
- was.mbox.search (key, val): find in extra_dict. if val is not given or given None, compare with category name. return [message_id, ...]
- was.mbox.remove (message_id)


Named Session & Messaging Box
------------------------------

*New in skitai version 0.15.30*

You can create multiple named session and mbox objects by mount() methods.

.. code:: python

  was.session.mount (
    name = None, securekey = None, 
    path = None, domain = None, secure = False, http_only = False, 
    session_timeout = None
   )
  
  was.mbox.mount (
    name = None, securekey = None, 
    path = None, domain = None, secure = False, http_only = False
  )


For example, your app need isolated session or mbox seperated default session for any reasons, can create session named 'ADM' and if this session or mbox is valid at only /admin URL.

.. code:: python

  @app.route("/")
  def index (was):   
    was.session.mount ("ADM", SECUREKEY_STRING, path = '/admin')
    was.session.set ("admin_login", True)

    was.mbox.mount ("ADM", SECUREKEY_STRING, path = '/admin')
    was.mbox.send ("10 data has been deleted", 'warning')

SECUREKEY_STRING needn't same with app.securekey. And path, domain, secure, http_only args is for session cookie, you can mount any named sessions or mboxes with upper cookie path and upper cookie domain. In other words, to share session or mbox with another apps, path should be closer to root (/).

.. code:: python

  @app.route("/")
  def index (was):   
    was.session.mount ("ADM", SECUREKEY_STRING, path = '/')
    was.session.set ("admin_login", True)

Above 'ADM' sesion can be accessed by all mounted apps because path is '/'.
    
Also note was.session.mount (None, SECUREKEY_STRING) is exactly same as mounting default session, but in this case SECUREKEY_STRING should be same as app.securekey.

mount() is create named session or mbox if not exists, exists() is just check wheather exists named session already.

.. code:: python

  if not was.session.exists (None):
    return "Your session maybe expired or signed out, please sign in again"
      
  if not was.session.exists ("ADM"):
    return "Your admin session maybe expired or signed out, please sign in again"



File Upload
---------------

.. code:: python
  
  FORM = """
    <form enctype="multipart/form-data" method="post">
    <input type="hidden" name="submit-hidden" value="Genious">   
    <p></p>What is your name? <input type="text" name="submit-name" value="Hans Roh"></p>
    <p></p>What files are you sending? <br />
    <input type="file" name="file">
    </p>
    <input type="submit" value="Send"> 
    <input type="reset">
  </form>
  """
  
  @app.route ("/upload")
  def upload (was, *form):
    if was.request.command == "get":
      return FORM
    else:
      file = form.get ("file")
      if file:
        file.save ("d:\\var\\upload", dup = "o") # overwrite
        
'file' object's attributes are:

- file.path: temporary saved file full path
- file.name: original file name posted
- file.size
- file.mimetype
- file.save (into, name = None, mkdir = False, dup = "u")
- file.remove ()
- file.read ()

  * if name is None, used file.name
  * dup: 
    
    + u - make unique (default)
    + o - overwrite


Using SQL Map with SQLPhile
---------------------------------

*New in Version 0.26.13*

SQLPhile_ is SQL generator and can be accessed from was.sql.

was.sql is a instance of sqlphile.SQLPhile.

If you want to use SQL templates, create sub directory 'sqlmaps' and place sqlmap files.

.. code:: python
  
  # default engine is skitai.DB_PGSQL and also available skitai.DB_SQLITE3
  # no need call for skitai.DB_PGSQL
  app.setup_sqlphile (skitai.DB_SQLITE3)
  
  @app.route ("/")
  def index (was):
    q = was.sql.select (tbl_'user').get ('id, name').filter (id = 4)
    req = was.db ("@db").execute (q)
    result = req.getwait ()

*New in skitai version 0.27*

From version 0.27 SQLPhile_ is integrated with PostgreSQL and SQLite3.

.. code:: python
    
    app = Atila (__name__)
    app.setup_sqlphile (skitai.DB_PGSQL)
    
    @app.route ("/")
    def query (was):
      dbo = was.db ("@mypostgres")    
      req = dbo.select ("cities").get ("id, name").filter (name__like = "virginia").execute ()
      response = req.getwait (timeout = 2)    
      dbo.insert ("cities").data (name = "New York").execute ().wait_or_throw ("500 Server Error")
     
      
Please, visit SQLPhile_ for more detail. 
    
.. _SQLPhile: https://pypi.python.org/pypi/sqlphile


Registering Per Request Calling Functions
-------------------------------------------

Method decorators called automatically when each method is requested in a app.

.. code:: python

  @app.before_request
  def before_request (was):
    if not login ():
      return "Not Authorized"
  
  @app.finish_request
  def finish_request (was):
    was.g.user_id    
    was.g.user_status
    ...
  
  @app.failed_request
  def failed_request (was, exc_info):
    was.g.user_id    
    was.g.user_status
    ...
  
  @app.teardown_request
  def teardown_request (was):
    was.g.resouce.close ()
    ...
  
  @app.route ("/view-account")
  def view_account (was, userid):
    was.g.user_id = "jerry"
    was.g.user_status = "active"
    was.g.resouce = open ()
    return ...

For this situation, 'was' provide was.g that is empty class instance. was.g is valid only in current request. After end of current request.

If view_account is called, Atila execute these sequence:

.. code:: python
  
  try:
    try: 
      content = before_request (was)
      if content:
        return content
      content = view_account (was, *args, **karg)
      
    except:
      content = failed_request (was, sys.exc_info ())
      if content is None:
        raise
      
    else:
      finish_request (was)

  finally:
    teardown_request (was)
  
  return content
    
Be attention, failed_request's 2nd arguments is sys.exc_info (). Also finish_request and teardown_request (NOT failed_request) should return None (or return nothing). 

If you handle exception with failed_request (), return custom error content, or exception will be reraised and Atila will handle exception.

*New in skitai version 0.14.13*

.. code:: python

  @app.failed_request
  def failed_request (was, exc_info):
    # releasing resources
    return was.response (
      "501 Server Error", 
      was.render ("err501.htm", msg = "We're sorry but something's going wrong")
    )

Define Autoruns 
--------------------------------

*New in skitai version 0.26.18*

You can make automation for preworks and postworks.

.. code:: python
  
  def pre1 (was):
    ...
  
  def pre2 (was):
    ...
  
  def post1 (was):
    ...
  
  @app.run_before (pre1, pre2)
  @app.run_after (post1)
  def index (was):
    return was.render ('index.html')

@app.run_before can return None or responsable contents for aborting all next run_before and main request.
@app.run_after return will be ignored

Define Conditional Prework 
-------------------------------

*New in skitai version 0.26.18*

@app.if~s are conditional executing decorators. 

.. code:: python

  def reload_config (was, path):
    ...
  
  @app.if_file_modified ('/opt/myapp/config', reload_config, interval = 1)
  def index (was):
    return was.render ('index.html')

@app.if_updated need more explaination.


Inter Process Update Notification and Consequences Automation
----------------------------------------------------------------

*New in skitai version 0.26.18*

@app.if_updated is related with skitai.register_states (), was.setlu() and was.getlu() and these are already explained was cache contorl part. And Atila app can use more conviniently.

These're used for mostly inter-process notification protocol.

Before skitai.run (), you should define updatable objects as string keys:

.. code:: python

  skitai.register_states ("weather-news", ...)

Then one process update object and update time by setlu ().

.. code:: python

  @app.route ("/")
  def add_weather (was):
    was.db.execute ("insert into weathers ...")
    was.setlu ("weather-news")
    return ... 

This update time stamp will be recorded in shared memory, then all skitai worker processes can catch this update by comparing previous last update time and automate consequences like refreshing cache.

.. code:: python
  
  def reload_cache (was, key):
    ...
  
  @app.if_updated ('weather-news', reload_cache)
  def index (was):
    return was.render ('index.html')
     

App Lifecycle Hook
----------------------

These app life cycle methods will be called by this order,

- before_mount (wac): when app imported on skitai server started
- mounted (*was*): called first with was (instance of wac)
- mounted_or_reloaded (*was*): called with was (instance of wac)
- loop whenever app is reloaded,
    
  - oldapp.before_reload (*was*)
  - newapp.reloaded (*was*)
  - mounted_or_reloaded (*was*): called with was (instance of wac)
  
- before_umount (*was*): called last with was (instance of wac), add shutting down process
- umounted (wac): when skitai server enter shutdown process

Please note that first arg of startup, reload and shutdown is *wac* not *was*. *wac* is Python Class object of 'was', so mainly used for sharing Skitai server-wide object via was.object before instancelizing to *was*.

.. code:: python

  @app.before_mount
  def before_mount (wac):
    logger = wac.logger.get ("app")
    # OR
    logger = wac.logger.make_logger ("login", "daily")
    config = wac.config
    wac.register ("loginengine", SNSLoginEngine (logger))
    wac.register ("searcher", FulltextSearcher (wac.numthreads))    
  
  @app.before_reload
  def before_remount (wac):
    wac.loginengine.reset ()
  
  @app.umounted
  def before_umount (wac):
    wac.umounted.close ()
        
    wac.unregister ("loginengine")
    wac.unregister ("searcher")

You can access numthreads, logger, config from wac.

As a result, myobject can be accessed by all your current app functions even all other apps mounted on Skitai.

.. code:: python
  
  # app mounted to 'abc.com/register'
  @app.route ("/")
  def index (was):
    was.loginengine.check_user_to ("facebook")
    was.searcher.query ("ipad")
  
  # app mounted to 'def.com/'
  @app.route ("/")
  def index (was):
    was.searcher.query ("news")

*Note:* The way to mount with host, see *'Mounting With Virtual Host'* chapter below.

It maybe used like plugin system. If a app which should be mounted loads pulgin-like objects, theses can be used by Skitai server wide apps via was.object1, was.object2,...

*New in skitai version 0.26*

If you have databases or API servers, and want to create cache object on app starting, you can use @app.mounted decorator.

.. code:: python
  
  def create_cache (res):
    d = {}
    for row in res.data:
      d [row.code] = row.name
    app.store.set ('STATENAMES', d)
  
  @app.mounted
  def mounted (was):
    was.db ('@mydb', callback = create_cache).execute ("select code, name from states;")    
    # or use REST API
    was.get ('@myapi/v1/states', callback = create_cache)
    # or use RPC
    was.rpc ('@myrpc/rpc2', callback = create_cache).get_states ()
  
  @app.reloaded
  def reloaded (was):
    mounted (was) # same as mounted
  
  @app.before_umount
  def before_umount (was):
    was.delete ('@session/v1/sessions', callback = lambda x: None)    
    
But both are not called by request, you CAN'T use request related objects like was.request, was.cookie etc. And SHOULD use callback because these are executed within Main thread.

    
Login and Permission Helper
------------------------------

*New in skitai version 0.26.16*

You can define login & permissoin check handler,

.. code:: python

  @app.login_handler
  def login_handler (was):  
    if was.session.get ("demo_username"):
      return
    
    if was.request.args.get ("username"):
      if not was.csrf_verify ():
        return was.response ("400 Bad Request")
      
      if was.request.args.get ("signin"):
        user, level = authenticate (username = was.request.args ["username"], password = was.request.args ["password"])
        if user:
          was.session.set ("demo_username", user)
          was.session.set ("demo_permission", level)
          return
          
        else:
          was.mbox.send ("Invalid User Name or Password", "error")    
          
    return was.render ("login.html", user_form = forms.DemoUserForm ())

  @app.permission_check_handler
  def permission_check_handler (was, perms):
    if was.session.get ("demo_permission") in perms:
      return was.response ("403 Permission Denied")
  
  @app.staff_member_check_handler
  def staff_check_handler (was):
    if was.session.get ("demo_permission") not in ('staff'):
      return was.response ("403 Staff Permission Required")

If you are using JWT you can integrate with this, And it is replacable instead of app.authorization_required.

.. code:: python

  @app.permission_check_handler
  def permission_check_handler (was, perms):
      claims = was.request.JWT
      if "err" in claims: return claims ["err"]
      if not perms: 
        return # permit
      for p in claims ["levels"]:
          if p in perms:
              return # permit
      return was.response ("403 Permission Denied")
      
And use it for your resources if you need,

.. code:: python

  @app.route ("/")
  @app.permission_required (["admin"])  
  @app.login_required
  def index (was):
    return "Hello"
  
  @app.staff_member_required
  def index2 (was):
    return "Hello"

If every thing is OK, it *SHOULD return None, not True*.

Conditional Permission Control
````````````````````````````````````````````````````

*New in version 0.3*

Let;s assume you manage permission by user levels: admin, staff and user.

.. code:: python
  
  @app.permission_check_handler
  def permission_check_handler (was, perms):
    claims = was.request.JWT
    if "err" in claims: 
      return claims ["err"]
    
    if not perms: 
      return # permit for anyone who is authorized
    if claims ["level"] == "admin":
      return # premit always
    if "admin" in perms:
      raise was.Error ("403 Permission Denied")
    if "staff" in prems and claims ["level"] != "staff":
        raise was.Error ("403 Permission Denied")
    
.. code:: python

  @app.route ("/animals/<id>")
  @app.permission_required ([], id = ["staff"])
  def animals (was, id = None):
      id = id or was.request.JWT ["userid"]
      
This resources required any permission for "/animals/" or "/animals/me". But '/animals/100' is required 'staff' permission. It may make permission control more simpler.

Also you can specify premissions per request methods.

.. code:: python

  @app.route ("/animals/<id>", methods = ["POST", "DELETE"])
  @app.permission_required (['user'], id = ["staff"], DELETE = ["admin"])
  def animals (was, id = None):
      id = id or was.request.JWT ["userid"]
      
This resources required 'user' permission for "/animals/" or "/animals/me". 
'/animals/100' is required 'staff' permission. It may make permission control more simpler.


Testpassing
`````````````````````````

Also you can test if user is valid,

.. code:: python
  
  def is_superuser (was):
    if was.user.username not in ('admin', 'root'):
      reutrn was.response ("403 Permission Denied")
  
  @app.testpass_required (is_superuser)
  def modify_profile (was):
    ...
    
The binded testpass_required function can return,

- True or None: continue request
- False: response 403 Permission Denied immediately
- Responsable object: response object immediately


Cross Site Request Forgery Token (CSRF Token)
------------------------------------------------

*New in skitai version 0.26.16*

At template, insert CSRF Token,

.. code:: html
  
  <form>
  {{ was.csrf_token_input }}
  ...
  </form>

then verify token like this,

.. code:: python

  @app.before_request
  def before_request (was):
    if was.request.args.get ("username"):
      if not was.csrf_verify ():
        return was.response ("400 Bad Request")


Making One-Time Token
--------------------------------------

*New in skitai version 0.26.17*

For creatiing onetime link url, you can convert your data to signatured token string.

Note: Like JWT token, this token contains data and decode easily, then you should not contain important information like password or PIN. This token just make sure contained data is not altered by comparing signature which is generated with your app scret key.  

.. code:: python
  
  @app.route ('/password-reset')
  def password_reset (was)
    if was.request.args ('username'):
      username = "hans"
      token = was.mkott (username, 3600, "pwrset") # valid within 1 hour 
      pw_reset_url = was.ab ('reset_password', token)
      # send email
      return was.render ('done.html')
     
    if was.request.args ('token'):
      username = was.deott (was.request.args ['token'])
      if not username:
        return was.response ('400 Bad Request')
      # processing password reset
      ...

If you want to expire token explicit, add session token key 

.. code:: python

  # valid within 1 hour and create session token named '_reset_token'
  token = was.mkott ("hans", 3600, 'rset')  
  >> kO6EYlNE2QLNnospJ+jjOMJjzbw?fXEAKFgGAAAAb2JqZWN0...

  username = was.deott (token)
  >> "hans"
  
  # if processing is done and for revoke token,
  was.rvott (token)
  

App Event Handling
---------------------

Most of Atila's event handlings are implemented with excellent `event-bus`_ library.

*New in skitai version 0.26.16*, *Availabe only on Python 3.5+*

.. code:: python

  import atila
  
  @app.on (atila.app_starting)
  def app_starting_handler (wasc):
    print ("I got it!")
  
  @app.on (atila.request_failed)
  def request_failed_handler (was, exc_info):
    print ("I got it!")
  
  @app.on (atila.template_rendering)
  def template_rendering_handler (was, template, params):
    print ("I got it!")

There're some app events.

- atila.app_starting: required (wasc)
- atila.app_started: required (wasc)
- atila.app_restarting: required (wasc)
- atila.app_restarted: required (wasc)
- atila.app_mounted: required (was)
- atila.app_unmounting: required (was)
- atila.request_failed: required ( was, exc_info)
- atila.request_success: required (was)
- atila.request_tearing_down: required (was)
- atila.request_starting: required (was)
- atila.request_finished: required (was)

.. _`event-bus`: https://pypi.python.org/pypi/event-bus


App Storage
----------------------------------------

*app.store* object is ditionary like object and provide thread-safe accessing.

It SHOULD be simple primitive value like string, int, float. About dictionary or class instances, It can't give no guarantee for thread-safe. 

.. code:: python

  def  (was, current_users):
    total = app.store.get ("total-user")
    app.store.set ("total-user", total + 1)
    ...


Inverval Base App Maintenancing
---------------------------------------------

If you need interval base maintaining jobs, 

.. code:: python

  app.config.maintain_interval = 10  # seconds
  app.store.set ("num-nodes", 0) # thread safe store
  
  @app.maintain
  def maintain_num_nodes (was, now, count):
  	...
  	num_nodes = was.getlu ("cluster.num-nodes")
  	if app.store ["num-nodes"] != num_nodes:
  	  app.store ["num-nodes"] = num_nodes
  	  app.broadcast ("cluster:num_nodes")

You can add multiple maintain jobs but maintain function names is SHOULD be unique.


Creating and Handling Custom Event
---------------------------------------

*Availabe only on Python 3.5+*

For creating custom event and event handler,

.. code:: python

  @app.on ("user-updated")
  def user_updated (was, user):
    ...

For emitting,

.. code:: python
    
  @app.route ('/users', methods = ["POST"])
  def users (was):
    args = was.request.json ()
    ...
    
    app.emit ("user-updated", args ['userid'])
    
    return ''

If event hasn't args, you can use `emit_after` decorator,

.. code:: python
    
  @app.route ('/users', methods = ["POST"])
  @app.emit_after ("user-updated")
  def users (was):
    args = was.request.json ()
    ...    
    return ''

Using this, you can build automatic excution chain,

.. code:: python
  
  @app.on ("photo-updated")
  def photo_updated (was):
    ...        
    
  @app.on ("user-updated")
  @app.emit_after ("photo-updated")
  def user_updated (was):
    ...        
      
  @app.route ('/users', methods = ["POST"])
  @app.emit_after ("user-updated")
  def users (was):
    args = was.request.json ()
    ...
    return ''


Cross App Communication & Accessing Resources
----------------------------------------------

Skitai prefer spliting apps to small microservices and mount them each. This feature make easy to move some of your mounted apps move to another machine. But this make difficult to communicate between apps. 

Here's some helpful solutions.


Accessing App Object Properties
`````````````````````````````````

*New in skitai version 0.26.7.2*

You can mount multiple app on Skitai, and maybe need to another app is mounted seperatly.

.. code:: python

  skitai.mount ("/", "main.py")
  skitai.mount ("/query", "search.py")

And you can access from filename of app from each apps,

.. code:: python

  search_app = was.apps ["search"]
  save_path = search_app.config.save_path  


URL Building for Resource Accessing
````````````````````````````````````

*New in skitai version 0.26.7.2*
  
If you mount multiple apps like this,

.. code:: python

  skitai.mount ("/", "main.py")
  skitai.mount ("/search", "search.py")

For building url in `main.py` app from a query function of `search.py` app, you should specify app file name with colon.

.. code:: python

  was.ab ('search:query', "Your Name") # returned '/search/query?q=Your%20Name'
  
And this is exactly same as,

  was.apps ["search"].build_url ("query", "Your Name")

But this is only functioning between apps are mounted within same host.


Custom Error Handling
``````````````````````````````````````````

*New in skitai version 0.26.7*

.. code:: python
  
  @app.default_error_handler
  def default_error_handler (was, error):
    return "<h1>{code} {message}</h1>".format (**error)

Or you can respond with JSON only.

.. code:: python

  @app.error_handler (404)
  def not_found (was, error):
    return "<h1>{code} {message}</h1>".format (**error)

- code: error code
- message: error message
- detail: error detail
- mode: debug or normal
- debug: debug info
- time: time when error occured
- url: request url
- software: server name and version
- traceback: available only if app.debug = True or None

Note that custom error templates can not be used before routing to the app.


Communication with Event
``````````````````````````

*New in skitai version 0.26.10*
*Availabe only on Python 3.5+*

'was' can work as an event bus using app.on_broadcast () - was.broadcast () pair. Let's assume that an users.py app handle only user data, and another photo.py app handle only photos of users.

.. code:: python

  skitai.mount ('/users', 'users.py')
  skitai.mount ('/photos', 'photos.py')

If a user update own profile, sometimes photo information should be updated.

At photos.py, you can prepare for listening to 'user:data-added' event and this event will be emited from 'was'.

.. code:: python
  
  @app.on_broadcast ('user:data-added')
  def refresh_user_cache (was, userid):
    was.sqlite3 ('@photodb').execute ('update ...').wait ()

and uses.py, you just emit 'user:data-added' event to 'was'.

.. code:: python
  
  @app.route ('/users', methods = ["PATCH"])
  def users (was):
    args = was.request.json ()
    was.sqlite3 ('@userdb').execute ('update ...').wait ()
    
    # broadcasting event to all mounted apps
    was.broadcast ('user:data-added', args ['userid'])
    
    return was.response (
      "200 OK", 
      json.dumps ({}), 
      [("Content-Type", "application/json")]
    )

If resource always broadcasts event without args, use `broadcast_after` decorator.

.. code:: python
  
  @app.broadcast_after ('some-event')
  def users (was):
    args = was.request.json ()
    was.sqlite3 ('@userdb').execute ('update ...').wait ()   

Note that this decorator cannot be routed by app.route ().


CORS (Cross Origin Resource Sharing) and Preflight
-----------------------------------------------------

For allowing CORS, you should do 2 things:

- set app.access_control_allow_origin
- allow OPTIONS methods for routing

.. code:: python
  
  app = Atila (__name__)
  app.access_control_allow_origin = ["*"]
  # OR specific origins
  app.access_control_allow_origin = ["http://www.skitai.com:5001"]
  app.access_control_max_age = 3600
  
  @app.route ("/post", methods = ["POST", "OPTIONS"])
  def post (was):
    args = was.request.json ()  
    return was.jstream ({...})  
    

If you want function specific CORS,

.. code:: python
  
  app = Atila (__name__)
  
  @app.route (
   "/post", methods = ["POST", "OPTIONS"], 
   access_control_allow_origin = ["http://www.skitai.com:5001"],
   access_control_max_age = 3600
  )
  def post (was):
    args = was.request.json ()  
    return was.jstream ({...})  


WWW-Authenticate
-------------------

*Changed in version 0.15.21*

  - removed app.user and app.password
  - add app.users object has get(username) methods like dictionary  

Atila provide simple authenticate for administration or perform access control from other system's call.

Authentication On Specific Methods
`````````````````````````````````````````

Otherwise you can make some routes requirigng authorization like this:

.. code:: python
  
  @app.route ("/hello/<name>", authenticate = "digest")
  def hello (was, name = "Hans Roh"):
    return "Hello, %s" % name

Or you can use @app.authorization_required decorator.
		
.. code:: python
  
  @app.route ("/hello/<name>")
  @app.authorization_required ("digest")
  def hello (was, name = "Hans Roh"):
    return "Hello, %s" % name

Available authorization methods are basic, digest and bearer. 
 

Password Provider
````````````````````

You can provide password and user information getter by 2 ways.

First, users object 

.. code:: python
  
  # users object shoukd have get(username) method
  app.users = {"hansroh": ("1234", False)}

Second, use decorator 

.. code:: python
  
  @app.authorization_handler
  def auth_handler (was, username):
    ...
    return ("1234", False)

The return object can be:

  - (str password, boolean encrypted, obj userinfo)
  - (str password, boolean encrypted)
  - str password
  - None if authorization failed

If you use encrypted password, you should use digest authorization and password should encrypt by this way:

.. code:: python
  
  from hashlib import md5
  
  encrypted_password = md5 (
    ("%s:%s:%s" % (username, realm, password)).encode ("utf8")
  ).hexdigest ()

    
If authorization is successful, app can access username and userinfo vi was.request.user.

  - was.request.user.name
  - was.request.user.realm
  - was.request.user.info

If your server run with SSL, you can use app.authorization = "basic", otherwise recommend using "digest" for your password safety.

Authentication On Entire App
```````````````````````````````

For your convinient, you can set authorization requirements to app level.

.. code:: python

  app = Atila (__name__)
  
  app.authenticate = "digest"
  app.realm = "Partner App Area of mysite.com"
  app.users = {"app": ("iamyourpartnerapp", 0, {'role': 'root'})}
  
  @app.route ("/hello/<name>")
  def hello (was, name = "Hans Roh"):
    return "Hello, %s" % name

If app.authenticate is set, all routes of app require authorization (default is False).


(JWT) Bearer Authorization
--------------------------------------

To making JWT token, your app need securekey.

.. code:: python
  
  app.securekey = '5b2c4f18-01fd-4b85-8cfa-01827878562f'

.. code:: python

  was.mkjwt ({"username": "hansroh", "exp": time.time () + 3600, ...})
  >> eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXV...

Note: was.dejwt (token) is also available.

Then client should add 'Authorization' to API request like,

.. code:: python

  Authorization: Bearer eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXV...

And use bearer_handler decorators.

.. code:: python
  
  @app.bearer_handler
  def bearer_handler (was, token):
    # if not JWT token,
    claims = parse_your_token_yourself (token)
    # if JWT, just use was.request.JWT
    claims = was.request.JWT
    if "err" in claims:
      return claims ["err"]
    
  @app.route ("/api/v1/predict")
  @app.authorization_required ("bearer")
  def predict (was):
    # now you can use these
    was.request.user # hansroh
    was.request.JWT # dict {"username": "hansroh", "exp": 2900...}

For your convinient, above bearer_handler is registered as default handler, but you can still override it.

Implementing XMLRPC Service
-----------------------------

Client Side:

.. code:: python

  import aquests
      
  stub = aquests.rpc ("http://127.0.0.1:5000/rpc")
  stub.add (10000, 5000)  
  fetchall ()
  
Server Side:

.. code:: python

  @app.route ("/add")
  def index (was, num1, num2):  
    return num1 + num2

Is there nothing to diffrence? Yes. Atila app methods are also used for XMLRPC service if return values are XMLRPC dumpable.


Implementing gRPC Service
-----------------------------

Client Side:

.. code:: python
  
  import aquests
  import route_guide_pb2
  
  stub = aquests.grpc ("http://127.0.0.1:5000/routeguide.RouteGuide")
  point = route_guide_pb2.Point (latitude=409146138, longitude=-746188906)
  stub.GetFeature (point)
  aquests.fetchall ()
  
Server Side:

.. code:: python
  
  import route_guide_pb2
  
  def get_feature (feature_db, point):
    for feature in feature_db:
      if feature.location == point:
        return feature
    return None
    
  @app.route ("/GetFeature")
  def GetFeature (was, point):
    feature = get_feature(db, point)
    if feature is None:
      return route_guide_pb2.Feature(name="", location=point)
    else:
      return feature

  if __name__ == "__main__":

  skitai.mount = ('/routeguide.RouteGuide', app)
  skitai.urn ()


For an example, here's my tfserver_ for Tensor Flow Model Server.
  
For more about gRPC and route_guide_pb2, go to `gRPC Basics - Python`_.

Note: I think I don't understand about gRPC's stream request and response. Does it means chatting style? Why does data stream has interval like GPS data be handled as stream type? If it is chat style stream, is it more efficient that use proto buffer on Websocket protocol? In this case, it is even possible collaborating between multiple gRPC clients.

.. _`gRPC Basics - Python`: http://www.grpc.io/docs/tutorials/basic/python.html
.. _tfserver: https://pypi.python.org/pypi/tfserver


Logging and Traceback
------------------------

.. code:: python
  
  @app.route ("/")
  def sum ():  
    was.log ("called index", "info")    
    try:
      ...
    except:  
      was.log ("exception occured", "error")
      was.traceback ()
    was.log ("done index", "info")

Note inspite of you do not handle exception, all app exceptions will be logged automatically by Atila. And it includes app importing and reloading exceptions.

- was.log (msg, category = "info")
- was.traceback (id = "") # id is used as fast searching log line for debug, if not given, id will be *Global transaction ID/Local transaction ID*

App Testing
---------------------------

For automated test, Atila provide test_client (). Test client will just emulate client-server communication. 

myapp.py is: 

.. code:: python

  app = Atila (__name__)
  
  @app.route ("/")
  def index (was):
    return "<h1>something</h1>"
  
  @app.route ("/apis/pets/<int:id>")  
  def pets (was, id):
    return was.API ({"id": id, "kind": "dog", "name": "Monk"})

  if __name__ == "__main__":
    skitai.mount ("/", app)
    skitai.run (port = 5000)
    
If you run unittest with pytest, your test script is like this.

.. code:: python

  def test_myapp (): 
    from myapp import app
  
    with app.test_client ("/", approot = ".") as cli:
      # html request
      resp = cli.get ("/")
      assert "something" in resp.text
      
      # api call
      stub = cli.api ()
      resp = stub.apis.pets (45).get ()
      assert resp.data ["id"] == 45
      
      resp = stub.apis.pets (100).get ()
      assert resp.data ["id"] == 100

Now run pytest.

Above code works fine if your app is composed with single file. If your app has sub modules, app will raise relative import related error.

..code:: python

  import skitai
  import atila

  def test_myapp ():
    pref = skitai.pref ()
    app = atila.load ("./mayapp/app.py", pref)

If your app is located as your module's export/skitai/__export__.py,

..code:: python
 
  import your_module
  app = atila.load (your_module, pref)

Now, you are ready to test.

Note: Internal requests like was.get, was.post, was.jsonrpc and database engine operations will work with synchronous mode and may will be slow.



VueJS with Skito-Atila
========================

I prefer to build VueJS as frontend app and Atila as backend.

Basic project directory stucture is,
 
project root

- frontend (vue project)

  * <dist>
  * <node_modules>
  * <src>
  * <public>  
  * package.json
  * vue.config.js
  * ...
   
- backend

  * <services>
  * serve.py
  
The core line sof serve.py,

.. code:: python

  from atila import Atila
  import skitai
  import os
  import sys
  from services import api
  
  app = Atila (__name__)
  app.mount ("/api/v1", api) # for backend API service
    
  @app.route ("/<path:path>")
  def vapp (was, path = None):
      return was.File (skitai.joinpath ("../frontend", "dist", "index.html"), "text/html")
  
  if __name__ == "__main__":    
      pref = skitai.pref ()
      pref.securekey = None
      pref.max_client_body_size = 2 << 32
      pref.access_control_allow_origin = ["127.0.0.1:5000"]
          
      if "---production" not in sys.argv:
          pref.debug = True
          pref.use_reloader = True        
          pref.access_control_allow_origin.append ("127.0.0.1:8080")
          
      skitai.mount ("/", app)    
      skitai.mount ("/", "../frontend/dist", pref = pref)
      skitai.run (name = "myapp", port = 5000)

This skitai starting script do these things,

- If requested URL is one of atila routes, then routed to it
- Otherwise all URL is routed to vue SPA (dist/index.html)
- All static root mounted to frontend/dist directory for service compiled js and css by webpack
  
You can develop vue app by,

.. code:: bash

  npm run serve
  # generally use port 8080

And Atila app developing by,
 
.. code:: bash

  python3 ../backend/serve.py
  # use port 5000

Finally,

.. code:: bash
  
  npm run build
  python3 ../backend/serve.py


If you interest about thi stuff, you can have reference_ which I personally build as bolier-plate. But it is just planning stage.

.. _reference: https://gitlab.com/hansroh/skito-vue



Working With Jinja2 Template Engine
==============================================================

If you want to use Jinja2 template engine, install first.

.. code:: bash

  pip3 install -U jinja2 

Although You can use any template engine, Skitai provides was.render() which uses Jinja2_ template engine. For providing arguments to Jinja2, use dictionary or keyword arguments.

.. code:: python
  
  return was.render ("index.html", choice = 2, product = "Apples")
  
  #is same with:
  
  return was.render ("index.html", {"choice": 2, "product": "Apples"})
  
  #BUT CAN'T:
  
  return was.render ("index.html", {"choice": 2}, product = "Apples")


Directory structure sould be:

- /project_home/app.py
- /project_home/templates/index.html


At template, you can use all 'was' objects anywhere defautly. Especially, Url/Form parameters also can be accessed via 'was.request.args'.

.. code:: html
  
  {{ was.cookie.username }} choices item {{ was.request.args.get ("choice", "N/A") }}.
  
  <a href="{{ was.ab ('checkout', choice) }}">Proceed</a>

Also 'was.g' is can be useful in case threr're lots of render parameters.

.. code:: python

  was.g.product = "Apple"
  was.g.howmany = 10
  
  return was.render ("index.html")

And at jinja2 template, 
  
.. code:: html
  
  {% set g = was.g }} {# make shortcut #}
  Checkout for {{ g.howmany }} {{ g.product }}{{g.howmany > 1 and "s" or ""}}
  

If you want modify Jinja2 envrionment, can through was.app.jinja_env object.

.. code:: python
  
  def generate_form_token ():
    ...
    
  was.app.jinja_env.globals['form_token'] = generate_form_token


*New in skitai version 0.15.16*

Added new app.jinja_overlay () for easy calling app.jinja_env.overlay ().

Recently JS HTML renderers like Vue.js, React.js have confilicts with default jinja mustache variable. In this case you mightbe need change it.

.. code:: python

  app = Atila (__name__)
  app.debug = True
  app.use_reloader = True
  app.jinja_overlay (
    variable_start_string = "{{", 
    variable_end_string = "}}", 
    block_start_string = "{%", 
    block_end_string = "%}",
    comment_start_string = "{#",
    comment_end_string = "#}",
    line_statement_prefix = "%",
    line_comment_prefix = "%%"
  )

if you set same start and end string, please note for escaping charcter, use double escape. for example '#', use '##' for escaping.

*Warning*: Current Jinja2 2.8 dose not support double escaping (##) but it will be applied to runtime patch by Atila. So if you use app.jinja_overlay, you have compatible problems with official Jinja2.

.. _Jinja2: http://jinja.pocoo.org/
.. _`Vue.js`: https://vuejs.org/

Using Skitai Async Requests Services Working With Jinja2 Template
--------------------------------------------------------------------------------------------------------

If you want to use Jinja2 template engine, install first.

.. code:: bash

  pip3 install -U jinja2
  
Basic usage is here_.

.. _here: https://pypi.org/project/skitai/#skitai-was-services

Async request's benefit will be maximied at your view template rather than your controller. At controller, you just fire your requests and get responses at your template.

.. code:: python

  @app.route ("/")
  @app.login_required
  def intro (was):
    was.g.aa = was.get ("https://example.com/blur/blur")
    was.g.bb = was.get ("https://example.com/blur/blur/more-blur")
    return was.render ('template.html')
	
Your template,

.. code:: html

  {% set response = was.g.aa.dispatch () %}  
  {% if response.status == 3 %}
    {{ was.response.throw ("500 Internal Server Error") }}
  {% endif %}
  
  {% if response.status_code == 200 %}
    {% for each in response.data %}
      ...
    {% endfor %}
  {% endif %}

*Available only with Atila*

Shorter version is for dispatch and throw HTTP error,

.. code:: html
  
  {% set response = was.g.aa.dispatch_or_throw ("500 Internal Server Error") %}


Registering Global Template Function
-------------------------------------------------------------

*New in skitai version 0.26.16*

template_global decorator makes a function possible to use in your template,

.. code:: python

  @app.template_global ("test_global")
  def test (was):  
    return ", ".join.(was.request.args.keys ())

At template,
    
.. code:: html

  {{ test_global () }}

Note that all template global function's first parameter should be *was*. But when calling, you SHOULDN't give *was*.


Registering Jinja2 Filter
--------------------------------------------------------------

*New in skitai version 0.26.16*

template_filter decorator makes a function possible to use in your template,

.. code:: python

  @app.template_filter ("reverse")
  def reverse_filter (s):  
    return s [::-1]

At template,
    
.. code:: html

  {{ "Hello" | reverse }}
    

Custom Error Template
--------------------------------------------------------------

*New in skitai version 0.26.7*

.. code:: python

  @app.default_error_handler
  def default_error_handler (was, error):
    return was.render ('default.htm', error = error)

  @app.error_handler (404)
  def not_found (was, error):
    return was.render ('404.htm', error = error)

Template file 404.html is like this:

.. code:: html

  <h1>{{ error.code }} {{ error.message }}</h1>  
  <p>{{ error.detail }}</p>
  <hr>
  <div>URL: {{ error.url }}</div>
  <div>Time: {{ error.time }}</div>  

Note that custom error templates can not be used before routing to the app.


Working With Django
===========================================

*New in skitai version 0.26.15*

I barely use Django, but recently I have opportunity using Django and it is very fantastic and especially impressive to Django Admin System.

Here are some examples collaborating with Djnago and Atila.

Before it begin, you should mount Django app,

.. code:: python
  
  # mount django app as backend app likely  
  pref = skitai.pref ()
  pref.use_reloader = True
  pref.use_debug = True
  
  skitai.mount ("/django", 'mydjangoapp/mydjangoapp/wsgi.py', 'application', pref)
  
  # main app
  skitai.mount ('/', 'app.py', 'app')
  skitai.run ()

When Django app is mounted, these will be processed.

1. add django project root path will be added to sys.path
2. app is mounted
3. database alias (@mydjangoapp) will be created as base name of django project root
 
FYI, you can access Django admin by /django/admin with default django setting.


Using Django Models
------------------------------------

You can use also Django models without mount app.

First of all, you should specify django setting with alias for django database engine.

.. code:: python

  skitai.alias ("@django", skitai.DJANGO, "myapp/settings.py")
  
Then call django.setup ()  and you can use your models,
  
.. code:: python
  
  import django
  django.setup () # should call  
  from mydjangoapp.photos import models

  @app,route ('/django/hello')
  def django_hello (was):
    models.Photo.objects.create (user='Hans Roh', title = 'My Photo') 
    result = models.Photo.filter (user='hansroh').order_by ('-create_at')

You can use Django Query Set as SQL generator for Skitai's asynchronous query execution. But it has some limitations.

- just vaild only select query and prefetch_related () will be ignored
- effetive only to PostgreSQL and SQLite3 (but SQLite3 dose not support asynchronous execution, so it is practically meaningless)

.. code:: python

  from mydjangoapp.photos import models

  @app,route ('/hello')
  def django_hello (was):    
    query = models.Photo.objects.filter (topic=1).order_by ('title')  
    return was.jstream (was.sqlite3 ("@entity").execute (query).getwait ().data, 'data')  


How To
================

Response All Errors As JSON
--------------------------------------

.. code:: python

  @app.default_error_handler
  def default_error_handler (was, error):
    code = error ["errno"] or str (error ["code"]) + '00'    
    return was.response.fault (
      error ["message"].lower (), code, None, 
      error ["detail"], exc_info = error ["traceback"]
    )


Links
======

- `GitLab Repository`_
- Bug Report: `GitLab issues`_

.. _`GitLab Repository`: https://gitlab.com/hansroh/atila
.. _`GitLab issues`: https://gitlab.com/hansroh/atila/issues


Change Log
===========

- 0.3 (Mar 13, 2019)

  - remove proxing django route
  - remove login service with django
  - remove django model signla redirecting  
  - add @app.test_params
  - change mount handler: def mount (app) => def __mount__ (app) but lower version compatible
  - make available @app.route ("")
  - add was.proxypass (alias, path, timeout = 3)
  - add special pre-defined URL parameter value: me, notme, new
  - add parameter validation, now response code 400, if validatiion if failed
  - fix implicit routing
  - add conditional permission control

- 0.2 (Feb 18, 2019)
  
  - fix implicit routing for root
  - remove jinja2 from requirements
  - add app.websocket_send ()
  - fix Futures respinse bugs
  - add was.API (), was.Fault (), was.File and was.Futures ()  
  
- 0.1 (Jan 17, 2019)
  
  - was.promise () has been deprecated, use was.Futures ()
  - add interval based maintain jobs executor
  - change name from app.storage to app.store
  - add default_bearer_handler
  - fix routing bugs related fancy URL
  - add was.request.URL, DEFAULT, FORM (former was.request.form ()), JSON (former was.request.json ()), DATA (former was.request.data), ARGS (former was.request.args)
  - add @app.test_param (required = None, ints = None, floats = None)  
  - project has been seperated from skitai and rename from saddle to atila, because saddle project is already exist on PYPI 
   
  

