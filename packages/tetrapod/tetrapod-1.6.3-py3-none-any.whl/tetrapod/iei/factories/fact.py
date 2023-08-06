import factory
import random
from faker import Factory as Faker_factory

from tetrapod.factories import Dict_date, Dict_partial_date
from tetrapod.iei.factories.iei import IEI_with_results, IEI_no_results

fake = Faker_factory.create()


class IEI_fact_record_list(factory.Factory):
    record = factory.lazy_attribute(
        lambda x: IEI_fact_record.build_batch(random.randint(1, 5)))
    count = 0

    class Meta:
        model = dict


class IEI_address_information(factory.Factory):
    message = factory.lazy_attribute(
        lambda x: "SSN IS VALID.  ISSUED IN {}".format(fake.state_abbr()))
    year = factory.lazy_attribute(
        lambda x: "IN THE YEAR {}".format(random.randint(1980, 2018)))
    records = factory.SubFactory(IEI_fact_record_list)

    class Meta:
        model = dict


class IEI_fact_address_list(factory.Factory):
    address = factory.lazy_attribute(
        lambda x: IEI_fact_address.build_batch(random.randint(1, 10)))
    count = 0

    class Meta:
        model = dict


class IEI_fact_record(factory.Factory):
    sourceorjurisdiction = factory.lazy_attribute(
        lambda x: fake.sentence(nb_words=3))
    firstname = factory.lazy_attribute(
        lambda x: fake.first_name())
    lastname = factory.lazy_attribute(
        lambda x: fake.last_name())
    middlename = factory.lazy_attribute(
        lambda x: random.choice((fake.first_name(), '')))
    fullname = factory.lazy_attribute(
        lambda x: " ".join([x.firstname, x.middlename, x.lastname]))
    dob = factory.SubFactory(Dict_date)
    fulldob = factory.lazy_attribute(
        lambda x: "/".join([x.dob['month'], x.dob['day'], x.dob['year']]))
    ssn = factory.lazy_attribute(
        lambda x: fake.ssn().replace('-', ''))
    age = factory.lazy_attribute(lambda x: random.randint(21, 110))

    addresses = factory.SubFactory(IEI_fact_address_list)

    class Meta:
        model = dict


class IEI_fact_address(factory.Factory):

    street_name = factory.lazy_attribute(
        lambda x: fake.street_name())
    street_number = factory.lazy_attribute(
        lambda x: fake.building_number())
    street_suffix = factory.lazy_attribute(
        lambda x: fake.street_suffix())

    fullstreet = factory.lazy_attribute(
        lambda x: fake.street_address())

    city = factory.lazy_attribute(lambda x: fake.city())
    state = factory.lazy_attribute(lambda x: fake.state_abbr())
    county = factory.lazy_attribute(lambda x: fake.city())
    from_date = factory.SubFactory(Dict_partial_date)
    to_date = factory.SubFactory(Dict_partial_date)
    zip = factory.lazy_attribute(lambda x: fake.postalcode())
    zip4 = factory.lazy_attribute(lambda x: fake.numerify(text="####"))
    street_pre_direction = factory.lazy_attribute(lambda x: fake.city_prefix())

    @factory.post_generation
    def groups(self, *arg, **kwargs):
        from_date = self.pop('from_date', None)
        self['from-date'] = from_date
        to_date = self.pop('to_date', None)
        self['to-date'] = to_date

    class Meta:
        model = dict


class IEI_fact(IEI_with_results):
    addressinformation = factory.SubFactory(IEI_address_information)


class IEI_fact_no_results(IEI_no_results):
    addressinformation = factory.SubFactory(IEI_address_information)
