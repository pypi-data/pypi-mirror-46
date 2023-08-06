import logging
import xml
from mudskipper import Client_soap
from mudskipper.connection import Connections_soap
from mudskipper.response import Response_xml as Response
from requests import Session
from zeep import Client as Zeep_client
from zeep.transports import Transport
from zeep import exceptions as zeep_exceptions

from .build_xml import build_send_orders_input
from tetrapod.compass import exceptions
from tetrapod.pipelines import (
    Transform_keys_camel_case_to_snake, Remove_xml_garage, Convert_dates,
    Compress_dummy_list, Compress_double_list, Combine_date_and_time,
    Convert_time, Rename_key, Guaranteed_list
)


logger_send_orders = logging.getLogger( 'tetrapod.compass.send_orders' )


class Connections_compass( Connections_soap ):
    def build_zeep_client( self, alias='default' ):
        config = self[ alias ]
        wsdl = config['wsdl']
        proxies = config.get( 'proxies', None )

        session = Session()
        session.verify = False
        transport = Transport( session=session )

        client = Zeep_client( wsdl, transport=transport )

        if proxies:
            client.transport.session.proxies = proxies

        auth = client.get_element(
            '{http://datalinkservices.org/}Authorization' )
        client.set_default_soapheaders( [
            auth(
                AcctID=config[ 'account' ], UserID=config[ 'user' ],
                Password=config[ 'password' ], )
        ] )
        return client


class Client( Client_soap ):

    COMMON_PIPELINE = (
        Remove_xml_garage | Transform_keys_camel_case_to_snake
        | Rename_key(
            ( 'dob', 'date_of_birth' ), ( 'f_name', 'first_name' ),
            ( 'm_name', 'middle_name' ), ( 'l_name', 'last_name' ),
            ( 'full_name_fml', 'full_name' ),
            ( 'exp_date', 'expiration_date' ), )
        | Guaranteed_list(
            'additional_messages', 'addresses', 'sub_violations',
            'licenses', 'classes', 'violations', 'statuses', 'accidents',
            'actions', 'description', 'location', 'adjudication' )
        | Compress_dummy_list(
            'additional_messages', 'addresses', 'sub_violations',
            'licenses', 'classes', 'violations', 'statuses', 'accidents',
            'actions', 'description', 'location', 'adjudication' )
        | Compress_double_list(
            'additional_messages', 'addresses', 'sub_violations',
            'licenses', 'classes', 'violations', 'statuses', 'accidents',
            'actions', 'description', 'location', 'adjudication' )
        | Convert_dates(
            ( '%m/%d/%Y', '%Y-%m-%d' ), 'order_date', 'date_of_bird',
            'exp_date', 'original_issue', 'conviction_date', 'incident_date',
            'report_date', 'date_of_birth', 'order_date', 'expiration_date' )
        | Convert_time( '%H:%M', 'report_time', 'order_time' )
        | Combine_date_and_time(
            ( 'report_date', 'report_time', 'report_date' ),
            ( 'order_date', 'order_time', 'order_date' ) )
    )

    def send_orders(
            self, first_name, last_name, state, driver_license_number,
            date_of_birth, gender='', history='Y3', middle_name='',
            partner_worker_id=None, _use_factory=None ):
        """
        This will send an mvr order to compass and return the results
        as a string
        """
        if _use_factory is not None:
            raise NotImplementedError
        else:
            body = build_send_orders_input(
                first_name=first_name, middle_name=middle_name,
                last_name=last_name, state=state,
                driver_license_number=driver_license_number,
                date_of_birth=date_of_birth, gender=gender, history=history,
                partner_worker_id=partner_worker_id,
                **self.account_info )

            try:
                logger_send_orders.info(
                    'body sended to compass.send_orders\n{}'.format(
                        str( body ) ) )
                raw_response = self.client.service.sendOrders( body )
            except zeep_exceptions.Fault as e:
                exceptions.Compass_soap.find_correct_exception( e )
            response = Response( raw_response )

        try:
            clean_result = self.COMMON_PIPELINE.run( response.native )
        except xml.parsers.expat.ExpatError as e:
            raise exceptions.Bad_formatted_xml from e

        order = clean_result[ 'mvrdl' ][ 'order' ]
        if isinstance( order, list ):
            logger_send_orders.warning(
                "was receiving a query and not the expected response" )
            order = order[1]
        self._validate_response( order )
        return order

    def search_report( self, *ids ):
        if _use_factory is not None:
            raise NotImplementedError

    @property
    def client( self ):
        """
        build the the zeep client using the current connection

        Returns
        =======
        a mistery
        """
        try:
            return self.___client
        except AttributeError:
            alias = self._default_connection_name
            self.___client = self._connections.build_zeep_client( alias )
            return self.___client

    @property
    def account_info( self ):
        connection = self.get_connection()
        return {
            'account': connection[ 'account' ],
            'user': connection[ 'user' ],
            'password': connection[ 'password' ],
        }

    def build_connection( self ):
        return Connections_compass()

    def _validate_response( self, response ):
        report_info = response[ 'report_info' ]
        error_code = report_info.get( 'error_code' )
        if error_code is not None:
            msg = report_info.get( 'error_message' )
            additional_messages = [
                d[ 'text' ] for d in report_info[ 'additional_messages' ] ]

            if error_code == '-5003':
                exception_class = exceptions.No_match
            elif error_code == '-5009':
                exception_class = exceptions.Deleted_report
            elif error_code in ( '-2006', '-2010' ):
                exception_class = exceptions.Incorrect_order_information
            elif error_code == '-1000':
                exception_class = exceptions.System_error_occurred
            elif error_code == '-2023':
                exception_class = exceptions.Not_authorized_for_product
            elif error_code == '-5006':
                exception_class = exceptions.Duplicate_still_processing
            elif error_code == '-5007':
                exception_class = exceptions.Still_processing
            elif error_code == '-5010':
                exception_class = exceptions.Duplicate_still_processing
            else:
                exception_class = exceptions.Compass_exception_base
            raise exception_class(
                msg, error_code=error_code,
                additional_messages=additional_messages, response=response )
