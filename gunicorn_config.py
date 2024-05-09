bind = '0.0.0.0:8000'
workers = 1
worker_class = 'uvicorn.workers.UvicornWorker'
loglevel = 'debug'
accesslog = './access_app.log'
acceslogformat = "%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog = './error_app.log'
