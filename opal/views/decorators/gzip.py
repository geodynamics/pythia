"Decorator for views that gzips pages if the client supports it."

from opal.utils.decorators import decorator_from_middleware
from opal.middleware.gzip import GZipMiddleware

gzip_page = decorator_from_middleware(GZipMiddleware)
