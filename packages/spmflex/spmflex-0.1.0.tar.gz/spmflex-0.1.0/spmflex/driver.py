"""
A Python driver for Honeywell's SPM Flex gas detector, using HTTP SOAP.

Distributed under the GNU General Public License v2
Copyright (C) 2019 NuMat Technologies
"""
import aiohttp
import xmltodict


class GasDetector(object):
    """Python driver for Honeywell SPM Flex Gas Detectors.

    This driver uses undocumented HTTP endpoints that are available through the
    Ethernet setting. This is much simpler than working with the Modbus
    TCP interface.
    """

    def __init__(self, address):
        """Save the IP address of the device."""
        if not address.startswith('http://'):
            address = 'http://' + address
        if not address.endswith('/'):
            address += '/'
        self.address = address

    async def __aenter__(self):
        """Support `async with` by entering a client session."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *err):
        """Support `async with` by exiting a client session."""
        await self.session.close()
        self.session = None

    async def get(self, raw=False):
        """Get current state from the SPM Flex gas detector.

        Args:
            raw: If True, returns all avaiable output
        Returns:
            Dictionary of sensor variables
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()
        endpoint = self.address + 'dyn/ContinuingStatus'
        async with self.session.get(endpoint) as response:
            if response.status > 200:
                return {'ip': self.address, 'connected': False}
            xml = await response.read()
        status = xmltodict.parse(xml)['ContinuingStatus']
        if raw:
            return status
        return {
            'ip': self.address,
            'connected': True,
            'concentration': float(status['Concentration']),
            'units': status['Units'],
            'flow': int(status['Flow'].rstrip('cc/min')),
            'gas': status['GasName'],
            'id': status['UnitID'].lstrip('Unit ID: '),
            'low-alarm threshold': status['Alarm1Setpoint'],
            'high-alarm threshold': status['Alarm2Setpoint'],
            'temperature': int(status['AmbientTemp'].rstrip('C')),
            'life': float(status['CCDaysRemaining'].split(' ')[-1]),
            'fault': 'Fault' if status['FaultDetails'] else 'No fault'
        }
