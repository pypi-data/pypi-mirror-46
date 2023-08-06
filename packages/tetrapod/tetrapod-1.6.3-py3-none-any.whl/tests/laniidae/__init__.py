from tetrapod.laniidae import connections


connections.configure(
    default={
        'host': 'laniidae:8000',
        'schema': 'http',
    },

    super_user={
        'host': 'laniidae:8000',
        'schema': 'http',
        'token': 'o8S7u_x_zsbMwHVaEvbKu0mkLAA=',
    },
)
