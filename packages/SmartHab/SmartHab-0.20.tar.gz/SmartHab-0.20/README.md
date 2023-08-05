# python-smarthab
This Python library allows you to programmatically control your SmartHab-powered
home.

## Security warning!
SmartHab currently offers no secure connection to their API. The credentials are sent in clear-text. **You've been warned.**

## What is SmartHab?
[SmartHab](http://www.smarthab.fr) is a company that installs their home 
automation solution in new buildings, and offers a mobile application for 
home owners or renters to control their home over the Internet.

Mobile App → API → SmartHab box (1 at each floor) → Z-Wave devices

## What does this library do?
`python-smarthab` connects to the SmartHab API and allows you to automate your
home without having to use the mobile application.

It might prove particularly useful if integrated into a home automation box or
software. Feel free to use it, it's under the GPL!

## How do I use it?
```bash
pip3 install SmartHab
```

```python
import pysmarthab

hub = pysmarthab.SmartHab()

# Login
hub.login('smarthab.user@example.com', '1234567')

if not hub.is_logged_in:
    # Bad credentials :(
    raise SystemExit

# Get the list of available devices
devices = hub.get_device_list()

# Close all roller shutters and turn on all lights
for device in devices:
    if isinstance(device, pysmarthab.Light):
        device.turn_on()

    if isinstance(device, pysmarthab.Shutter):
        device.close()
```
