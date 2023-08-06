import factory
from faker import Factory as Faker_factory

fake = Faker_factory.create()


class IEI_request_information(factory.Factory):
    code = "100"
    codemessage = "RECORDS FOUND"
    inputs = {}

    class Meta:
        model = dict


class IEI_request_information_no_records(factory.Factory):
    code = "101"
    codemessage = "NO RECORDS FOUND"
    inputs = {}

    class Meta:
        model = dict


class IEI_response(factory.Factory):
    disclaimer_link = """**IMPORTANT NOTICE** USE OR DISSEMINATION OF
    THIS DATA IS SUBJECT TO THE TERMS, CONDITIONS, RESTRICTIONS AND
    LIMITATIONS SPECIFIED AT:
    http://www.backgroundscreeningsystems.com/disclaimers.aspx"""

    class Meta:
        model = dict


class IEI_with_results(IEI_response):
    requestinformation = factory.SubFactory(IEI_request_information)


class IEI_no_results(IEI_response):
    requestinformation = factory.SubFactory(IEI_request_information_no_records)
