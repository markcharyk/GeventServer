from lettuce import step
from lettuce import world
from http_server import build_response


@step('a code of (\d+)')
def a_code(step, code):
    world.code = int(code)


@step('I build the response')
def call_build_response(step):
    world.response = build_response(world.code, "placeholder data")


@step('I receive (.+)')
def compare(step, expected):
    assert world.response == expected, "Got %s" % world.response
