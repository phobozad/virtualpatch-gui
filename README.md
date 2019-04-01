# virtualpatch-gui
Frontend for building a virtual patch panel based on IOS-XE devices

Note: this is very early code in development and is not production ready.

## Requirements
 - Python 3.5+
 - Bottle
 - Requests
 - Router/Switch running IOS-XE that supports VPWS using AToM (e.g. Cat3850, Cat9k)

## Installation

Follow standard git clone process & virtualenv creation:

```
git clone https://github.com/phobozad/virtualpatch-gui.git
cd virtualpatch-gui
python3 -m venv vpg
source vpg/bin/activate
pip install -r requirements.txt
```

## Usage
### Device Configuration
RestConf on the switch/router needs to be enabled (for Catalyst switches this requires 16.8.1 or newer).  RestConf requires HTTPS and AAA new-model authentication.

	Switch#conf t
	Switch(config)#aaa new-model
	Switch(config)#aaa authentication login default local
	Switch(config)#aaa authorization exec default local 
	Switch(config)#ip http authentication aaa
	Switch(config)#ip http secure-server
	Switch(config)#restconf
	Switch(config)#end
	Switch#wr mem

Note that the device has to support VPWS using Any Transport over MPLS (AToM) - this includes Catalyst 3850 and certain Catalyst 9k platforms running newer code as well as IOS-XE routers that support the feature/licensing.  Testing is primarily done against 


### Application Configuration
The switch/router IP/Hostname and authentication credentials are configured in config.json.  Currently only one device is supported.

### Starting the app
Currently the code has only been tested using the built-in Bottle development web server.

For non-debug use, bind to a network interface, disable debugging, and disable the auto-reloader functionality in run.py.  Then run run.py to start the web server. Alternatively, use with a WSGI compatible web server.

	python run.py

When done running app, use Ctrl+C on the CLI to stop the web server.

### Hiding network interfaces
Any interface on the device with a description starting with `$$NoVPP` will be ignored by the app when trying to create/edit virtual patches.  This should be used on management or other key ports that are not used as general patch panel ports.

### Labeling network interfaces
Each Port can be labled for easy identification of what is getting patched together.  The labels in the app are pulled from the physical interface descriptions on the device.

### Patching devices together
With current functionality, any two devices plugged into the same logical device (router/switch) can be virtually patched together without moving any physical cables.

To connect two devices:
 1. Add a patch
 2. Provide a unique identifier for this patch.  This ID can't be changed after initial creation.
 3. Select the two interfaces to connect as the "A-Side" and "Z-Side".  Note that the order of does not matter.
 4. Save the new patch

If you get a success message after saving then the two devices should see each other as if they were directly connected.  This includes Layer2 control protocols like CDP.

Note: Currently only GigabitEthernet ports are exposed in the App.  This will be configurable in future versions, but is hard-coded today.  In the future, a configuration setting will allow control what types of ports to expose in the UI and look for on the device. (e.g. "GigabitEthernet", "TenGigabitEthernet", etc.).

### Changing a pair of cross-connected ports
When a "patch" has been created to connect two ports, this patch/cross-connect should be deleted before attempting to re-use the same ports for a different pairing.  Failure to do so may result in de-sync of the router's running configuration and NetConf/RestConf configuration datastore.

## License
Licensed under the Zlib license

Copyright (c) 2019 Chris Burger

This software is provided 'as-is', without any express or implied
warranty. In no event will the authors be held liable for any damages
arising from the use of this software.

Permission is granted to anyone to use this software for any purpose,
including commercial applications, and to alter it and redistribute it
freely, subject to the following restrictions:

   1. The origin of this software must not be misrepresented; you must not
   claim that you wrote the original software. If you use this software
   in a product, an acknowledgment in the product documentation would be
   appreciated but is not required.

   2. Altered source versions must be plainly marked as such, and must not be
   misrepresented as being the original software.

   3. This notice may not be removed or altered from any source
   distribution.
