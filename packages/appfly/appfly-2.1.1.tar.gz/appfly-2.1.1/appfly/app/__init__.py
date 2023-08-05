import json
from flask import Flask, request
from deeptracepy import DeepTrace
from appfly.app.routes import ping
from flask_socketio import SocketIO
from flask_cors import CORS, cross_origin

cors_default = {
        "api/ping": {"origins": "*"}
}

app = None
socketio = None

def add_event(name, event, namespace):
    """ Add an socket event on the global sockeio instance
        Params:
            name: The event name;
            event: Event method;
            namespace: method namespace
    """
    global socketio
    socketio.on_event(name, event, namespace=namespace)

def add_url(url, route, method):
    """ Add an url to global flask app instance
        Params: 
            url: url, example: /your/route
            route: route that will receive/handle the request
            method: http verb [GET, POST, PUT, DELETE...]
    """
    global app
    len_urls = len(list(app.url_map.iter_rules()))
    app.add_url_rule("/api"+url, url[1:], route, methods=[method])
    # app.add_url_rule("/api"+url, "url_{}".format(len_urls), route, methods=[method])

def factory(fn, app_name, config={}):
    """ Create a flask/sockeio app instance and set some default configs
        Params:
            fn:
            name:
            cors:
            templete_folder:
            has_socket:
    """
    global app, socketio
    app = Flask(app_name)
    CORS(app, resources={json.dumps(cors_default)})
    # TODO: verify all parameters that flask accept and make
    # a loop to verify if the user wanna use some one of this parameters
    if 'template_folder' in config:
        app.template_folder = config['template_folder']
    if 'has_socket' in config: 
        socketio = SocketIO(app) #TODO: verify if it is a socket instance by other away
    if 'cors' in config:
        CORS(app, resources=json.dumps({**config['cors'], **cors_default})) 

    add_url("/ping", ping.route, "GET")  
    fn(app, config)
    
    @app.after_request
    def after_request(response):
       if 'deeptrace' in config:
        dt = DeepTrace(config['deeptrace'])
        dt.handle(request, response)
       return response
    
print('API is running...')
