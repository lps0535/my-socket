from multiprocessing import Process, Queue
import argparse
import socket
import sys
import time
import os


##############################################################################
# UDP implementation
##############################################################################
def sender_udp(out_socket, fileno):
    """ Create a udp socket and read arbitrary input which is sent to
        reciever. """
    sys.stdin = os.fdopen(fileno)

    print "Enter message to send. All messages recieved will be shown below. Type EXIT to end the program."
    while 1:
        data = raw_input()
        if data=="EXIT":
            sys.exit(0)
        elif data:
            cs = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            cs.sendto(data, out_socket)
            time.sleep(1)
    cs.close()


def listener_udp(in_socket):
    """ UDP listener which receives message from another socket."""

    ss = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    graceful_bind(ss, in_socket)
    while 1:
        # recieve data on in_socket which was sent by sender_udp()
        data=ss.recv(2048)
        print("Message received: %s" % data)

    ss.close()



##############################################################################
# TCP implementation
##############################################################################
def sender_tcp(out_socket, fileno):
    """ Create a socket and read arbitrary input which is sent to
        reciever."""
    sys.stdin = os.fdopen(fileno)

    print "Enter message to send. All messages recieved will be shown below. Type EXIT to end the program."
    while 1:
        data = raw_input()
        tcp_connect_send(data, out_socket)

def listener_tcp(in_socket):
    """ TCP listener which receives message from another socket."""

    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    graceful_bind(ss, in_socket)
    ss.listen(1)
    while 1:
        con, addr = ss.accept()
        data      = con.recv(2048)
        print("Message received: %s" % data)
        con.close()
    ss.close()


## Helper Functions
def tcp_connect_send(data, conn_socket):
    """ Connects to socket and send data to the appropriate reciever."""
    if data == "EXIT":
        sys.exit(0)
    elif data:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(conn_socket)
            s.send(data)
            s.close()
        except Exception:
            print 'ERROR: Connection to specified socket "%s" cannot be established. Either IP "%s" is not reachable or port "%d" is not available.\nPlease try again after the destination socket is listening on the specified port.' % (conn_socket, conn_socket[0], conn_socket[1])

def graceful_bind(ss, socket):
    """ Binds to socket else show the error"""
    try:
        ss.bind(socket)
    except Exception as e:
        print 'ERROR: Connection to specified socket "%s" cannot be established.Either IP "%s" is not reachable or port "%d" is not available.Complete error message is:\n%s\nABORTING!!' % (socket, socket[0],
        socket[1], str(e))
        raise

def initiate_processes(out_socket, in_socket, use_udp=False):
    """ Initiate two different processes sender_process and listener_process."""
    sender_function = sender_udp if use_udp else sender_tcp
    listener_function = listener_udp if use_udp else listener_tcp

    try:
        fileno = sys.stdin.fileno()
        sender_process = Process(target=sender_function, args=((out_socket),
            fileno))
        listener_process = Process(target=listener_function,
                args=((in_socket),))
        sender_process.start()
        listener_process.start()
        return (sender_process, listener_process)
    except Exception as e:
        print "\nERROR: Unable to start listener/sender processes. Complete error message: %s\nABORTING!!\n" % (str(e))

def check_processess(sender_process, listener_process):
    """ Checks whether both sender/listener processes are alive simulatneously, if not  then this will terminate both."""
    while 1:
        if not sender_process.is_alive() or not listener_process.is_alive():
            sender_process.terminate()
            listener_process.terminate()
            break

def main():
    # Creates Sender, Listener and verification as Threads for UDP and TCP.
    parser = argparse.ArgumentParser()
    parser.add_argument("listener_port", type=int, help="An available port on local machine used to recieve messages.")
    parser.add_argument("reciever_ip", help="IP address of the machine where messages will be sent.")
    parser.add_argument("reciever_port", type=int, help="A port on the machine where messages will be sent. A copy of this program must be listening on this port to send messages.")
    parser.add_argument("--tcp", action="store_true", help="Send/Recieve messages through TCP protocol. This is the default choice.")
    parser.add_argument("--udp", action="store_true", help="Send/Recieve messages through UDP protocol. This option overrides TCP, if provided.")
    args = parser.parse_args()
    out_socket = ('localhost', args.listener_port)
    in_socket = (args.reciever_ip, args.reciever_port)
    use_udp = True if args.udp else False

    (sender_process, listener_process) = initiate_processes(out_socket, in_socket, use_udp)
    check_processess(sender_process, listener_process)

if __name__=='__main__':
    main()
