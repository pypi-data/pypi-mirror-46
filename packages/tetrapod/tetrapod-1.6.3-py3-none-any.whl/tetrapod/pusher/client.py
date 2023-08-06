import pusher
from mudskipper import Client as Client_base
from mudskipper.connection import Connections_base
import logging


logger = logging.getLogger( 'tetrapod.pusher' )


class Connections( Connections_base ):
    def build_client( self, alias ):
        connection = self[ alias ]
        client = pusher.Pusher(
            app_id=connection[ 'app_id' ],
            key=connection[ 'key' ],
            secret=connection[ 'secret' ],
            cluster=connection[ 'cluster' ] )
        return client


class Client( Client_base ):
    """
    pusher client

    Notes
    =====
    `online doc <https://pusher.com/docs/server_api_guide>`_
    """
    def __init__( self, *args, channels=None, **kw ):
        self._channels = channels
        super().__init__( *args, **kw )

    def trigger( self, event, payload=None, **kw ):
        """
        thigger a envent in the channels of the client
        """
        if self.is_test_mode:
            result = {}
        else:
            result = self._client.trigger( self._channels, event, payload, )
        logger.info( 'pusher event', extra={ 'pusher': { 'event': event } } )
        return result

    def channel( self, channels ):
        return self.__class__(
            self._default_connection_name,
            _connections=self._connections, channels=channels )

    def using( self, name ):
        return self.__class__(
            name, _connections=self._connections, channels=self._channels )

    @property
    def _client( self ):
        client = self._connections.build_client(
            self._default_connection_name )
        return client

    def build_connection( self ):
        return Connections()

    @property
    def is_test_mode( self ):
        return self.get_connection().get( 'test_mode', False )
