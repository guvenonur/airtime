from flask import Flask, render_template, request, send_from_directory, redirect
from db.operations import Operations
from notifier.crawler import Crawler
from notifier.email import Email
from notifier.preparations import Preparations
from db.tv_series import TvSeries
from celery import Celery

prep = Preparations()
cr = Crawler()
em = Email()
op = Operations()

app = Flask(__name__)
app.secret_key = 'random string'

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('static/images', path)


@celery.task()
def update_imdb():
    df = prep.get_imdb_data()
    op.insert(df=df, table='imdb_dataset', method='replace')


@app.route('/')
def home():
    update_imdb.apply_async()
    return render_template('index.html')


@app.route('/add_record', methods=['POST'])
def add_record():
    """
    Adding new record to tv_series

    :return:
    """
    try:
        name = request.form['name']
        season = request.form['season']
        episode = request.form['episode']

        df = prep.merge_entries(name, season, episode)
        op.insert(df, table='tv_series', method='append')

        return redirect('/list')

    except Exception as e:
        return render_template("index.html", error=str(e))


@app.route('/list')
def show_list():
    """

    :return:
    """
    try:
        rows = op.get_list()
        return render_template("list.html", rows=rows)

    except Exception as e:
        return render_template("list.html", rerror=str(e))


@app.route('/list/edit', methods=['GET'])
def get_list_edit():
    """
    Response when get request to history edit

    :return: return history if user logged in ago, else return sign in page
    :rtype: str(render_template) or werkzeug.wrappers.Response(redirect)
    """
    try:
        imdb_id = request.args['imdb_id']
        res = op.get_by_id(imdb_id=imdb_id)
        return render_template('edit.html', item=res, title='List', active=2)

    except Exception as e:
        return render_template("list.html", error=str(e))


@app.route('/edit', methods=['POST'])
def edit():
    """
    Edit operation in database

    :return:  status of edit operation
    :rtype: str
    """
    imdb_id = str(request.form['imdb_id'])

    try:
        season = request.form['season']
        episode = request.form['episode']

        record = TvSeries(imdb_id=str(imdb_id), season=season, episode=episode)
        op.update(record)

        return redirect('/list')
    except Exception as e:
        item = op.get_by_id(imdb_id)
        return render_template('edit.html', error=str(e), active=2, title='Edit', item=item)


@app.route('/delete', methods=['GET'])
def delete():
    """
    Delete operation in database

    :return:  status of delete operation
    :rtype: str
    """
    try:
        imdb_id = str(request.args['imdb_id'])
        op.delete_by_id(imdb_id)
        return redirect('/list')
    except Exception as e:
        return render_template('list.html', error=str(e))


@app.route('/send')
def enter_mail():
    return render_template('mail.html')


@app.route('/sendmail', methods=['POST', 'GET'])
def send_mail():
    try:
        df = op.get_dataframe()
        message = cr.crawl_airtimes(df=df)
        mail = request.form['mail']
        em.send_email(mail=mail, message=message)

        return redirect('/done')

    except Exception as e:
        return render_template("mail.html", error=str(e))


@app.route('/done')
def final_page():
    return render_template("done.html")


if __name__ == '__main__':
    app.run(debug=True)
