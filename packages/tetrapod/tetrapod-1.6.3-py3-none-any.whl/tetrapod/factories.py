import factory
from faker import Factory as Faker_factory

fake = Faker_factory.create()


class Dict_partial_date(factory.Factory):
    raw_date = factory.lazy_attribute(lambda x: fake.date_this_decade())
    month = factory.lazy_attribute(lambda x: x.raw_date.strftime("%m"))
    year = factory.lazy_attribute(lambda x: x.raw_date.strftime("%Y"))

    @factory.post_generation
    def groups(self, *arg, **kwargs):
        self.pop('raw_date', None)

    class Meta:
        model = dict


class Dict_date(Dict_partial_date):
    day = factory.lazy_attribute(lambda x: x.raw_date.strftime("%d"))
