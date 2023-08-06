import factory
import random
from faker import Factory as Faker_factory


fake = Faker_factory.create()


class BGC( factory.Factory ):
    order_id = factory.lazy_attribute( lambda x: fake.uuid4() )
    xmlns_xsi = 'http://www.w3.org/2001/XMLSchema-instance'
    xsi_noNamespaceSchemaLocation = (
        'http://localhost/schema/BGCDirect/4.13/OnlineResponse.xsd' )

    class Meta:
        model = dict


class _BGC_error( factory.Factory ):
    code = factory.lazy_attribute( lambda x: random.choice( ( '20', '28', ) ) )
    text = factory.lazy_attribute(
        lambda x: fake.sentence(
            nb_words=20, variable_nb_words=True, ext_word_list=None ) )

    class Meta:
        model = dict


class BGC_error( BGC ):
    response = factory.lazy_attribute(
        lambda x: { 'errors': [ _BGC_error.build() ] } )
