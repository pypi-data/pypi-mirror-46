# NetAPI

Network API library that perform the core of the work -> requests execution and data parsing.

It relies on the main vendor libraries to perform its work and its main objective to grant network objects that can be used with your applications.

## Installation

You can directly install it using pip

```
pip install netapi
```

## How it works

Here is an example of how to use the library:

```python
# Use Arista pyeapi client for connection
from netapi.connector.pyeapier import Device
from netapi.net.pyeapier import Interface

from pprint import pprint

# Create a device connection object using its api https interface
router01 = Device(
    host="192.168.0.77",
    username="someuser",
    password="somepassword",
    transport="https"
)
```

Show device connection attributes, notice that secrets are hidden
```python
print(router01)

Device(host='192.168.0.77', username='someuser', port=None, net_os='eos', transport='https')
```

You can see the metadata for this instance and get information like timestamp, type of implementation, id of the instance, among other things:
```python
print(router01.metadata)

Metadata(name='device', type='entity', implementation='EOS-PYEAPI', created_at=datetime.datetime(2019, 5, 14, 16, 47, 35, 319134), id=UUID('51d317ab-584d-4f32-a789-402770c361f2'), updated_at=None, collection_count=0, parent=None)
```

You can run a command/action and retrieve its output. The format would depend mostly of the device, net_os, implementation (like EOS-PYEAPI or raw SSH for example) and the type of command.
```python
pprint(router01.run('show version'))

{'show version': {'architecture': 'i386',
                  'bootupTimestamp': 1557851831.0,
                  'hardwareRevision': '',
                  'internalBuildId': '1a44ce37-92c4-48b6-b922-38b7eed939b6',
                  'internalVersion': '4.21.5F-11604264.4215F',
                  'isIntlVersion': False,
                  'memFree': 1372616,
                  'memTotal': 2015608,
                  'mfgName': '',
                  'modelName': 'vEOS',
                  'serialNumber': '',
                  'systemMacAddress': '0c:59:30:85:d7:1d',
                  'uptime': 1158.4,
                  'version': '4.21.5F'}}
```
This library provides common handlers,  for well known network technologies. Here is an example for the Management 1 interface. Notice that I pass the device connector object:
```python
mgmt01 = Interface(name="Management1", connector=router01)

# You can collect its attributes by running the get() method
mgmt01.get()
```

You can see its attributes. Since it is an interface I will only show some key ones
```python
print(mgmt01)

Interface(name='Management1',
          description=None,
          enabled=True,
          status_up=True,
          status='UP',
          last_status_change=datetime.datetime(2019, 5, 14, 17, 38, 45, 217419),
          number_status_changes=4,
          forwarding_model='routed',
          physical=InterfacePhysical(mtu=1500,
              bandwidth=1000000000,
              duplex='duplexFull',
              mac=EUI('0C-59-30-C7-EE-00')),
          optical=InterfaceOptical(tx=None, rx=None, status=None),
          addresses=InterfaceIP(ipv4=IPNetwork('10.193.7.142/24'),
              ipv6=None,
              secondary_ipv4=[],
              dhcp=None),
          instance='default',
          counters=InterfaceCounters(rx_bits_rate=1728.866885299387,
              tx_bits_rate=246.67962344503712,
              rx_pkts_rate=4.007927363735154,
              tx_pkts_rate=0.23434463850156687,
              ...
              tx_errors_tx_pause=0.0),
          members=None,
          last_clear=None,
          counter_refresh=datetime.datetime(2019, 5, 14, 17, 43, 38, 787766), update_interval=300.0)
```

There are multiple parameters here but and I ommitted othere but you can see that IP addresses are netaddr IPNetwork object and similarly the MAC addresses are EUI objects. Also the counter_refresh interval are datetime objects.

These instances also have metadata
```python
print(mgmt01.metadata)

Metadata(name='interface', type='entity', implementation='EOS-PYEAPI', created_at=datetime.datetime(2019, 5, 14, 16, 43, 44, 819105), id=UUID('73297adf-a0d6-4f8d-b247-0d793e577efb'), updated_at=datetime.datetime(2019, 5, 14, 16, 43, 54, 483277), collection_count=1, parent=None)
```

You can see that in the metadata the updated_at field is populated? This happened because we invoked the get() method to collect the data. Now let's change the interface description and refresh the interface data (this is done outside of the script)

Assuming a change to the description was done, now retrieve again the data
```python
print(mgmt01.description)

DUMMY DESCRIPTION
```

You can see that the description changes but also the metadata has been updated!
```python
print(mgmt01.metadata)

Metadata(name='interface', type='entity', implementation='EOS-PYEAPI', created_at=datetime.datetime(2019, 5, 14, 16, 43, 44, 819105), id=UUID('73297adf-a0d6-4f8d-b247-0d793e577efb'), updated_at=datetime.datetime(2019, 5, 14, 17, 20, 27, 557810), collection_count=2, parent=None)
```
You can see updated_at has been updated :) and the collection_count has increased to 2

