class IEI_exception_base( Exception ):
    def __init__( self, errors, *args, **kw ):
        self._iei_errors = errors
        super().__init__( *args, **kw )

    def __str__( self ):
        return str(
            [ 'code: {} -- text: "{}"'.format( k, v )
                for k, v in self._iei_errors.items() ] )


class IEI_ncis_exception( IEI_exception_base ):
    pass
