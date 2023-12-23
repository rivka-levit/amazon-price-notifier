from flask import Flask, render_template, request, redirect, url_for

from utils.watcher import AmazonPriceWatcher

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        product_url = request.form.get('product')
        watcher = AmazonPriceWatcher(product_url)
        watcher.watch()

        return redirect(url_for('started'))


@app.route('/started')
def started():
    return render_template('started.html')


if __name__ == '__main__':
    app.run()
