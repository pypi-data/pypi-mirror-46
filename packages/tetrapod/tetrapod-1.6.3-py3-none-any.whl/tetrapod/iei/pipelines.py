from tetrapod.pipelines import Pipeline


class Guaranteed_list(Pipeline):

    def __init__( self, **kw ):
        super().__init__( **kw )

    def process( self, obj, *args, **kw ):
        if isinstance( obj, dict ):
            for k, value in obj.items():
                result = value
                if isinstance( result, dict ):
                    if len( result ) == 2 and 'count' in result:
                        result = self.transform( result )
                obj[ k ] = result
                self.process( result )
        elif isinstance( obj, list ):
            for i in obj:
                self.process( i )
        return obj

    def transform( self, x ):
        for k, v in x.items():
            if k != 'count':
                if not isinstance( v, list ):
                    return [ v ]
                return v


class Time_lapse(Pipeline):

    def __init__( self, *keys, **kw ):
        self._keys = keys
        super().__init__( **kw )

    def process(self, obj, *args, **kw):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in self._keys:
                    obj[k] = self.transform(v)
                else:
                    self.process(v)
        elif isinstance(obj, list):
            for i in obj:
                self.process(i)
        return obj

    def transform(self, x):
        years = x.get('years', 0)
        months = x.get('months', 0)
        days = x.get('days', 0)

        lapse = "{} YEARS {} MONTHS {} DAYS".format(years, months, days)
        return lapse
