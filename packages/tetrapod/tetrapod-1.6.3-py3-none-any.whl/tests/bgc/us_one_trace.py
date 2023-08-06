import datetime
import unittest

from .client import Test_bgc
from tetrapod.bgc import exceptions
from tetrapod.bgc.factories.us_one_trace import (
    Us_one_trace as Us_one_trace_factory,
    Us_one_trace_with_error as Us_one_trace_with_error_factory,
)
from unittest.mock import patch
from vcr_unittest import VCRTestCase


class Basic_factory_us_one_trace( unittest.TestCase ):
    def setUp( self ):
        self.factory = Us_one_trace_factory
        super().setUp()


class Test_us_one_trace_factory_errors( unittest.TestCase ):
    def setUp( self ):
        self.factory = Us_one_trace_with_error_factory
        super().setUp()


class Test_raise_the_correct_error(
        Test_bgc, Test_us_one_trace_factory_errors ):

    def test_should_raise_bgc_us_one_trace_exception( self ):
        with self.assertRaises( exceptions.BGC_us_one_trace_exception ):
            self.client.us_one_trace(
                ssn='899991111', first_name='Ken', last_name='Rico',
                reference_id="a_reference", _use_factory=self.factory )

    def test_exception_should_have_code_and_text( self ):
        try:
            self.client.us_one_trace(
                ssn='899991111', first_name='Ken', last_name='Rico',
                reference_id='a_reference', _use_factory=self.factory )
            self.fail(
                "should raise the exception 'BGC_us_one_trace_exception' " )
        except exceptions.BGC_us_one_trace_exception as e:
            self.assertIn( "code", str( e ) )
            self.assertIn( "text", str( e ) )


class Test_have_basic_fields_with_factory(
        Test_bgc, Basic_factory_us_one_trace ):

    def test_should_containt_the_min_fields( self ):
        result = self.client.us_one_trace(
            ssn='899991111', first_name='Ken', last_name='Rico',
            reference_id="a_reference", _use_factory=self.factory )
        self.assertIn( 'order_id', result )
        self.assertTrue( result[ 'order_id' ] )
        self.assertIn( 'order', result )
        self.assertIsInstance( result[ 'order' ], dict )
        self.assertIn( 'records', result )
        self.assertIsInstance( result[ 'records' ], list )

        records = result[ 'records' ]
        for record in records:
            self.assertIn( 'city', record )
            self.assertIn( 'county', record )
            self.assertIn( 'date_first_seen', record )
            self.assertIn( 'first_name', record )
            self.assertIn( 'last_name', record )
            self.assertIn( 'middle_name', record )
            self.assertIn( 'phone_info', record )
            self.assertIn( 'postal_code', record )
            self.assertIn( 'postal_code4', record )
            self.assertIn( 'state', record )
            self.assertIn( 'verified', record )

            street = record[ 'street' ]
            self.assertIn( 'name', street)
            self.assertIn( 'number', street )
            self.assertIn( 'post_direction', street )
            self.assertIn( 'pre_direction', street )
            self.assertIn( 'suffix', street )

            self.assertIsInstance(
                record[ 'date_first_seen' ], datetime.date )
            self.assertIn( 'date_first_seen__raw', record )
            self.assertIsInstance( record[ 'date_first_seen__raw' ], dict )
            self.assertIn( 'date_last_seen', record )
            self.assertIsInstance(
                record[ 'date_last_seen' ], datetime.date )
            self.assertIn( 'date_last_seen__raw', record )
            self.assertIsInstance( record[ 'date_last_seen__raw' ], dict )


class Test_us_one_trace_use_basic_facory_no_used_requests(
        Test_bgc, Basic_factory_us_one_trace ):

    @patch( 'requests.post' )
    def test_should_no_call_request_post( self, requests ):
        self.client.us_one_trace(
            ssn='899991111', first_name='Ken', last_name='Rico',
            reference_id='a_reference', _use_factory=self.factory )
        requests.post.assert_not_called()

    @patch( 'requests.put' )
    def test_should_no_call_request_put( self, requests ):
        self.client.us_one_trace(
            ssn='899991111', first_name='Ken', last_name='Rico',
            reference_id='a_reference', _use_factory=self.factory )
        requests.put.assert_not_called()

    @patch( 'requests.get' )
    def test_should_no_call_request_get( self, requests ):
        self.client.us_one_trace(
            ssn='899991111', first_name='Ken', last_name='Rico',
            reference_id='a_reference', _use_factory=self.factory )
        requests.get.assert_not_called()

    @patch( 'requests.delete' )
    def test_should_no_call_request_delete( self, requests ):
        self.client.us_one_trace(
            ssn='899991111', first_name='Ken', last_name='Rico',
            reference_id='a_reference', _use_factory=self.factory )
        requests.delete.assert_not_called()


class Test_with_jonh_doe( Test_bgc, VCRTestCase ):

    def test_with_more_of_one_record_should_return_a_simple_list( self ):
        result = self.client.us_one_trace(
            ssn='999999999', first_name='jonh', last_name='doe',
            reference_id='a_reference' )
        records = result[ 'records' ]
        self.assertIsInstance( records, list )
        self.assertTrue( records )
        for record in records:
            self.assertIsInstance( record, dict )

    def test_should_containt_the_min_fields( self ):
        result = self.client.us_one_trace(
            ssn='999999999', first_name='jonh', last_name='doe',
            reference_id='a_reference' )

        self.assertIn( 'order_id', result )
        self.assertTrue( result[ 'order_id' ] )
        self.assertIn( 'order', result )
        self.assertIsInstance( result[ 'order' ], dict )
        self.assertIn( 'records', result )
        self.assertIsInstance( result[ 'records' ], list )

        records = result[ 'records' ]
        for record in records:
            self.assertIn( 'city', record )
            self.assertIn( 'county', record )

            self.assertIn( 'first_name', record )
            self.assertIn( 'last_name', record )
            self.assertIn( 'middle_name', record )
            self.assertIn( 'phone_info', record )
            self.assertIn( 'postal_code', record )
            self.assertIn( 'postal_code4', record )
            self.assertIn( 'state', record )
            self.assertIn( 'verified', record )

            street = record[ 'street' ]
            self.assertIn( 'name', street)
            self.assertIn( 'number', street )
            self.assertIn( 'post_direction', street )
            self.assertIn( 'pre_direction', street )
            self.assertIn( 'suffix', street )

            self.assertIsInstance(
                record[ 'date_first_seen' ], datetime.date )
            self.assertIn( 'date_first_seen__raw', record )
            self.assertIsInstance( record[ 'date_first_seen__raw' ], dict )
            self.assertIn( 'date_last_seen', record )
            self.assertIsInstance(
                record[ 'date_last_seen' ], datetime.date )
            self.assertIn( 'date_last_seen__raw', record )
            self.assertIsInstance( record[ 'date_last_seen__raw' ], dict )
