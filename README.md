# CHATWIZ API

## Run celery
Navigate to llm/tasks folder and execute:
celery -A chatwiztasks worker -Q chatwiztasks_queue --loglevel=INFO --hostname=chatwiz --autoscale=2,1


## Run API
Navigate to project root and execute:
uvicorn app.main:app --host 0.0.0.0