import time
import threading

from flask import Flask, render_template, request, redirect, url_for

from utils.watcher import AmazonPriceWatcher


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':

        def do_watching(product_url: str) -> None:
            """Create and run the watcher."""

            watcher = AmazonPriceWatcher(product_url)
            watcher.watch()

        # Create new thread and run the do_watching() function there.

        thread = WatchThread(
            target=do_watching,
            kwargs={'product_url': request.form.get('product')}
        )
        thread.start()
        time.sleep(1)

        # Check if an error has been stored in messages.

        if thread.messages:
            messages = thread.messages
            thread.messages = None

            return redirect(url_for('error', messages=messages))

        return redirect(url_for('started'))


@app.route('/started')
def started():
    """Return success page after the watching process has been started."""

    return render_template('started.html')


@app.route('/error')
def error():
    """Return error page if an error occurs."""

    messages = request.args.get('messages')

    return render_template('error.html', messages=messages)


class WatchThread(threading.Thread):
    """Custom Thread to catch error messages from a separate thread."""

    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super().__init__(group=group, target=target, name=name,
                         args=args, kwargs=kwargs, daemon=daemon)
        self.messages = None

    def run(self):
        """Override run method to handle error messages."""

        try:
            super().run()
        except ValueError as e:
            self.messages = str(e)
        except Exception as e:
            self.messages = str(e)
