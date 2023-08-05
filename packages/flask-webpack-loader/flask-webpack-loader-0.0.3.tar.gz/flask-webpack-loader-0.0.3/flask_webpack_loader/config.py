import re
import os


__all__ = ('DEFAULT_CONFIG',)


DEFAULT_CONFIG = {
    'CACHE': True,
    'BUNDLE_DIR_NAME': os.path.join('static', 'bundles'),
    'STATIC_URL': 'static',
    'STATS_FILE': 'webpack-stats.json',
    # FIXME: Explore usage of fsnotify
    'POLL_INTERVAL': 0.1,
    'TIMEOUT': None,
    'IGNORES': [re.compile(r'.+\.hot-update.js'), re.compile(r'.+\.map')]
}

