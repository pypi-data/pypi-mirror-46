import os
from tetrapod.compass import connections


connections.configure(
    default={
        'wsdl': 'tests/compass/DatalinkOrderService.wsdl.xml',
        'account': os.environ[ 'COMPASS__DEFAULT__ACCOUNT' ],
        'user': os.environ[ 'COMPASS__DEFAULT__USER' ],
        'password': os.environ[ 'COMPASS__DEFAULT__PASSWORD' ]
    },
)
