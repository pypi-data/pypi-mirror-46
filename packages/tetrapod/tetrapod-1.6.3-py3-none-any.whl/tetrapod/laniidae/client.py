import copy

from mudskipper import Client as Client_base
from mudskipper.connection import Connections as Connections_base

from tetrapod.laniidae.endpoints import Users, Package, Profile_detail


class Connections( Connections_base ):
    def __init__( self, *args, **kw ):
        self._f = None
        super().__init__( *args, **kw )

    def get( self, alias='default' ):
        if isinstance( alias, str ):
            return super().get( alias )
        else:
            if self._f is None or not callable( self._f ):
                raise NotImplementedError(
                    'you should add the lamdba for extract the '
                    'tokens using the funcion of "set_alias_lambda"' )
            token = self._f( alias )
            copy_of_default = copy.deepcopy( self.get( 'default' ) )
            copy_of_default[ 'token' ] = token
            self.add( alias, copy_of_default )
            return copy_of_default

    def set_alias_lambda( self, f ):
        self._f = f


class Client( Client_base ):
    def create_user(
            self, *, user_name, password, email,
            first_name, last_name, is_superuser=False, is_staff=False,
            partner_name, webhook_url ):
        data = dict(
            username=user_name, password=password, email=email,
            first_name=first_name, last_name=last_name,
            is_superuser=is_superuser, is_staff=is_staff,
            partners=[ { 'name': partner_name } ],
            hookshot={ 'url': webhook_url },
        )
        endpoint = Users(
            host=self.host, headers=self.headers, schema=self.schema )
        return endpoint.post( data )

    def package( self, *args, **kw ):
        endpoint = Package(
            host=self.host, headers=self.headers, schema=self.schema )
        return endpoint.get( **kw )

    def profile( self, *args, **kw ):
        if 'url' in kw:
            endpoint = Profile_detail(
                host=self.host, headers=self.headers, schema=self.schema,
                url=kw[ 'url' ] )
            return endpoint.get()
        raise NotImplementedError

    @property
    def headers( self ):
        connection = self.get_connection()
        if 'token' not in connection:
            return {}
        else:
            return {
                'Authorization': 'Token {}'.format( connection[ 'token' ] )
            }

    @property
    def host( self ):
        connection = self.get_connection()
        return connection[ 'host' ]

    @property
    def schema( self ):
        connection = self.get_connection()
        return connection.get( 'schema', 'https' )

    def build_connection( self ):
        return Connections()
