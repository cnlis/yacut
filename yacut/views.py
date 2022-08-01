import string
from http import HTTPStatus
from random import randrange

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import MainForm
from .models import URL_map


def is_correct_short_id(short_id):
    return (isinstance(short_id, str) and len(short_id) <= 16 and
            short_id.isalnum() and short_id.isascii())


def is_busy_short_id(short_id):
    return URL_map.query.filter_by(short=short_id).first() is not None


def get_unique_short_id():
    chars = string.digits + string.ascii_letters
    chars_len = len(chars)
    while True:
        result = ''.join(chars[randrange(chars_len)] for _ in range(6))
        if not is_busy_short_id(result):
            return result


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = MainForm()
    if form.validate_on_submit():
        short_id = form.custom_id.data
        if short_id:
            if is_busy_short_id(short_id):
                flash(f'Имя {short_id} уже занято!', category='message')
                return render_template('index.html', form=form)
            if not is_correct_short_id(short_id):
                flash('Некорректное имя ссылки!', category='message')
                return render_template('index.html', form=form)
        else:
            short_id = get_unique_short_id()
        item = URL_map(
            original=form.original_link.data,
            short=short_id
        )
        db.session.add(item)
        db.session.commit()
        flash('Ваша новая ссылка готова:', category='message')
        flash(short_id, category='short_id')
    return render_template('index.html', form=form)


@app.route('/<string:short_id>')
def redirect_view(short_id):
    item = URL_map.query.filter_by(short=short_id).first()
    if item is not None:
        if 'http://' not in item.original and 'https://' not in item.original:
            return redirect('http://' + item.original)
        return redirect(item.original)
    abort(HTTPStatus.NOT_FOUND)
