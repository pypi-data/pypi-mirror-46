from zeep import exceptions as zeep_exceptions


class Compass_exception_base( Exception ):
    def __init__(
            self, *args, error_code, additional_messages=None,
            response=None, **kw ):

        self.error_code = error_code
        if additional_messages is None:
            additional_messages = []
        self.additional_messages = additional_messages
        self.response = response
        super().__init__( *args, **kw )

    def __str__( self ):
        if self.additional_messages:
            messages = "\n".join( self.additional_messages )
            return "error code: '{}', '{}'\n{}".format(
                self.error_code, super().__str__(), messages )
        else:
            return "error code: '{}', '{}'".format(
                self.error_code, super().__str__() )


class Still_processing( Compass_exception_base ):
    pass


class Duplicate_still_processing( Compass_exception_base ):
    pass


class No_match( Compass_exception_base ):
    pass


class Deleted_report( Compass_exception_base ):
    pass


class Incorrect_order_information( Compass_exception_base ):
    pass


class System_error_occurred( Compass_exception_base ):
    pass


class Not_authorized_for_product( Compass_exception_base ):
    pass


class Only_office_hour( Compass_exception_base ):
    pass


class Bad_formatted_xml( Compass_exception_base ):
    def __init__( self, *args, **kw ):
        super().__init__(
            "bad formatted xml from compass", error_code='-1' )


class Compass_soap( Compass_exception_base ):
    def __init__( self, *args, **kw ):
        super().__init__(
            "unhandled soap exception", error_code='-10', **kw )

    @classmethod
    def find_correct_exception( cls, exception ):
        if isinstance( exception, zeep_exceptions.Fault ):
            if 'Invalid Client Code or User' in str( exception ):
                raise Not_authorized() from exception
            else:
                raise cls from exception
        else:
            raise exception


class Not_authorized( Compass_soap ):
    def __init__( self, *args, **kw ):
        super().__init__(
            "Invalid client code or user", error_code='-11', **kw )
