from unittest.mock import AsyncMock, patch

import aiohttp
import pytest

from tiltpi.api import TiltPiClient, TiltPiConnectionError, TiltPiConnectionTimeoutError
from tiltpi.model import TiltColor, TiltHydrometerData

TEST_HOST = "192.1.1.123"
TEST_PORT = 1880


def make_mock_response(response_data):
    mock_response = AsyncMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = response_data

    context_manager = AsyncMock()
    context_manager.__aenter__.return_value = mock_response
    context_manager.__aexit__.return_value = None
    return context_manager


@pytest.mark.asyncio
@patch.object(aiohttp.ClientSession, "get")
async def test_get_hydrometers_success(mock_get):
    """Test successful fetch of hydrometer data using a patch decorator."""
    response = [
        {
            "mac": "00:11:22:33:44:55",
            "Color": "blue",
            "Temp": 70,
            "SG": 1.012,
        },
        {
            "mac": "AA:BB:CC:DD:EE:FF",
            "Color": "red",
            "Temp": 68,
            "SG": 1.015,
        },
    ]

    mock_get.return_value = make_mock_response(response)

    client = TiltPiClient(TEST_HOST, TEST_PORT, aiohttp.ClientSession())
    result = await client.get_hydrometers()
    assert len(result) == 2
    assert isinstance(result[0], TiltHydrometerData)
    assert result[0].mac_id == "00:11:22:33:44:55"
    assert result[0].color == TiltColor.BLUE
    assert result[0].temperature == 70.0
    assert result[0].gravity == 1.012
    assert isinstance(result[1], TiltHydrometerData)
    assert result[1].mac_id == "AA:BB:CC:DD:EE:FF"
    assert result[1].color == TiltColor.RED
    assert result[1].temperature == 68.0
    assert result[1].gravity == 1.015


@pytest.mark.asyncio
@patch.object(aiohttp.ClientSession, "get")
async def test_get_hydrometers_timeout(mock_get):
    """Test that a timeout error is raised."""
    mock_get.side_effect = TimeoutError("Timeout occurred")
    client = TiltPiClient(TEST_HOST, TEST_PORT, aiohttp.ClientSession())
    with pytest.raises(TiltPiConnectionTimeoutError):
        await client.get_hydrometers()


@pytest.mark.asyncio
@patch.object(aiohttp.ClientSession, "get")
async def test_get_hydrometers_connection_error(mock_get):
    """Test that a connection error is raised."""
    mock_get.side_effect = aiohttp.ClientError("Connection error occurred")
    client = TiltPiClient(TEST_HOST, TEST_PORT, aiohttp.ClientSession())
    with pytest.raises(TiltPiConnectionError):
        await client.get_hydrometers()
