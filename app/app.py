from flask import (Flask, render_template, request, redirect, url_for)
from threading import Thread

from utils.watcher import AmazonPriceWatcher

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        def do_watching(product_url: str):
            watcher = AmazonPriceWatcher(product_url)
            watcher.watch()

        thread = Thread(
            target=do_watching,
            kwargs={'product_url': request.form.get('product')}
        )
        thread.start()

        return redirect(url_for('started'))


@app.route('/started')
def started():
    return render_template('started.html')
