import unittest
from unittest.mock import patch, Mock

from tetrapod.bgc import bgc, exceptions
from tetrapod.bgc.factories.us_one_validate import (
    Us_one_trace as Us_one_trace_factory
)
from tetrapod.bgc.factories.bgc import BGC_error as BGC_error_factory
from vcr_unittest import VCRTestCase
import datetime


class Test_bgc( unittest.TestCase ):
    def setUp( self ):
        self.client = bgc
        super().setUp()


class Test_us_one_search( VCRTestCase, Test_bgc ):
    def test_just_work( self ):
        result = self.client.us_one_search(
            ssn='048920148', first_name='Luis', last_name='Morales',
            middle_name='Alberto',
            dob=datetime.date( 1994, 10, 20 ),
            jurisdiction='CT', purpose='EMPLOYMENT',
            reference_id='a_reference' )
        self.assertIsInstance( result, dict )


class Test_build_body( Test_bgc ):
    def test_should_add_the_reference_id( self ):
        result = self.client.build_body( reference_id="a_reference" )
        self.assertEqual( result[ 'BGC' ][ '@referenceKey' ], "a_reference" )


class Test_us_one_validate( VCRTestCase, Test_bgc ):
    def test_ssn_from_the_page( self ):
        result = self.client.us_one_validate(
            ssn='899999914', reference_id='a_reference' )
        self.assertIn( 'order_id', result )
        self.assertIsInstance( result['order'], dict )
        self.assertIsInstance( result['is_valid'], bool )
        self.assertIsInstance( result['is_deceased'], bool )
        self.assertIsInstance( result['text_response'], str )
        self.assertTrue(
            result['text_response'], "the message should no be empty" )

        self.assertIsNone( result['state_issued'] )
        self.assertIsNone( result['year_issued'] )


class Test_us_one_validate_with_factory( Test_bgc ):
    def setUp( self ):
        self.factory = Us_one_trace_factory
        super().setUp()

    def test_ssn_from_factory( self ):
        result = self.client.us_one_validate(
            ssn='899999914', _use_factory=self.factory,
            reference_id="a_reference" )
        self.assertIn( 'order_id', result )
        self.assertIsInstance( result['order'], dict )
        self.assertIsInstance( result['is_valid'], bool )
        self.assertIsInstance( result['is_deceased'], bool )
        self.assertIsInstance( result['text_response'], str )
        self.assertTrue(
            result['text_response'], "the message should no be empty" )

        self.assertIsNone( result['state_issued'] )
        self.assertIsNone( result['year_issued'] )


@unittest.skip( "only return errors" )
class Test_us_one_trace_test_data_from_bgc( VCRTestCase, Test_bgc ):
    def test_ken_rico_89991111( self ):
        bgc.us_one_trace(
            ssn='899991111', first_name='Ken', last_name='Rico',
            reference_id="a_reference" )

    def test_ken_rita_89991111( self ):
        bgc.us_one_trace(
            ssn='899991111', first_name='Ken', last_name='Rita',
            reference_id="a_reference" )

    def test_bob_cornwallis_89999666( self ):
        bgc.us_one_trace(
            ssn='89999666', first_name='Bob', last_name='Cornwallis',
            reference_id="a_reference" )

    def test_bobby_cornwallis_899999666( self ):
        bgc.us_one_trace(
            ssn='899999666', first_name='Bobby', last_name='Cornwallis',
            reference_id="a_reference" )

    def test_john_able_999999990( self ):
        bgc.us_one_trace(
            ssn='999999990', first_name='John', last_name='Able',
            reference_id="a_reference" )

    def test_robbert_cornwallis_899999666( self ):
        bgc.us_one_trace(
            ssn='899999666', first_name='Robbert', last_name='Cornwallis',
            reference_id="a_reference" )

    def test_sam_mcsammy_899999667( self ):
        bgc.us_one_trace(
            ssn='899999667', first_name='Sam', last_name='McSammy',
            reference_id="a_reference" )

    def test_trudy_truthful_899999668( self ):
        bgc.us_one_trace(
            ssn='899999668', first_name='Trudy', last_name='Truthful',
            reference_id="a_reference" )

    def test_akatestdude_akabgcdtest_899999777( self ):
        bgc.us_one_trace(
            ssn='899999777', first_name='AKATestDude',
            last_name='AKABGCDTest',
            reference_id="a_reference" )

    def test_Dontorderthis_Thisisforbgcdtests_899999777( self ):
        bgc.us_one_trace(
            ssn='899999777', first_name='Dontorderthis',
            last_name='Thisisforbgcdtests',
            reference_id="a_reference" )

    def test_jonh_comic_899999915( self ):
        bgc.us_one_trace(
            ssn='899999915', first_name='Jonh', last_name='Comic',
            reference_id="a_reference" )

    def test_john_queue_899999917( self ):
        bgc.us_one_trace(
            ssn='899999917', first_name='Jonh', last_name='Queue',
            reference_id="a_reference" )

    def test_jonh_comic_899999918( self ):
        bgc.us_one_trace(
            ssn='899999918', first_name='Jonh', last_name='Comic',
            reference_id="a_reference" )

    def test_johnny_comical_899999918( self ):
        bgc.us_one_trace(
            ssn='899999918', first_name='Jonh', last_name='Comical',
            reference_id="a_reference" )

    def test_john_able_899999991( self ):
        bgc.us_one_trace(
            ssn='899999991', first_name='John', last_name='Able',
            reference_id="a_reference" )

    def test_jon_able_899999991( self ):
        bgc.us_one_trace(
            ssn='899999991', first_name='Jon', last_name='Able',
            reference_id="a_reference" )

    def test_jenny_fromthewall_899999996( self ):
        bgc.us_one_trace(
            ssn='899999996', first_name='Jenny', last_name='Fromthewall',
            reference_id="a_reference" )

    def test_john_able_999999991( self, bgc_sdaf: dict ):
        bgc.us_one_trace(
            ssn='999999991', first_name='John', last_name='Able',
            reference_id="a_reference" )

    def test_test_dude_999999993( self ):
        bgc.us_one_trace(
            ssn='999999993', first_name='Test', last_name='Dude',
            reference_id="a_reference" )

    def test_test_null_999999993( self ):
        bgc.us_one_trace(
            ssn='999999993', first_name='Test', last_name='NULL',
            reference_id="a_reference" )

    def test_test_nulldistrict_999999993( self ):
        bgc.us_one_trace(
            ssn='999999993', first_name='Test', last_name='Nulldistrict',
            reference_id="a_reference" )

    def test_john_jones_899991234( self ):
        bgc.us_one_trace(
            ssn='899991234', first_name='John', last_name='Jones',
            reference_id="a_reference" )


class Test_exceptions_login( VCRTestCase, Test_bgc ):
    def test_is_no_sended_the_correct_user_should_raise_a_exception( self ):
        with self.assertRaises( exceptions.BGC_exception_base ):
            bgc.using(
                'wrong_user' ).us_one_validate(
                    ssn='899999914', reference_id='a_reference' )

    def test_is_no_sended_the_correct_password_should_raise_a_exception(
            self ):
        with self.assertRaises( exceptions.BGC_exception_base ):
            bgc.using(
                'wrong_password' ).us_one_validate(
                    ssn='899999914', reference_id='a_reference' )

    def test_is_no_sended_the_correct_account_should_raise_a_exception( self ):
        with self.assertRaises( exceptions.BGC_exception_base ):
            bgc.using(
                'wrong_account' ).us_one_validate(
                    ssn='899999914', reference_id='a_reference' )


class BGC_factory_exception( unittest.TestCase ):
    def setUp( self ):
        self.factory = BGC_error_factory
        super().setUp()


class BGC_build_xml_text( Test_bgc ):
    def test_build_us_one_trace_should_login_be_before_that_product( self ):
        xml_text = self.client.build_us_one_trace(
            ssn='899999914', first_name='jonh', last_name='dow',
            reference_id="a_reference" )
        self.assertLess(
            xml_text.index( 'login' ), xml_text.index( 'product' ) )

    def test_build_us_one_validate_should_login_be_before_that_product( self ):
        xml_text = self.client.build_us_one_validate(
            ssn='899999914', reference_id="a_reference" )
        self.assertLess(
            xml_text.index( 'login' ), xml_text.index( 'product' ) )


class Test_client_raise_base_exception( Test_bgc, BGC_factory_exception ):
    def test_us_one_validate_raise_exception( self ):
        with self.assertRaises( exceptions.BGC_exception_base ):
            self.client.us_one_validate(
                ssn='899999914', reference_id="a_reference",
                _use_factory=self.factory )

    def test_us_one_trace_rasise_exception( self ):
        with self.assertRaises( exceptions.BGC_exception_base ):
            self.client.us_one_trace(
                ssn='899991111', first_name='Ken', last_name='Rico',
                reference_id='a_reference', _use_factory=self.factory )

    @patch( 'requests.post' )
    def test_us_one_trace_raise_base_exception_with_malformed_xml(
            self, request_post ):
        request_post.return_value = Mock( text='<xml>asdf<ml>>>' )
        with self.assertRaises( exceptions.BGC_exception_base ):
            self.client.us_one_trace(
                ssn='899991111', first_name='Ken', last_name='Rico',
                reference_id='a_reference', )

    @patch( 'requests.post' )
    def test_us_one_validate_raise_exception_with_malformed_xml(
            self, request_post ):
        request_post.return_value = Mock( text='<xml>asdf<ml>>>' )
        with self.assertRaises( exceptions.BGC_exception_base ):
            self.client.us_one_validate(
                ssn='899999914', reference_id='a_reference' )
