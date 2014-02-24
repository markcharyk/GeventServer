Feature: Parse a client request
    Determine if the client is requesting a GET operation

    Scenario: Parse an allowed GET request
        Given the header GET /index.html HTTP/1.1
        When I call parse_request
        Then I see the output /index.html

    Scenario: Parse an unallowed POST request
        Given the header POST /index.html HTTP/1.1
        When I call parse_request
        Then I see the output 405 Error