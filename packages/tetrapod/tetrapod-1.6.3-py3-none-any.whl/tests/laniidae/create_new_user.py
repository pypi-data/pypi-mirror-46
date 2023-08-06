from faker import Factory as Faker_factory
from vcr_unittest import VCRTestCase

from tetrapod.laniidae import laniidae, connections
from tetrapod.laniidae.endpoints import User_detail


fake = Faker_factory.create()


class dump:
    pass


class Test_new_users( VCRTestCase ):
    def setUp( self ):
        super().setUp()
        self.client = laniidae.using( 'super_user' )

    def test_create_new_users( self ):
        response = self.client.create_user(
            user_name=fake.user_name(), password=fake.password(),
            email=fake.email(), first_name=fake.first_name(),
            last_name=fake.last_name(), partner_name=fake.name(),
            webhook_url="http://google.com" )
        self.assertIsInstance( response, User_detail )

    def test_get_new_token_of_a_new_user( self ):
        response = self.client.create_user(
            user_name=fake.user_name(), password=fake.password(),
            email=fake.email(), first_name=fake.first_name(),
            last_name=fake.last_name(), partner_name=fake.name(),
            webhook_url="http://google.com" )
        token = response.token
        self.assertTrue( token.format_url.startswith( response.format_url )  )
        self.assertTrue( token.format_url.endswith( 'token' )  )

    def test_token_response_get_a_list_of_tokens( self ):
        response = self.client.create_user(
            user_name=fake.user_name(), password=fake.password(),
            email=fake.email(), first_name=fake.first_name(),
            last_name=fake.last_name(), partner_name=fake.name(),
            webhook_url="http://google.com" )
        token_response = response.token.get()
        token = token_response.native[0].key
        self.assertTrue( token )


class Test_package( VCRTestCase ):
    def setUp( self ):
        super().setUp()
        self.client = laniidae
        connections.set_alias_lambda( lambda x: x.token )

    def test_get_all_packages( self ):
        response = self.client.using( 'super_user' ).create_user(
            user_name=fake.user_name(), password=fake.password(),
            email=fake.email(), first_name=fake.first_name(),
            last_name=fake.last_name(), partner_name=fake.name(),
            webhook_url="http://google.com" )
        token_response = response.token.get()
        token = dump()
        token.token = token_response.native[0].key
        response = self.client.using( token ).package()
        # response = self.client.using( token ).package( name='compass' )
        have_compass = False
        for package in response.native:
            if package.name == 'compass':
                have_compass = True
        if not have_compass:
            self.fail( "cannot find the package of compass" )

    def test_get_compass_package( self ):
        response = self.client.using( 'super_user' ).create_user(
            user_name=fake.user_name(), password=fake.password(),
            email=fake.email(), first_name=fake.first_name(),
            last_name=fake.last_name(), partner_name=fake.name(),
            webhook_url="http://google.com" )
        token_response = response.token.get()
        token = dump()
        token.token = token_response.native[0].key
        response = self.client.using( token ).package( name='compass' )
        self.assertEqual( response.native[0].name, 'compass' )

    def test_do_a_check( self ):
        response = self.client.using( 'super_user' ).create_user(
            user_name=fake.user_name(), password=fake.password(),
            email=fake.email(), first_name=fake.first_name(),
            last_name=fake.last_name(), partner_name=fake.name(),
            webhook_url="http://google.com" )
        token_response = response.token.get()
        token = dump()
        token.token = token_response.native[0].key
        response = self.client.using( token ).package( name='compass' )
        compass = response.native[0]
        response = compass.check.post( {
            'first_name': fake.first_name(), 'last_name': fake.last_name(),
            'state': 'IL', 'driver_license_number': '123456789',
            'date_of_birth': '1980-01-01', 'gender': '',
        } )
        self.assertTrue(
            response.format_url.startswith(
                'http://laniidae:8000/profiles/' ) )

    def test_get_the_profile_after_check( self ):
        response = self.client.using( 'super_user' ).create_user(
            user_name=fake.user_name(), password=fake.password(),
            email=fake.email(), first_name=fake.first_name(),
            last_name=fake.last_name(), partner_name=fake.name(),
            webhook_url="http://google.com" )
        token_response = response.token.get()
        token = dump()
        token.token = token_response.native[0].key
        response = self.client.using( token ).package( name='compass' )
        compass = response.native[0]
        response = compass.check.post( {
            'first_name': fake.first_name(), 'last_name': fake.last_name(),
            'state': 'IL', 'driver_license_number': '123456789',
            'date_of_birth': '1980-01-01', 'gender': '',
        } )
        profile_response = response.get().native
        self.assertEqual( profile_response.status, 'wait' )

    def test_get_profile_with_url( self ):
        response = self.client.using( 'super_user' ).create_user(
            user_name=fake.user_name(), password=fake.password(),
            email=fake.email(), first_name=fake.first_name(),
            last_name=fake.last_name(), partner_name=fake.name(),
            webhook_url="http://google.com" )
        token_response = response.token.get()
        token = dump()
        token.token = token_response.native[0].key
        response = self.client.using( token ).package( name='compass' )
        compass = response.native[0]
        response = compass.check.post( {
            'first_name': fake.first_name(), 'last_name': fake.last_name(),
            'state': 'IL', 'driver_license_number': '123456789',
            'date_of_birth': '1980-01-01', 'gender': '',
        } )
        profile_response = response.get().native

        response = self.client.using( 'super_user' ).profile(
            url=profile_response.url ).native
        self.assertEqual( profile_response, response )
