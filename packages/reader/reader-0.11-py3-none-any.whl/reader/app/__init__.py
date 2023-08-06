import json
import contextlib

from flask import Flask, Blueprint, current_app, g, request, abort
from flask import Response, stream_with_context
import humanize

from reader import Reader, ReaderError
from .api_thing import APIThing, APIError
from reader.plugins import Loader, LoaderError


blueprint = Blueprint('reader', __name__)

blueprint.app_template_filter('humanize_naturaltime')(humanize.naturaltime)


def get_reader():
    if not hasattr(g, 'reader'):
        reader = Reader(current_app.config['READER_DB'])
        current_app.reader_load_plugins(reader)
        g.reader = reader
    return g.reader

def close_db(error):
    if hasattr(g, 'reader'):
        # TODO: Expose "closing" the storage in the Reader API.
        g.reader._storage.db.close()


def stream_template(template_name_or_list, **kwargs):
    template = current_app.jinja_env.get_template(template_name_or_list)
    stream = template.stream(**kwargs)
    stream.enable_buffering(50)
    return Response(stream_with_context(stream))


@blueprint.route('/')
def entries():
    show = request.args.get('show', 'unread')
    assert show in ('all', 'read', 'unread')

    has_enclosures = request.args.get('has-enclosures')
    has_enclosures = {None: None, 'no': False, 'yes': True}[has_enclosures]

    reader = get_reader()

    feed_url = request.args.get('feed')
    feed = None
    if feed_url:
        feed = reader.get_feed(feed_url)
        if not feed:
            abort(404)

    entries = list(reader.get_entries(which=show, feed=feed_url, has_enclosures=has_enclosures))

    entries_data = None
    if feed_url:
        entries_data = [e.id for e in entries]

    return stream_template('entries.html', entries=entries, feed=feed, entries_data=entries_data)


@blueprint.route('/feeds')
def feeds():
    sort = request.args.get('sort', 'title')
    assert sort in ('title', 'added')

    feeds = get_reader().get_feeds(sort=sort)
    return stream_template('feeds.html', feeds=feeds)


@blueprint.route('/metadata')
def metadata():
    reader = get_reader()

    feed_url = request.args['feed']
    feed = reader.get_feed(feed_url)
    if not feed:
        abort(404)

    metadata = reader.iter_feed_metadata(feed_url)

    return stream_template('metadata.html', feed=feed, metadata=metadata)


form_api = APIThing(blueprint, '/form-api', 'form_api')


@contextlib.contextmanager
def readererror_to_apierror(*args):
    try:
        yield
    except ReaderError as e:
        category = None
        if hasattr(e, 'url'):
            category = (e.url, )
            if hasattr(e, 'id'):
                category += (e.id, )
        raise APIError(str(e), category)


@form_api
@readererror_to_apierror()
def mark_as_read(data):
    feed_url = data['feed-url']
    entry_id = data['entry-id']
    get_reader().mark_as_read((feed_url, entry_id))


@form_api
@readererror_to_apierror()
def mark_as_unread(data):
    feed_url = data['feed-url']
    entry_id = data['entry-id']
    get_reader().mark_as_unread((feed_url, entry_id))


@form_api(really=True)
@readererror_to_apierror()
def mark_all_as_read(data):
    feed_url = data['feed-url']
    entry_id = json.loads(data['entry-id'])
    for entry_id in entry_id:
        get_reader().mark_as_read((feed_url, entry_id))


@form_api(really=True)
@readererror_to_apierror()
def mark_all_as_unread(data):
    feed_url = data['feed-url']
    entry_id = json.loads(data['entry-id'])
    for entry_id in entry_id:
        get_reader().mark_as_unread((feed_url, entry_id))


@form_api(really=True)
@readererror_to_apierror()
def delete_feed(data):
    feed_url = data['feed-url']
    get_reader().remove_feed(feed_url)


@form_api
@readererror_to_apierror()
def add_feed(data):
    feed_url = data['feed-url'].strip()
    assert feed_url, "feed-url cannot be empty"
    # TODO: handle FeedExistsError
    get_reader().add_feed(feed_url)


@form_api
@readererror_to_apierror()
def update_feed_title(data):
    feed_url = data['feed-url']
    feed_title = data['feed-title'].strip() or None
    get_reader().set_feed_user_title(feed_url, feed_title)


@form_api
@readererror_to_apierror()
def add_metadata(data):
    feed_url = data['feed-url']
    key = data['key']
    get_reader().set_feed_metadata(feed_url, key, None)

@form_api
@readererror_to_apierror()
def update_metadata(data):
    feed_url = data['feed-url']
    key = data['key']
    try:
        value = json.loads(data['value'])
    except json.JSONDecodeError as e:
        raise APIError("invalid JSON: {}".format(e), (feed_url, key))
    get_reader().set_feed_metadata(feed_url, key, value)

@form_api
@readererror_to_apierror()
def delete_metadata(data):
    feed_url = data['feed-url']
    key = data['key']
    get_reader().delete_feed_metadata(feed_url, key)



class FlaskPluginLoader(Loader):

    def handle_error(self, exception, cause):
        current_app.logger.exception(
            "%s; original traceback follows",
            exception, exc_info=cause or exception)


def create_app(db_path, plugins=()):
    app = Flask(__name__)
    app.config['READER_DB'] = db_path

    try:
        app.reader_load_plugins = FlaskPluginLoader(plugins).load_plugins
    except LoaderError as e:
        app.logger.exception("%s; original traceback follows", e, exc_info=e.__cause__ or e)
        app.reader_load_plugins = lambda reader: reader

    app.secret_key = 'secret'
    app.teardown_appcontext(close_db)

    from .enclosure_tags import enclosure_tags_blueprint, enclosure_tags_filter
    try:
        import mutagen
        import requests
        app.register_blueprint(enclosure_tags_blueprint)
    except ImportError:
        pass
    blueprint.app_template_filter('enclosure_tags')(enclosure_tags_filter)

    app.register_blueprint(blueprint)
    return app

