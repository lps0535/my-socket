# My-Socket

This is a toy-project (experimental) which reads from an arbitrary input from one socket and writes it to another socket. These sockets can be on two different machines or on the same machine.

**Note**: This program is not suitable for production environments in its current state.


## Usage

This section is divided into two parts: `Arguments` and `Message passing`.

### Arguments

You can run the program with a `-h` option to see all the arguments, positional and optional. Following is brief explanation of the arguments and their posotion:
```
usage: my_socket.py [-h] [--tcp] [--udp]
                    listener_port reciever_ip reciever_port

positional arguments:
  listener_port  An available port on local machine used to recieve messages.
  reciever_ip    IP address of the machine where messages will be sent.
  reciever_port  A port on the machine where messages will be sent. A copy of
                 this program must be listening on this port to send messages.

optional arguments:
  -h, --help     show this help message and exit
  --tcp          Send/Recieve messages through TCP protocol. This is the
                 default choice.
  --udp          Send/Recieve messages through UDP protocol. This option
                 overrides TCP, if provided.
```

### Message passing

To pass messages between two sockets, you need to run two instances of this program. You need to ensure that one socket is listening on the port other socket is sending messages to and vice versa. Use the following commands to run two instances of program, which will be able to successfully pass messages between each other:
```
python src/my_socket.py 9000 localhost 9001
python src/my_socket.py 9001 localhost 9000
```
In this example, both the sockets are located on the same machine. First socket is listening on port 9000 and sending to `localhost:9001` while second socket is listening on port 9001 and sending to `localhost:9000`.

If this step goes fine you should see a message like this: `Enter message to send. All messages recieved will be shown below. Type EXIT to end the program.` Now if you type a message from the first instance and hit enter, you should be able to see the message on the other instance. If something goes wrong, you should see a fairly descriptive eror message explaining the error and its possible causes.

Type `EXIT` to exit the program.


## Features

- **Multiple protocols**: It can send and recieve messages either via TCP or UDP which depends on user input. You can use the `--use-udp` option to use UDP instead of TCP, which is the default choice.
- **Robusteness**: It is very robust. We've used several layers of error handling and ensure that it will never hang up unexpectedly.
- **Tests**: Most part of the code is covered by tests.
- **Same socket messages**: You can even send and recieve on the same socket. For example, you can send as well as recieve messages on a port on your localhost, say 8000. This might not be very useful in a practial scenario but it demostrates the robusteness of the program.


## Limitations

- Currently, messages cannot contain newlines as we use that as end of input. but this should an easy problem to overcome, as we can use BEGIN and END identifiers to mark the begin and end of input.
- Also, it will only work for text messages at the moment.
- While most parts of the code are covered by tests, there still are some areas which need testing. The main problems in doing that are multiprocessing in the program and to test transmission across different machines.


## Tests

We're using [Nose tests](https://nose.readthedocs.org/en/latest/) to unit-test the program. All the tests are located in `my-socket/tests` directory. Currently we only `test_sockets.py` but we can add more in future, if required.

**Usage**: To run the tests, use the following command from `my-socket/tests` directory:
```
nosetests tests/
```
