from mudskipper.endpoint import Endpoint as Endpoint_base, GET, POST
from tetrapod.laniidae.response import (
    User_detail as User_detail_response, User_list, Token_list, Package_list,
    Profile_detail as Profile_detail_response,
)
from urllib.parse import urljoin
from .exceptions import Laniidae_exception


class Endpoint( Endpoint_base ):
    def __init__( self, *args, headers=None, **kw ):
        if headers is None:
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        else:
            headers.update( {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            } )
        super().__init__( *args, headers=headers, **kw )


class Users( Endpoint, GET, POST ):
    url = 'https://laniidae.com/users/'

    def build_response( self, response, method ):
        if method == 'post':
            if response.status_code == 201:
                params = vars( self )()
                url = response.headers[ 'Location' ]
                params[ 'url' ] = url
                return User_detail( **params, from_endpoint=self )
            else:
                raise Laniidae_exception(
                    status_code=response.status_code,
                    body=response.text )
        return User_list( response, from_endpoint=self )


class User_detail( Endpoint, GET ):
    url = 'https://laniidae.com/users/{user_id}/'

    @property
    def token( self ):
        params = vars( self )()
        url = urljoin( self.format_url, 'token' )
        params[ 'url' ] = url
        return Token( **params )

    def build_response( self, response, method ):
        return User_detail_response( response, from_endpoint=self )


class Token( Endpoint, GET ):
    def build_response( self, response, method ):
        return Token_list( response, from_endpoint=self )


class Package( Endpoint, GET ):
    url = 'https://laniidae.com/packages/'

    def build_response( self, response, method ):
        return Package_list( response, from_endpoint=self )


class Package_check( Endpoint, POST ):
    url = 'https://laniidae.com/packages/{pk}/check/'

    def build_response( self, response, method ):
        if method == 'post':
            if response.status_code == 201:
                params = vars( self )()
                url = response.headers[ 'Location' ]
                params[ 'url' ] = url
                return Profile_detail( **params, from_endpoint=self )
            else:
                raise Laniidae_exception(
                    status_code=response.status_code,
                    body=response.text )


class Profile_detail( Endpoint, GET ):
    url = 'https://laniidae.com/packages/{pk}/check/'

    def build_response( self, response, method ):
        return Profile_detail_response( response, from_endpoint=self )
