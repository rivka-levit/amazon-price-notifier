from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        return redirect('started.html')


@app.route('/started.html')
def started():
    return render_template('started.html')


if __name__ == '__main__':
    app.run()
