import factory
import random
from faker import Factory as Faker_factory

from tetrapod.factories import Dict_partial_date
from .bgc import BGC

fake = Faker_factory.create()


class _Us_one_trace_order( factory.Factory ):
    SSN = factory.lazy_attribute(
        lambda x: fake.ssn().replace( '-', '' ) )
    first_name = factory.lazy_attribute( lambda x: fake.first_name() )
    last_name = factory.lazy_attribute( lambda x: fake.last_name() )

    class Meta:
        model = dict


class _Us_one_trace_phone( factory.Factory ):
    number_is_public = factory.lazy_attribute(
        lambda x: random.choice( ( 'YES', 'NO' ) ) )
    phone_number = factory.lazy_attribute( lambda x: fake.phone_number() )

    class Meta:
        model = dict


class _Us_one_trace_record( factory.Factory ):
    first_name = factory.lazy_attribute( lambda x: fake.first_name() )
    last_name = factory.lazy_attribute( lambda x: fake.last_name() )
    suffix = None
    middle_name = None
    verified = factory.lazy_attribute(
        lambda x: random.choice( ( True, False) ) )

    street_name = factory.lazy_attribute(
        lambda x: fake.street_name() )
    street_number = factory.lazy_attribute(
        lambda x: fake.building_number() )
    street_suffix = factory.lazy_attribute(
        lambda x: fake.street_suffix() )
    street_post_direction = None
    street_pre_direction = None

    city = factory.lazy_attribute( lambda x: fake.city() )
    state = factory.lazy_attribute( lambda x: fake.state_abbr() )
    county = None
    date_first_seen = factory.SubFactory(Dict_partial_date)
    date_last_seen = factory.SubFactory(Dict_partial_date)
    postal_code = factory.lazy_attribute( lambda x: fake.postalcode() )
    postal_code4 = factory.lazy_attribute(
        lambda x: fake.numerify( text="####" ) )
    phone_info = factory.SubFactory( _Us_one_trace_phone )

    class Meta:
        model = dict


class _Us_one_trace( factory.Factory ):
    version = 1
    order = factory.SubFactory( _Us_one_trace_order )
    response = factory.lazy_attribute(
        lambda x: { 'records': [ _Us_one_trace_record.build() ] } )

    class Meta:
        model = dict


class _Us_one_trace_error( factory.Factory ):
    code = factory.lazy_attribute( lambda x: random.choice( ( '20', '28', ) ) )
    text = factory.lazy_attribute(
        lambda x: fake.sentence(
            nb_words=20, variable_nb_words=True, ext_word_list=None ) )

    class Meta:
        model = dict


class _Us_one_trace_errors( factory.Factory ):
    version = 1
    order = factory.SubFactory( _Us_one_trace_order )
    response = factory.lazy_attribute(
        lambda x: { 'errors': [ _Us_one_trace_error.build() ] } )

    class Meta:
        model = dict


class Us_one_trace( BGC ):
    """
    basic factory for test the function of us_one_trace
    """
    product = factory.Dict(
        { 'us_one_trace': factory.SubFactory( _Us_one_trace ) } )

    class Meta:
        model = dict


class Us_one_trace_with_error( BGC ):
    """
    basic factory for generate the exception BGC_us_one_trace_exception
    """
    product = factory.Dict(
        { 'us_one_trace': factory.SubFactory( _Us_one_trace_errors ) } )

    class Meta:
        model = dict
