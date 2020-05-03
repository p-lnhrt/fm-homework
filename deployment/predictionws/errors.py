import flask

errors_bp = flask.Blueprint(name='errors', import_name=__name__)


@errors_bp.errorhandler(404)
def resource_not_found(error):
    print(error)
    return flask.make_response(flask.jsonify({'error': 'Resource not found'}), 404)
