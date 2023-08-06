import unittest
from unittest.mock import patch

from tetrapod.pusher import pusher


class Test_pusher_with_channel( unittest.TestCase ):
    def setUp( self ):
        self.client = pusher.channel( 'tetrapod.test' )
        super().setUp()


class Test_pusher_with_channel_test_mode( unittest.TestCase ):
    def setUp( self ):
        self.client = pusher.using( 'test_mode' ).channel( 'tetrapod.test' )
        super().setUp()


class Test_pusher_set_channel( unittest.TestCase ):
    def setUp( self ):
        self.client = pusher
        self.client_with_channel = pusher.channel( 'tetrapod.test' )
        super().setUp()

    def test_by_default_no_have_channel( self ):
        self.assertIsNone( self.client._channels )

    def test_set_channel_should_set_the_value( self ):
        self.assertEqual( self.client_with_channel._channels, 'tetrapod.test' )
        self.assertIsNone( self.client._channels )

    def test_set_channel_should_create_a_new_client( self ):
        self.assertIsNot( self.client_with_channel, self.client )

    def test_set_channel_should_have_the_same_connections( self ):
        self.assertIs(
            self.client_with_channel._connections, self.client._connections )

    def test_using_set_the_channels( self ):
        client = self.client_with_channel.using( 'default' )
        self.assertIsNot( client, self.client_with_channel )
        self.assertEqual(
            client._channels, self.client_with_channel._channels )


class Test_pusher_trigger( Test_pusher_with_channel ):
    def test_just_work( self ):
        result = self.client.trigger( 'test' )
        self.assertEqual( result, {} )

    @patch( 'pusher.Pusher.trigger' )
    def test_should_call_the_trigger_function( self, trigger ):
        self.client.trigger( 'test' )
        self.assertTrue( trigger.call_args_list )


class Test_pusher_trigger_in_test_mode( Test_pusher_with_channel_test_mode ):
    def test_just_work( self ):
        result = self.client.trigger( 'test' )
        self.assertEqual( result, {} )

    @patch( 'pusher.Pusher.trigger' )
    def test_should_no_call_the_trigger_function( self, trigger ):
        self.client.trigger( 'test' )
        self.assertFalse( trigger.call_args_list )
