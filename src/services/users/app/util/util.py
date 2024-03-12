import hashlib
import time
from sqlalchemy.exc import OperationalError


def get_field(request, field, default=None):
    return request.json.get(field, default)


def password_hasher(username, password):
    m = hashlib.md5()
    m.update((username + password).encode())
    return m.hexdigest()


def connect_to_db(db, app, retries=10, delay=2):
    db.init_app(app)

    while retries > 0:
        try:
            with app.app_context():
                db.create_all()
            return
        except OperationalError as err:
            retries -= 1
            print('Could not connect to DB, retrying in', delay, 'seconds')
            time.sleep(delay)

    raise Exception('Can not connect to DB')
