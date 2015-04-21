"""
    @TODO: Update this.
    Tests parse functions used in screenshot directive.

    Usage: Run `nosetests tests/test_parse_commands.py` to run just this file or
    `nosetests tests` to run all tests from files inside 'tests' directory.
    Either of the two commands must be run from the 'sphinx-docs' directory.
"""

from nose.tools import assert_equal, raises, with_setup
import os
import sys
from mock import patch

sys.path.insert(0, os.path.abspath(os.path.join('src')))
import my_socket

@raises(Exception)
def test_invalid_port():
    """ Test to ensure that listener cannot bind to an invalid port. Must raise
    an exception."""
    in_socket = ('localhost', 1)
    my_socket.listener_tcp(in_socket)

def test_exit():
    """Test to ensure that if user at one socket enters EXIT, socket closes"""
    with patch('my_socket.sys.exit') as exit_mock:
        # Declare two sockets and initiate sender/listener processes.
        # @TODO: Change the tests to pick random free ports as 9000/90001 might not
        # be free.

        # Test with different sender/listener ports.
        in_socket = ('localhost', 9000)
        out_socket = ('localhost', 9001)
        (sender_process, listener_process) = my_socket.initiate_processes(out_socket, in_socket)
        # Send a test message.
        my_socket.tcp_connect_send("EXIT", out_socket)
        # Ensure that my_socket called sys.exit()
        assert exit_mock.called

        # Terminate processes
        sender_process.terminate()
        listener_process.terminate()

def test_local_message_send():
    """Test to ensure that messages are exchanged on a local machine."""
    # Declare two sockets and initiate sender/listener processes. Ensure that
    # an instance of program is listenig on port 9001.
    # @TODO: Change the tests to pick random free ports as 9000/90001 might not
    # be free.

    # Test with different sender/listener ports.
    in_socket = ('localhost', 9000)
    out_socket = ('localhost', 9001)
    (sender_process, listener_process) = my_socket.initiate_processes(out_socket, in_socket)
    # Send a test message.
    my_socket.tcp_connect_send("Test message", out_socket)

    # Terminate processes
    sender_process.terminate()
    listener_process.terminate()

def test_remote_message_send():
    """Test to ensure that messages are exchanged on different machines."""
    # Declare two sockets and initiate sender/listener processes.
    # @TODO: Need to figure out how to run this program on two different IP
    # addresses and test on those.

    in_socket = ('localhost', 9000)
    out_socket = ('<remote-ip>', 9001)
    (sender_process, listener_process) = my_socket.initiate_processes(out_socket, in_socket)
    # Send a test message.
    my_socket.tcp_connect_send("Test message", out_socket)
    # Assert that the recieved message is same as the sent message. This assert
    # currently does not works properly due to mutli-processing in my_socket.

    # Terminate processes
    sender_process.terminate()
    listener_process.terminate()
