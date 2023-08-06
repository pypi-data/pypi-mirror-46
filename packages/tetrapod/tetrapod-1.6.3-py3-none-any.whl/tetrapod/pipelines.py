import re
import copy
import datetime
import itertools

from .s_dict import keys_to_snake_case, remove_nones


__all__ = [ 'Pipeline', 'Transform_keys_camel_case_to_snake' ]


DATE_ISO = '%Y-%m-%d'


class Pipeline_manager:
    def __init__( self, *args, **kw ):
        self.children = []

    def __repr__( self ):
        result = "<class {}( children={} )>".format(
            self.__class__, self.op, self.children )
        return result

    def __copy__( self ):
        return copy.deepcopy( self )

    def __deepcopy__( self, extra_shit ):
        new_node = self.__class__()
        for child in self.children:
            new_node.append( child )
        return new_node

    def append( self, other ):
        self.children.append( other )

    def __add__( self, other ):
        result = copy.copy( self )
        result.children += other.children
        return result

    def __or__( self, other ):
        me = copy.deepcopy(self)
        if isinstance( other, Pipeline_manager ):
            return me + other

        me.append(other)
        return me

    def to_dict( self ):
        result = {
            'children': [ child for child in self.children ]
        }
        return result

    def run( self, obj ):
        result = obj
        for node in self.children:
            if isinstance( node, type ):
                node = node()
            result = node.process( result )
        return result


class Pipeline_meta( type ):
    def __or__( cls, other ):
        return Pipeline_manager() | cls | other


class Pipeline( metaclass=Pipeline_meta ):
    FUN = None

    def __init__( self, *args, fun=None, **kw ):
        if fun is None:
            self._fun = self.FUN
        else:
            self._fun = fun

    def process( self, obj, *arg, **kw ):
        if not self._fun:
            raise NotImplementedError
        else:
            return self._fun( obj )

    def __or__( self, other ):
        return Pipeline_manager() | self | other


class Transform_keys_camel_case_to_snake( Pipeline ):
    def FUN( self, obj ):
        return keys_to_snake_case( obj )


class Remove_nones( Pipeline ):
    def FUN( self, obj ):
        return remove_nones( obj )


class Remove_xml_garage( Pipeline ):

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            result = {}
            for k, v in obj.items():
                if k.startswith( '#' ) or k.startswith( '@' ) or ':' in k:
                    new_k = k[1:]
                    new_k = new_k.replace( ':', '_' )
                    k = new_k
                result[ k ] = self.process( v )
            return result
        elif isinstance( obj, list ):
            return [ self.process( i ) for i in obj ]
        return obj


class Replace_string( Pipeline ):

    def __init__( self, string, value, *args, **kw ):
        self.string = string
        self.value = value
        super().__init__( *args, **kw )

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            for k, v in obj.items():
                if v == self.string:
                    obj[k] = self.value
                self.process( v )
        elif isinstance( obj, list ):
            for i in obj:
                self.process( i )
        return obj


class Rename_key( Pipeline ):

    def __init__( self, *key_to_key, **kw ):
        self._key_to_key = key_to_key
        super().__init__( *key_to_key, **kw )

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            for k, new_k in self._key_to_key:
                if k in obj:
                    obj[ new_k ] = obj.pop( k )
            for v in obj.values():
                self.process( v )
        elif isinstance( obj, list ):
            for i in obj:
                self.process( i )
        return obj


class Guaranteed_list( Pipeline ):

    def __init__( self, *keys, **kw ):
        self._keys = keys
        super().__init__( **kw )

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            for k, v in obj.items():
                if k in self._keys:
                    obj[ k ] = self.transform( v )
                self.process( v )
        elif isinstance( obj, list ):
            for i in obj:
                self.process( i )
        return obj

    def transform( self, x ):
        if not x:
            return []
        elif isinstance( x, list ):
            return x
        else:
            return [x]


class Compress_dummy_list( Pipeline ):

    def __init__( self, *keys, **kw ):
        self._keys = keys
        super().__init__( **kw )

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            for k, v in obj.items():
                if k in self._keys:
                    obj[ k ] = self.transform( v )
                self.process( v )
        elif isinstance( obj, list ):
            for i in obj:
                self.process( i )
        return obj

    def transform( self, x ):
        if isinstance( x, list ):
            result = []
            for y in x:
                if isinstance( y, dict ) and len( y ) == 1:
                    result += list( y.values() )
                else:
                    result.append( y )
            return result
        else:
            return x


class Compress_double_list( Pipeline ):

    def __init__( self, *keys, **kw ):
        self._keys = keys
        super().__init__( **kw )

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            for k, v in obj.items():
                if k in self._keys:
                    obj[ k ] = self.transform( v )
                self.process( v )
        elif isinstance( obj, list ):
            for i in obj:
                self.process( i )
        return obj

    def transform( self, x ):
        if ( isinstance( x, list ) and len( x ) == 1
                and isinstance( x[0], list ) ):
            return x[0]
        return x


class Parse_dict( Pipeline ):
    def __init__( self, *keys, **kw ):
        self._keys = keys
        super().__init__( **kw )

    def _corresponds_to_my_dict( self, d ):
        return set( d.keys() ) == set( self._keys )

    def transform( self, d ):
        raise NotImplementedError

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            result = {}
            for k, v in obj.items():
                if isinstance( v, dict ) and self._corresponds_to_my_dict( v ):
                    result[ "{}__raw".format( k ) ] = v
                    result[k] = self.transform( v )
                else:
                    result[k] = self.process( v )
            return result
        elif isinstance( obj, list ):
            return [ self.process( i ) for i in obj ]
        return obj


class Parse_full_dict_date(Parse_dict):
    def __init__(self, **kw):
        super().__init__('year', 'month', 'day')

    def transform(self, d):
        def x(a, b):
            return int(a) if a not in ('', '0', '00', '0000') else b
        year = x(d['year'], 1000)
        month = x(d['month'], 1)
        day = x(d['day'], 1)
        return datetime.date(year, month, day)


class Remove_year_zero( Parse_dict ):
    def __init__( self, **kw ):
        super().__init__( 'year', 'month', 'day' )

    def transform( self, d ):
        if int( d[ 'year' ] ) == 0:
            return { 'month': d[ 'month' ], 'day': d[ 'day' ] }
        return d


class Parse_partial_dict_date( Parse_dict ):
    def __init__( self, **kw ):
        super().__init__( 'year', 'month', )

    def transform( self, d ):
        if int( d[ 'year' ] ) == 0:
            return datetime.date( year=1000, month=int( d[ 'month' ] ), day=1 )
        return datetime.date(
            year=int( d[ 'year' ] ), month=int( d[ 'month' ] ), day=1 )


class Expand_dict_with_start_with( Pipeline ):
    def __init__( self, new_key, start_with, *args, **kw ):
        self._new_key = new_key
        self._start_with = start_with
        self._regex = re.compile( r"^{}".format( start_with ) )
        super().__init__( *args, **kw )

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            result = {}
            expand_keys = list( filter(
                self._regex.match, obj.keys() ) )
            normal_keys = list( itertools.filterfalse(
                self._regex.match, obj.keys() ) )
            if expand_keys:
                result[ self._new_key ] = {
                    k.replace( self._start_with, '' ):
                        self.process( obj[k] )
                    for k in expand_keys }
            if normal_keys:
                result.update( {
                    k: self.process( obj[k] )
                    for k in normal_keys } )
            return result
        elif isinstance( obj, list ):
            return [ self.process( i ) for i in obj ]
        return obj


class Convert_dates_from_formats( Pipeline ):

    def __init__( self, from_format, to_format, default_invalid, *keys, **kw ):
        self._keys = keys
        self._from_format = from_format
        self._to_format = to_format
        self._default_invalid = default_invalid
        super().__init__( **kw )

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            for k, v in obj.items():
                if k in self._keys:
                    obj[k] = self.transform( v )
                else:
                    self.process( v )
        elif isinstance( obj, list ):
            for i in obj:
                self.process( i )
        return obj

    def transform( self, x ):
        try:
            d = datetime.datetime.strptime( x, self._from_format )
            return d.strftime( self._to_format )
        except:
            return self._default_invalid


class Convert_dates( Pipeline ):

    def __init__( self, from_format, *keys, **kw ):
        self._from_format = from_format
        self._keys = keys
        super().__init__( **kw )

    def _corresponds_to_my_dict( self, d ):
        return set( d.keys() ) == set( self._keys )

    def transform( self, x ):
        if isinstance( self._from_format, str ):
            try:
                return datetime.datetime.strptime( x, self._from_format )
            except ValueError:
                return None
        if isinstance( self._from_format, ( tuple, list ) ):
            result = None
            for _format in self._from_format:
                try:
                    result = datetime.datetime.strptime( x, _format )
                    break
                except ValueError:
                    continue
            return result

    def transform_iso( self, d ):
        if d is None:
            return d
        return d.isoformat()

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            result = {}
            for k, v in obj.items():
                if isinstance( v, str ) and k in self._keys:
                    result[k] = self.transform( v )
                    result["{}__raw".format( k )] = v
                    date_iso = self.transform_iso( result[k])
                    result["{}__iso".format( k )] = date_iso
                else:
                    result[k] = self.process( v )
            return result
        elif isinstance( obj, list ):
            return [ self.process( i ) for i in obj ]
        return obj


class Combine_date_and_time( Pipeline ):

    def __init__( self, *date_time_keys, remove_keys=True, **kw ):
        self._date_time_keys = date_time_keys
        self._remove_keys = remove_keys
        super().__init__( **kw )

    def transform( self, obj, date_key, time_key ):
        try:
            result = datetime.datetime.combine(
                obj[ date_key ], obj[ time_key ] )
        except TypeError:
            return None
        if self._remove_keys:
            del obj[ date_key ]
            del obj[ time_key ]
        return result

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            result = {}
            for date_key, time_key, rename_key in self._date_time_keys:
                if date_key in obj and time_key in obj:
                    result[ rename_key ] = self.transform(
                        obj, date_key, time_key )
            for k, v in obj.items():
                result[k] = self.process( v )
            return result
        elif isinstance( obj, list ):
            return [ self.process( i ) for i in obj ]
        return obj


class Convert_time( Pipeline ):

    def __init__( self, from_format, *keys, **kw ):
        self._from_format = from_format
        self._keys = keys
        super().__init__( **kw )

    def transform( self, x ):
        date = datetime.datetime.strptime( x, self._from_format )
        return date.time()

    def transform_iso( self, d ):
        if d is None:
            return d
        return d.isoformat()

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            result = {}
            for k, v in obj.items():
                if isinstance( v, str ) and k in self._keys:
                    result[k] = self.transform( v )
                    result["{}__raw".format( k )] = v
                    date_iso = self.transform_iso( result[k])
                    result["{}__iso".format( k )] = date_iso
                else:
                    result[k] = self.process( v )
            return result
        elif isinstance( obj, list ):
            return [ self.process( i ) for i in obj ]
        return obj
