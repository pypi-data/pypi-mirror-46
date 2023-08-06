from mudskipper.endpoint import (
    POST,
    Endpoint as Endpoint_base,
    Response as Response_base,
)
import xmltodict
from tetrapod.bgc.exceptions import BGC_exception_base
from xml.parsers.expat import ExpatError
import json


class Response( Response_base ):
    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            raw_response = self._response.text
            try:
                parse = xmltodict.parse( raw_response )
            except ExpatError as e:
                raise BGC_exception_base( { '0': raw_response } ) from e
            self._native = json.loads( json.dumps( parse ) )
            return self._native


class Endpoint( Endpoint_base, POST ):
    def build_response( self, response, method=None ):
        return Response( response )

    def generate_post_headers( self ):
        return { 'Content-type': 'text/xml; charset=utf-8' }
