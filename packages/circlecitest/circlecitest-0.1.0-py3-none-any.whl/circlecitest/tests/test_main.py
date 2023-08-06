import ipaddress
import sys
from io import StringIO

import pytest

from circlecitest.main import get_ip, print_result


@pytest.mark.asyncio
async def test_get_ip():
    result = await get_ip()
    assert isinstance(result, str)
    assert isinstance(ipaddress.ip_address(result), ipaddress.IPv4Address)


def test_print_result():
    captured_output = StringIO()
    sys.stdout = captured_output

    value = 'some string'

    result = print_result(value)
    assert result is None
    assert f'Your IP is {value}\n' == captured_output.getvalue()
