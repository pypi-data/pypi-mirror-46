from .client import Client as _Client


bgc = _Client()
connections = bgc.extract_connections()


__all__ = [ 'bgc', 'connections' ]
