from lettuce import step
from lettuce import world
from http_server import parse_request, MethodNotAllowedError


@step('the header (.+)')
def a_request(step, header):
    world.header = header


@step('I call parse_request')
def call_parse_request(step):
    try:
        world.cmd = parse_request(world.header)
    except MethodNotAllowedError:
        world.cmd = "405 Error"


@step('I see the output (.+)')
def compare(step, expected):
    assert world.cmd == expected, "Got %s" % world.cmd
