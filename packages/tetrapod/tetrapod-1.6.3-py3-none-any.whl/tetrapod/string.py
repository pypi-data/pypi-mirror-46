from .regex import separate_camelcase_phase_1, separate_camelcase_phase_2


__all__ = [ 'camel_to_snake' ]


def camel_to_snake( s ):
    result = separate_camelcase_phase_1.sub( r'\1_\2', s )
    result = separate_camelcase_phase_2.sub( r'\1_\2', result ).lower()
    return result
