import datetime
import os
import unittest
from vcr_unittest import VCRTestCase
from tetrapod.iei import iei
from tetrapod.iei import connections
from tetrapod.iei.exceptions import IEI_ncis_exception
from tetrapod.iei.factories.fact import IEI_fact

connections.configure(
    default={
        'wsdl': 'https://xml.innovativedatasolutions.com/'
                'NatCrimWs/Search.asmx?WSDL',
        'login': os.environ['IEI__DEFAULT__LOGIN'],
        'password': os.environ['IEI__DEFAULT__PASSWORD']
    },
    wrong_login={
        'wsdl': 'https://xml.innovativedatasolutions.com/'
                'NatCrimWs/Search.asmx?WSDL',
        'login': os.environ['IEI__WRONG__LOGIN'],
        'password': os.environ['IEI__DEFAULT__PASSWORD']
    },
    default_proxies={
        'wsdl': 'https://xml.innovativedatasolutions.com/'
                'NatCrimWs/Search.asmx?WSDL',
        'login': os.environ['IEI__DEFAULT__LOGIN'],
        'password': os.environ['IEI__DEFAULT__PASSWORD'],
        'proxies': {
            'http': 'http://fixie:YoAzlpvu3OG7Uiz@velodrome.usefixie.com:80',
            'https': 'https://fixie:YoAzlpvu3OG7Uiz@velodrome.usefixie.com:80'}
    }
)


class Test_iei(unittest.TestCase):
    def setUp(self):
        self.client = iei
        super().setUp()


class Test_iei_client(VCRTestCase, Test_iei):

    def test_iei_ok_response_with_hits(self):
        result = self.client.ncis(
            ssn='', first_name='Kevin', last_name='Donner',
            middle_name='Thomas',
            dob=datetime.date(1960, 9, 1),
            reference_id='foo@bar')
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result['records']) > 0)

    def test_iei_ok_response_clear(self):
        result = self.client.ncis(
            ssn='', first_name='Nark', last_name='Goldman',
            middle_name='Simonz',
            dob=datetime.date(1970, 1, 1),
            reference_id='foo@bar')
        self.assertListEqual(result['records'], [])

    def test_iei_validates_response(self):
        with self.assertRaises(IEI_ncis_exception):
            self.client.ncis(
                ssn='', first_name='', last_name='',
                middle_name='',
                dob=datetime.date(1960, 9, 1),
                reference_id='')


class Test_exceptions_login(VCRTestCase, Test_iei):

    def test_is_no_sended_the_correct_user_should_raise_a_exception(self):
        with self.assertRaises(IEI_ncis_exception) as ex:
            iei.using('wrong_login').ncis(
                ssn='', first_name='Kevin', last_name='Donner',
                middle_name='Thomas',
                dob=datetime.date(1960, 9, 1),
                reference_id='foo@bar')

        self.assertDictEqual(ex.exception._iei_errors,
                             {'200': 'Invalid username and/or password'})


class Test_client_with_proxy(VCRTestCase, Test_iei):

    def test_client_uses_configured_proxy(self):
        result = iei.using('default_proxies').ncis(
            ssn='', first_name='Kevin', last_name='Donner',
            middle_name='Thomas',
            dob=datetime.date(1960, 9, 1),
            reference_id='foo@bar')

        self.assertIsInstance(result, dict)
        self.assertTrue(len(result['records']) > 0)


class Test_iei_fact_client(VCRTestCase, Test_iei):

    def test_iei_ok_response(self):
        result = self.client.fact(
            ssn='626047234', first_name='Mickey', last_name='Devin',
            reference_id='foo@bar')
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result['records']) > 0)

    def test_iei_fact_deceased_ssn(self):
        result = self.client.fact(ssn='416039521')
        self.assertTrue(result['is_deceased'])

    def test_iei_fact_invalid_ssn(self):
        result = self.client.fact(ssn='899999666')
        self.assertFalse(result['is_valid'])

    def test_iei_fact_invalid_month(self):
        result = self.client.fact(ssn='162781716')
        self.assertEqual(
            result['records'][0]['dob'],
            datetime.date(1997, 1, 1))


class Test_iei_fact_with_factory(Test_iei):

    def setUp(self):
        self.factory = IEI_fact
        super().setUp()

    def test_fact_from_factory(self):
        result = self.client.fact(
            ssn='899999914', _use_factory=self.factory,
            reference_id="a_reference")

        self.assertTrue(result)
        self.assertEqual(result['code'], "100")
        self.assertTrue(result['is_valid'])
        self.assertFalse(result['is_deceased'])
        self.assertIsInstance(result['address_info'], dict)
        self.assertIsInstance(result['request_info'], dict)

        self.assertIsInstance(result['records'], list)
        self.assertTrue(len(result['records']) > 0)

        addresses = result['records'][0]['addresses']
        self.assertIsInstance(addresses, list)
        self.assertTrue(len(addresses) > 0)

        address = addresses[0]
        self.assertIsInstance(address['to-date'], datetime.date)
        self.assertIsInstance(address['from-date'], datetime.date)


class Test_iei_pipelines(Test_iei):

    def test_iei_pipelines(self):
        common_size = len(self.client.COMMON_PIPELINE.children)
        fact_size = len(self.client.FACT_PIPELINE.children)
        self.assertNotEqual(common_size, fact_size)
