from http import HTTPStatus

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URL_map
from .views import get_unique_short_id, is_busy_short_id, is_correct_short_id


@app.route('/api/id/', methods=['POST'])
def add_short():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    custom_id = data.get('custom_id', None)
    if custom_id:
        if is_busy_short_id(custom_id):
            raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
        if not is_correct_short_id(custom_id):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки')
    else:
        data['custom_id'] = get_unique_short_id()
    item = URL_map()
    item.from_dict(data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=['GET'])
def get_short(short_id):
    item = URL_map.query.filter_by(short=short_id).first()
    if item is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify(item.to_api_dict()), HTTPStatus.OK
