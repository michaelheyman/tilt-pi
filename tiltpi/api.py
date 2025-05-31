"""API client for Tilt Pi."""

import asyncio
from typing import Final

import aiohttp

from tiltpi.errors import TiltPiConnectionError, TiltPiConnectionTimeoutError
from tiltpi.model import TiltColor, TiltHydrometerData

ENDPOINT_GET_ALL: Final = "/macid/all"


class TiltPiClient:
    """API client for Tilt Pi."""

    def __init__(
        self,
        host: str,
        port: int,
        session: aiohttp.ClientSession,
        timeout: int = 15,
    ) -> None:
        """Initialize the API client."""
        self._host = host
        self._port = port
        self._session = session
        self._timeout = aiohttp.ClientTimeout(total=timeout)

    async def get_hydrometers(self) -> list[TiltHydrometerData]:
        """Get all hydrometer data."""
        try:
            async with self._session.get(
                f"http://{self._host}:{self._port}{ENDPOINT_GET_ALL}",
                timeout=self._timeout,
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
        except asyncio.TimeoutError as err:
            raise TiltPiConnectionTimeoutError(
                f"Timeout while connecting to Tilt Pi at {self._host}"
            ) from err
        except aiohttp.ClientError as err:
            raise TiltPiConnectionError(
                f"Error connecting to Tilt Pi at {self._host}"
            ) from err

        return [
            TiltHydrometerData(
                mac_id=hydrometer["mac"],
                color=TiltColor(hydrometer["Color"].title()),
                temperature=float(hydrometer["Temp"]),
                gravity=float(hydrometer["SG"]),
            )
            for hydrometer in data
        ]
