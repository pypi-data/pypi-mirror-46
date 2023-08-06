import factory
from faker import Factory as Faker_factory
from .bgc import BGC


fake = Faker_factory.create()


class _Us_one_validate_order( factory.Factory ):
    SSN = factory.lazy_attribute(
        lambda x: fake.ssn().replace( '-', '' ) )

    class Meta:
        model = dict


class _Us_one_validate_record( factory.Factory ):
    is_deceased = factory.lazy_attribute( lambda x: fake.boolean() )
    is_valid = factory.lazy_attribute( lambda x: fake.boolean() )
    text_response = factory.lazy_attribute(
        lambda x: fake.sentence(
            nb_words=20, variable_nb_words=True, ext_word_list=None ) )
    year_issued = None
    state_issued = None

    class Meta:
        model = dict


class _Us_one_validate( factory.Factory ):
    version = 1
    order = factory.SubFactory( _Us_one_validate_order )
    response = factory.lazy_attribute(
        lambda x: { 'validation': _Us_one_validate_record.build() } )

    class Meta:
        model = dict


class Us_one_trace( BGC ):
    """
    basic factory for test the function of us_one_validate
    """
    product = factory.Dict(
        { 'us_one_validate': factory.SubFactory( _Us_one_validate ) } )

    class Meta:
        model = dict
