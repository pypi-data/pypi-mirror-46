import os
from tetrapod.pusher import connections


connections.configure(
    default={
        'app_id': os.environ[ 'PUSHER__DEFAULT__APP_ID' ],
        'cluster': os.environ[ 'PUSHER__DEFAULT__CLUSTER' ],
        'key': os.environ[ 'PUSHER__DEFAULT__KEY' ],
        'secret': os.environ[ 'PUSHER__DEFAULT__SECRET' ],
    },
    test_mode={
        'app_id': os.environ[ 'PUSHER__DEFAULT__APP_ID' ],
        'cluster': os.environ[ 'PUSHER__DEFAULT__CLUSTER' ],
        'key': os.environ[ 'PUSHER__DEFAULT__KEY' ],
        'secret': os.environ[ 'PUSHER__DEFAULT__SECRET' ],
        'test_mode': True,
    },
)
