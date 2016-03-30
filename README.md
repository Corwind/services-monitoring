# Services Monitoring

This project is divided in two parts, a server and a client.

## The server
It exposes a http server which on a GET request on /query returns the states
of services as configured in a yaml file.

## The client
The client is a simple django app that shows the states of all machines it is
configured to poll.
