#!/usr/bin/python3
"""Starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
import models

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Displays 'Hello HBNB!'"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Displays 'HBNB'"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """Replace underscores with spaces in text"""
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route('/python/', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is_cool'):
    """Replace underscores with spaces in text"""
    text = text.replace('_', ' ')
    return "Python {}".format(text)


@app.route('/number/<int:n>', strict_slashes=False)
def number(n):
    """Displays 'n is a number' if n is an integer"""
    return "{} is a number".format(n)


@app.route('/number_template/<int:n>', strict_slashes=False)
def num_template(n=None):
    """Displays a HTML page only if n is an integer"""
    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def odd_or_even(n):
    """Displays a HTML page only if n is an integer"""
    parity = 'even' if n % 2 == 0 else 'odd'
    return render_template('6-number_odd_or_even.html', n=n, parity=parity)


@app.route('/states', strict_slashes=False)
@app.route('/states_list', strict_slashes=False)
def states_list():
    """Display a HTML page of the States"""
    states = storage.all(State)
    return render_template('7-states_list.html', states=states)


@app.route('/cities_by_states', strict_slashes=False)
def states_cities():
    """Display a HTML page of the States"""
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.route('/states/<string:id>', strict_slashes=False)
def state_id(id=None):
    """Display a HTML page of the cities of a state"""
    states = storage.all(State).get('State.{}'.format(id))
    return render_template('9-states.html', states=states)


@app.route('/hbnb_filters', strict_slashes=False)
def hbnb_filters():
    """Display a HTML page"""
    st = storage.all(State)
    am=storage.all(Amenity)
    return render_template('10-hbnb_filters.html', states=st, amenities=am)


@app.teardown_appcontext
def teardown_db(error):
    """Closes the database again at the end of the request."""
    storage.close()


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
