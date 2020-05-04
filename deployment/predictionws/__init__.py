import logging
import sys

import flask

__version__ = '0.0.1'


def create_app():
    app = flask.Flask(import_name=__name__)

    app.config.from_pyfile(filename='config.py')

    level = app.config['LOGGING_LEVEL']
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stderr)

    import predictionws.views as views
    app.register_blueprint(blueprint=views.model_bp)
    app.register_blueprint(blueprint=views.prediction_bp)

    import predictionws.db as db
    app.teardown_appcontext(db.teardown_db)

    import predictionws.warehouse as wh
    app.teardown_appcontext(wh.teardown_warehouse)

    return app
