import xmltodict

send_orders_xml_format = """
<?xml version="1.0" encoding="utf-8"?>
<DL_Orders
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://imvrs.com">
    <DL_Order xmlns="">
        <DestAcctID>{account}</DestAcctID>
        <DestUserID>{user}</DestUserID>
        <SourceAcctID>{account}</SourceAcctID>
        <SourceUserID>{user}</SourceUserID>
        <SourceRoute>CI</SourceRoute>
        <DestRoute>CO</DestRoute>
        <Quoteback>{partner_worker_id}</Quoteback>
        <Quoteback2/>
        <OrderID/>
        <Source/>
        <Version/>
        <State>{state}</State>
        <ProcessType>OL</ProcessType>
        <ProductCode>DL</ProductCode>
        <ReportType>Standard</ReportType>
        <ReportStyle>XML</ReportStyle>
        <History>{history}</History>
        <PurposeCode>EMP</PurposeCode>
        <DLOrder>
            <DLSearchType>ByLicense</DLSearchType>
            <DLNum>{driver_license_number}</DLNum>
            <FName>{first_name}</FName>
            <MName>{middle_name}</MName>
            <LName>{last_name}</LName>
            <DOB>{date_of_birth}</DOB>
            <Gender>{gender}</Gender>
        </DLOrder>
    </DL_Order>
</DL_Orders>
"""

search_report_xml_format = """
<?xml version="1.0" encoding="utf-8"?>
<DL_Orders
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="http://imvrs.com">
    <DL_Search xmlns="">
        <DestAcctID>{account}</DestAcctID>
        <DestUserID>{user}</DestUserID>
        <SourceAcctID>{account}</SourceAcctID>
        <SourceUserID>{user}</SourceUserID>
        <SourceRoute>CI</SourceRoute>
        <DestRoute>CO</DestRoute>

        <SearchByField>{search_type}</SearchByField>
        <SearchValues>
            {search_values}
        </SearchValues>
    </DL_Search>
</DL_Orders>
"""

search_value = "<SearchValue>{value}</SearchValue>"


def build_send_orders_input( **kw ):
    kw[ 'date_of_birth' ] = kw[ 'date_of_birth' ].strftime( '%m/%d/%Y' )
    body_xml = xmltodict.unparse( build_dict_send_orders( **kw ) )
    body_xml_2 = send_orders_xml_format.format( **kw )
    return body_xml_2
    return body_xml
    # return "<![CDATA[{}]]>".format( body_xml )


def build_search_reports( *values, account, user, search_type ):
    """
    build the xml  for the seach reports

    Parameters
    ==========
    values: list of string or int
        is  the list of id or dates you want to search in compass
    account_id: string or int
    user_id: string or int
    search_type: py:class:`app.mvr.compass_api.seach_types`

    Returns
    =======
    string
    """
    search_values = ''.join([search_value.format(value=v) for v in values])
    common_fields = build_common_fields( account_id, user_id )
    body = search_report_xml_format.format(
        account=account, user=user, search_type=search_type.value,
        search_values=search_values )
    data = base.format( body=body )
    return data


def build_dict_send_orders( **kw ):
    return {
        'DL_Orders': {
            '@xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance",
            '@xmlns:xsd': "http://www.w3.org/2001/XMLSchema",
            '@xmlns': "http://imvrs.com",

            'DL_Order': [
                {
                    '@xmlns': "",
                    'DestAcctID': kw[ 'account' ],
                    'DestUserID': kw[ 'user' ],
                    'SourceAcctID': kw[ 'account' ],
                    'SourceUserID': kw[ 'user' ],

                    'SourceRoute': 'CI',
                    'DestRoute': 'CO',
                    'Quoteback': kw[ 'partner_worker_id' ],
                    'Quoteback2': None,
                    'OrderID': None,
                    'Source': None,
                    'Version': None,
                    'State': kw[ 'state' ],
                    'ProcessType': 'OL',
                    'ProductCode': 'DL',
                    'ReportType': 'Standard',
                    'ReportStyle': 'XML',
                    'History': kw[ 'history' ],

                    'PurposeCode': 'EMP',
                    'DLOrder': {
                        'DLSearchType': 'ByLicense',
                        'DLNum': kw[ 'driver_license_number' ],
                        'FName': kw[ 'first_name' ],
                        'MName': kw[ 'middle_name' ],
                        'LName': kw[ 'last_name' ],
                        'DOB': kw[ 'date_of_birth' ],
                        'Gender': kw[ 'gender' ],
                    },
                }
            ]
        }
    }
