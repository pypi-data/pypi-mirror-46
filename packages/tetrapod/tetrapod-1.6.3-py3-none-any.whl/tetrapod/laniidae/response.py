from chibi.atlas import Chibi_atlas
from mudskipper.endpoint import Response


class User_list( Response ):
    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            from tetrapod.laniidae.endpoints import User_detail
            raw_list = self._response.json()
            self._native = []
            for u in raw_list:
                user = Chibi_atlas( u )
                if self.from_endpoint:
                    params = vars( self.from_endpoint )()
                    params.pop( 'url', None )
                    user.detail = User_detail( pk=user.pk, **params )

                self._native.append( user )
            return self._native


class User_detail( Response ):
    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            raw_data = self._response.json()
            self._native = Chibi_atlas( raw_data )
            return self._native


class Token_list( Response ):
    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            raw_list = self._response.json()
            self._native = []
            for u in raw_list:
                user = Chibi_atlas( u )
                self._native.append( user )
            return self._native


class Package_list( Response ):
    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            from tetrapod.laniidae.endpoints import Package_check
            raw_list = self._response.json()
            self._native = []
            for u in raw_list:
                user = Chibi_atlas( u )
                if self.from_endpoint:
                    params = vars( self.from_endpoint )()
                    params.pop( 'url', None )
                    user.check = Package_check( pk=user.pk, **params )
                self._native.append( user )
            return self._native


class Package_detail( Response ):
    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            raw_data = self._response.json()
            self._native = Chibi_atlas( raw_data )
            return self._native


class Profile_detail( Response ):
    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            raw_data = self._response.json()
            self._native = Chibi_atlas( raw_data )
            return self._native
