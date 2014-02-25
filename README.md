GeventServer
============
This is an HTTP Server designed to handle only GET requests for files kept in a "webroot" directory. Anything else will throw an error.
This server uses GEvent to handle increased loads of traffic (i.e. more than one connection at a time). See requirements.txt file for the required installations of GEvent and other modules.

Testing is handled by a combination of Python's unittest module and lettuce.
