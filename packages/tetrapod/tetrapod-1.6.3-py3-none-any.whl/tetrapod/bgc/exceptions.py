class BGC_exception_base( Exception ):
    def __init__( self, errors, *args, **kw ):
        self._bgc_errors = errors
        super().__init__( *args, **kw )

    def __str__( self ):
        return str(
            [ 'code: {} -- text: "{}"'.format( k, v )
                for k, v in self._bgc_errors.items() ] )


class BGC_us_one_trace_exception( BGC_exception_base ):
    pass


class BGC_us_one_search_exception( BGC_exception_base ):
    pass
