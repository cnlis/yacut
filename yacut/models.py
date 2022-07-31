from datetime import datetime

from flask import url_for

from yacut import db


class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), nullable=False, unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            short_link=url_for(
                'redirect_view', short_id=self.short, _external=True
            ),
            url=self.original,
        )

    # для прохождения тестов
    def to_api_dict(self):
        return dict(url=self.original)

    def from_dict(self, data):
        self.original = data.get('url')
        self.short = data.get('custom_id')
