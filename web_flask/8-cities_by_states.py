#!/usr/bin/python3
"""Flask app, fetching data from storage with relationship
"""

from models import storage
from models.state import State
from flask import Flask, render_template
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/cities_by_states')
def states_list():
    """Return cities by states
    """
    path = '8-cities_by_states.html'
    states = storage.all(State)

    return render_template(path, states=states)


@app.teardown_appcontext
def app_teardown(arg=None):
    """Clean-up session
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
