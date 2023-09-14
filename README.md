# CHATWIZ API

## Run celery
Navigate to llm/tasks folder and execute:
```bash
celery -A chatwiztasks worker -Q chatwiztasks_queue --loglevel=INFO --hostname=chatwiz --autoscale=2,1
```


## Run API
Navigate to project root and execute:
```bash
uvicorn app.main:app --host 0.0.0.0
```
