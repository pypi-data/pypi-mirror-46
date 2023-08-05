import json
import time
from io import open

from .exceptions import (
    WebpackError,
    WebpackLoaderBadStatsError,
    WebpackLoaderTimeoutError,
    WebpackBundleLookupError
)
from .config import DEFAULT_CONFIG


class WebpackLoader(object):

    def __init__(self, app=None):
        self.app = app
        self.config = DEFAULT_CONFIG
        self.assets = {}

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        :param app: Flask application
        :return: None
        """
        self.config = app.config.get('WEBPACK_LOADER') or self.config
        self.config['CACHE'] = app.config.get('DEBUG', True)

        app.add_template_global(self.render_bundle)
        app.add_template_global(self.render_static)

    @staticmethod
    def _filter_by_extension(bundle, extension):
        """Return only files with the given extension"""
        for chunk in bundle:
            if chunk['name'].endswith('.{0}'.format(extension)):
                yield chunk

    def _get_bundle(self, bundle_name, extension):
        bundle = self.get_bundle(bundle_name)
        if extension:
            bundle = self._filter_by_extension(bundle, extension)
        return bundle

    def get_files(self, bundle_name, extension=None):
        """Returns list of chunks from named bundle"""
        return list(self._get_bundle(bundle_name, extension))

    def render_bundle(self, bundle_name, extension=None, attrs=''):
        """
        Get a list of formatted <script> & <link> tags for the assets in the
        named bundle.
        :param bundle_name: The name of the bundle
        :param extension: (optional) filter by extension, eg. 'js' or 'css'
        :param attrs: attrs
        :return: a list of formatted tags as strings
        """

        bundle = self._get_bundle(bundle_name, extension)
        tags = []
        for chunk in bundle:
            if chunk['name'].endswith(('.js', '.js.gz')):
                tags.append(
                    (
                        '<script type="text/javascript" src="{0}" {1}></script>'
                    ).format(chunk['url'], attrs)
                )
            elif chunk['name'].endswith(('.css', '.css.gz')):
                tags.append(
                    (
                        '<link type="text/css" href="{0}" rel="stylesheet" {1}/>'
                    ).format(chunk['url'], attrs)
                )
        return '\n'.join(tags)

    def render_static(self, asset_name):
        """
        :param asset_name: the name of the asset
        :return: path to webpack asset as a string
        """
        return "{0}{1}".format(
           self.get_assets().get('publicPath', self.config['STATIC_URL']),
           asset_name
        )

    def _load_assets(self):
        try:
            with open(self.config['STATS_FILE'], encoding="utf-8") as f:
                return json.load(f)
        except IOError:
            raise IOError(
                'Error reading {0}. Are you sure webpack has generated '
                'the file and the path is correct?'.format(
                    self.config['STATS_FILE']))

    def get_assets(self):
        if self.config['CACHE']:
            if not self.assets:
                self.assets = self._load_assets()
            return self.assets
        return self._load_assets()

    def filter_chunks(self, chunks):
        for chunk in chunks:
            ignore = any(regex.match(chunk['name']) for regex in self.config.get('IGNORES', []))
            if not ignore:
                chunk['url'] = self.get_chunk_url(chunk)
                yield chunk

    def get_chunk_url(self, chunk):
        public_path = chunk.get('publicPath')
        if public_path:
            return public_path

        return '{0}{1}'.format(self.config['BUNDLE_DIR_NAME'], chunk['name'])

    def get_bundle(self, bundle_name):
        assets = self.get_assets()

        # poll when debugging and block request until bundle is compiled
        # or the build times out
        if self.app.config.get('DEBUG', False):
            timeout = self.config['TIMEOUT'] or 0
            timed_out = False
            start = time.time()
            while assets['status'] == 'compiling' and not timed_out:
                time.sleep(self.config['POLL_INTERVAL'])
                if timeout and (time.time() - timeout > start):
                    timed_out = True
                assets = self.get_assets()

            if timed_out:
                raise WebpackLoaderTimeoutError(
                    "Timed Out. Bundle `{0}` took more than {1} seconds "
                    "to compile.".format(bundle_name, timeout)
                )

        if assets.get('status') == 'done':
            chunks = assets['chunks'].get(bundle_name, None)
            if chunks is None:
                raise WebpackBundleLookupError('Cannot resolve bundle {0}.'.format(bundle_name))
            return self.filter_chunks(chunks)

        elif assets.get('status') == 'error':
            if 'file' not in assets:
                assets['file'] = ''
            if 'error' not in assets:
                assets['error'] = 'Unknown Error'
            if 'message' not in assets:
                assets['message'] = ''
            error = u"""{error} in {file} {message}""".format(**assets)
            raise WebpackError(error)

        raise WebpackLoaderBadStatsError(
            "The stats file does not contain valid data. Make sure "
            "webpack-bundle-tracker plugin is enabled and try to run "
            "webpack again."
        )
