# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['netapi',
 'netapi.connector',
 'netapi.connector.eos',
 'netapi.connector.linux',
 'netapi.net',
 'netapi.net.eos',
 'netapi.probe',
 'netapi.probe.eos',
 'netapi.probe.ios',
 'netapi.probe.junos',
 'netapi.probe.linux',
 'netapi.probe.nxos',
 'netapi.probe.xe',
 'netapi.probe.xr']

package_data = \
{'': ['*']}

install_requires = \
['netaddr>=0.7.19,<0.8.0', 'pyeapi>=0.8.2,<0.9.0']

setup_kwargs = {
    'name': 'netapi',
    'version': '0.1.0',
    'description': 'Network API library. A programmatic interface to network devices',
    'long_description': '# NetAPI\n\nNetwork API library that perform the core of the work -> requests execution and data parsing.\n\nIt relies on the main vendor libraries to perform its work and its main objective to grant network objects that can be used with your applications.\n\n## Installation\n\nYou can directly install it using pip\n\n```\npip install netapi\n```\n\n## How it works\n\nHere is an example of how to use the library:\n\n```python\n# Use Arista pyeapi client for connection\nfrom netapi.connector.pyeapier import Device\nfrom netapi.net.pyeapier import Interface\n\nfrom pprint import pprint\n\n# Create a device connection object using its api https interface\nrouter01 = Device(\n    host="192.168.0.77",\n    username="someuser",\n    password="somepassword",\n    transport="https"\n)\n```\n\nShow device connection attributes, notice that secrets are hidden\n```python\nprint(router01)\n\nDevice(host=\'192.168.0.77\', username=\'someuser\', port=None, net_os=\'eos\', transport=\'https\')\n```\n\nYou can see the metadata for this instance and get information like timestamp, type of implementation, id of the instance, among other things:\n```python\nprint(router01.metadata)\n\nMetadata(name=\'device\', type=\'entity\', implementation=\'EOS-PYEAPI\', created_at=datetime.datetime(2019, 5, 14, 16, 47, 35, 319134), id=UUID(\'51d317ab-584d-4f32-a789-402770c361f2\'), updated_at=None, collection_count=0, parent=None)\n```\n\nYou can run a command/action and retrieve its output. The format would depend mostly of the device, net_os, implementation (like EOS-PYEAPI or raw SSH for example) and the type of command.\n```python\npprint(router01.run(\'show version\'))\n\n{\'show version\': {\'architecture\': \'i386\',\n                  \'bootupTimestamp\': 1557851831.0,\n                  \'hardwareRevision\': \'\',\n                  \'internalBuildId\': \'1a44ce37-92c4-48b6-b922-38b7eed939b6\',\n                  \'internalVersion\': \'4.21.5F-11604264.4215F\',\n                  \'isIntlVersion\': False,\n                  \'memFree\': 1372616,\n                  \'memTotal\': 2015608,\n                  \'mfgName\': \'\',\n                  \'modelName\': \'vEOS\',\n                  \'serialNumber\': \'\',\n                  \'systemMacAddress\': \'0c:59:30:85:d7:1d\',\n                  \'uptime\': 1158.4,\n                  \'version\': \'4.21.5F\'}}\n```\nThis library provides common handlers,  for well known network technologies. Here is an example for the Management 1 interface. Notice that I pass the device connector object:\n```python\nmgmt01 = Interface(name="Management1", connector=router01)\n\n# You can collect its attributes by running the get() method\nmgmt01.get()\n```\n\nYou can see its attributes. Since it is an interface I will only show some key ones\n```python\nprint(mgmt01)\n\nInterface(name=\'Management1\',\n          description=None,\n          enabled=True,\n          status_up=True,\n          status=\'UP\',\n          last_status_change=datetime.datetime(2019, 5, 14, 17, 38, 45, 217419),\n          number_status_changes=4,\n          forwarding_model=\'routed\',\n          physical=InterfacePhysical(mtu=1500,\n              bandwidth=1000000000,\n              duplex=\'duplexFull\',\n              mac=EUI(\'0C-59-30-C7-EE-00\')),\n          optical=InterfaceOptical(tx=None, rx=None, status=None),\n          addresses=InterfaceIP(ipv4=IPNetwork(\'10.193.7.142/24\'),\n              ipv6=None,\n              secondary_ipv4=[],\n              dhcp=None),\n          instance=\'default\',\n          counters=InterfaceCounters(rx_bits_rate=1728.866885299387,\n              tx_bits_rate=246.67962344503712,\n              rx_pkts_rate=4.007927363735154,\n              tx_pkts_rate=0.23434463850156687,\n              ...\n              tx_errors_tx_pause=0.0),\n          members=None,\n          last_clear=None,\n          counter_refresh=datetime.datetime(2019, 5, 14, 17, 43, 38, 787766), update_interval=300.0)\n```\n\nThere are multiple parameters here but and I ommitted othere but you can see that IP addresses are netaddr IPNetwork object and similarly the MAC addresses are EUI objects. Also the counter_refresh interval are datetime objects.\n\nThese instances also have metadata\n```python\nprint(mgmt01.metadata)\n\nMetadata(name=\'interface\', type=\'entity\', implementation=\'EOS-PYEAPI\', created_at=datetime.datetime(2019, 5, 14, 16, 43, 44, 819105), id=UUID(\'73297adf-a0d6-4f8d-b247-0d793e577efb\'), updated_at=datetime.datetime(2019, 5, 14, 16, 43, 54, 483277), collection_count=1, parent=None)\n```\n\nYou can see that in the metadata the updated_at field is populated? This happened because we invoked the get() method to collect the data. Now let\'s change the interface description and refresh the interface data (this is done outside of the script)\n\nAssuming a change to the description was done, now retrieve again the data\n```python\nprint(mgmt01.description)\n\nDUMMY DESCRIPTION\n```\n\nYou can see that the description changes but also the metadata has been updated!\n```python\nprint(mgmt01.metadata)\n\nMetadata(name=\'interface\', type=\'entity\', implementation=\'EOS-PYEAPI\', created_at=datetime.datetime(2019, 5, 14, 16, 43, 44, 819105), id=UUID(\'73297adf-a0d6-4f8d-b247-0d793e577efb\'), updated_at=datetime.datetime(2019, 5, 14, 17, 20, 27, 557810), collection_count=2, parent=None)\n```\nYou can see updated_at has been updated :) and the collection_count has increased to 2\n\n',
    'author': 'David Flores',
    'author_email': 'davidflores7_8@hotmail.com',
    'url': 'https://gitlab.com/the-networkers/netaudithor/netapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
