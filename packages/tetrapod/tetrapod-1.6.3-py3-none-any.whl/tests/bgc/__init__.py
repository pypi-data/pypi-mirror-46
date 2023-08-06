import os
from tetrapod.bgc import connections


connections.configure(
    default={
        'host': (
            'https://direct2m.backgroundchecks.com/'
            'integration/bgcdirectpost.aspx' ),
        'user': os.environ[ 'BGC__DEFAULT__USER' ],
        'password': os.environ[ 'BGC__DEFAULT__PASSWORD' ],
        'account': os.environ[ 'BGC__DEFAULT__ACCOUNT' ],
    },
    wrong_password={
        'host': (
            'https://direct2m.backgroundchecks.com/'
            'integration/bgcdirectpost.aspx' ),
        'user': os.environ[ 'BGC__WRONG_PASSWORD__USER' ],
        'password': os.environ[ 'BGC__WRONG_PASSWORD__PASSWORD' ],
        'account': os.environ[ 'BGC__WRONG_PASSWORD__ACCOUNT' ],
    },
    wrong_user={
        'host': (
            'https://direct2m.backgroundchecks.com/'
            'integration/bgcdirectpost.aspx' ),
        'user': os.environ[ 'BGC__WRONG_USER__USER' ],
        'password': os.environ[ 'BGC__WRONG_USER__PASSWORD' ],
        'account': os.environ[ 'BGC__WRONG_USER__ACCOUNT' ],
    },
    wrong_account={
        'host': (
            'https://direct2m.backgroundchecks.com/'
            'integration/bgcdirectpost.aspx' ),
        'user': os.environ[ 'BGC__WRONG_ACCOUNT__USER' ],
        'password': os.environ[ 'BGC__WRONG_ACCOUNT__PASSWORD' ],
        'account': os.environ[ 'BGC__WRONG_ACCOUNT__ACCOUNT' ],
    },
)
