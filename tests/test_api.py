from unittest.mock import AsyncMock, Mock, patch

import aiohttp
import pytest
import pytest_asyncio

from tiltpi.api import TiltPiClient, TiltPiConnectionError, TiltPiConnectionTimeoutError
from tiltpi.model import TiltColor, TiltHydrometerData

TEST_HOST = "192.1.1.123"
TEST_PORT = 1880


@pytest_asyncio.fixture
async def mock_client_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


def make_mock_response(response_data):
    mock_response = AsyncMock()
    mock_response.raise_for_status = Mock(return_value=None)
    mock_response.json.return_value = response_data

    context_manager = AsyncMock()
    context_manager.__aenter__.return_value = mock_response
    context_manager.__aexit__.return_value = None
    return context_manager


@pytest.mark.asyncio
@patch.object(aiohttp.ClientSession, "get")
async def test_get_hydrometers_success(mock_get, mock_client_session):
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

    client = TiltPiClient(
        host=TEST_HOST,
        port=TEST_PORT,
        session=mock_client_session,
    )
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
async def test_get_hydrometers_timeout(mock_get, mock_client_session):
    """Test that a timeout error is raised."""
    mock_get.side_effect = TimeoutError("Timeout occurred")
    client = TiltPiClient(
        host=TEST_HOST,
        port=TEST_PORT,
        session=mock_client_session,
    )
    with pytest.raises(TiltPiConnectionTimeoutError):
        await client.get_hydrometers()


@pytest.mark.asyncio
@patch.object(aiohttp.ClientSession, "get")
async def test_get_hydrometers_connection_error(mock_get, mock_client_session):
    """Test that a connection error is raised."""
    mock_get.side_effect = aiohttp.ClientError("Connection error occurred")
    client = TiltPiClient(
        host=TEST_HOST,
        port=TEST_PORT,
        session=mock_client_session,
    )
    with pytest.raises(TiltPiConnectionError):
        await client.get_hydrometers()
