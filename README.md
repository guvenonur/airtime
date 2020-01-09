# Airtime Notifier

Log where you left your favorite tv shows and this project will crawl the airtimes to notify you via email.

## Installation

```git clone https://github.com/guvenonur/airtime.git```

```pip install -r requirements.txt ```

### Getting Started

First, create sqlite db once by running:

```
python3 db/imdb_dataset.py
```

Now you can either use supervisord or three terminal windows.

#### Option 1: Terminals
First Window: Run redis-server for celery backend
```
redis-server
```
Second Window: Run main.py
```
python main.py config.ini
```

Third Window: Run celery worker
```
celery -A main.celery worker
```
#### Option 2: Supervisor
Run supervisor using supervisord.conf
```
supervisord -c supervisord.conf
```

### Test
Check http://localhost:5000/

And, you can use flower to check celery tasks with:

```
celery flower -A main.celery --address=127.0.0.1 --port=5555
```
Now you can check http://localhost:5555/ to monitor celery tasks.

## Acknowledgments
* Big shout out to all my colleagues for helping and guiding me through it all, especially Egemen Zeytinci and Tarık Yılmaz.
