class Laniidae_exception( Exception ):
    def __init__( self, *args, status_code, body, **kw ):
        self.status_code = status_code
        self.body = body

    def __str__( self ):
        return "error code: '{}', '{}'\n{}".format(
            self.status_code, super().__str__(), self.body )
