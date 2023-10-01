bind = '127.0.0.1:8000'
workers = 1
worker_class = 'uvicorn.workers.UvicornWorker'
loglevel = 'debug'
# FIXME: Change abs path
accesslog = '/home/bush/project/chatwiz/chatwiz_api/logs/access_app.log'
acceslogformat ="%(h)s %(l)s %(u)s %(t)s %(r)s %(s)s %(b)s %(f)s %(a)s"
errorlog =  '/home/bush/project/chatwiz/chatwiz_api/logs/app.log'
