import json
from .string import camel_to_snake
from .regex import test as regex_test
import re


def get_items_by_regex( d, regex ):
    regex = re.compile( regex )
    return { k: v for k, v in d.items() if regex_test( regex, k ) }


def delete_list_of_keys( d, keys ):
    for key in keys:
        del d[ key ]
    return d


def _remove_element_list( l, element ):
    result = []
    for i in l:
        if i is element:
            continue
        if isinstance( i, list ):
            result.append( _remove_element_list( i, element ) )
        if isinstance( i, dict ):
            result.append( remove_element( i, element ) )

    return result


def remove_element( d, element ):
    keys_to_delete = []
    for key, value in d.items():
        if value is element:
            keys_to_delete.append( key )
            continue
        if isinstance( value, dict ):
            r = remove_element( value, element )
        elif isinstance( value, list ):
            r = _remove_element_list( value, element )
        else:
            continue
        if r:
            d[ key ] = r
        else:
            keys_to_delete.append( key )

    delete_list_of_keys( d, keys_to_delete )
    return d


def remove_nones( d ):
    return remove_element( d, None )


def i_hate_ordered_dict( d ):
    return json.loads( json.dumps( d ) )


def keys_to_snake_case( d ):
    result = {}
    for k, v in d.items():
        if isinstance( k, str ):
            k = camel_to_snake( k )
        if isinstance( v, ( dict, list, tuple ) ):
            v = _inner_keys_to_snake_case( v )
        result[k] = v
    return result


def _inner_keys_to_snake_case( d ):
    if isinstance( d, dict ):
        return keys_to_snake_case( d )
    elif isinstance( d, list ):
        return [ _inner_keys_to_snake_case( a ) for a in d ]
    elif isinstance( d, tuple ):
        return tuple( _inner_keys_to_snake_case( a ) for a in d )
    return d
