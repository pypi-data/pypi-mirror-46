# WolkGatewayModule-SDK-Python

Python 3 package for connecting devices to WolkAbout IoT Platform through [WolkGateway](https://github.com/Wolkabout/WolkGateway).

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


## Requirements

* Python 3.7

All requirements for this project can be installed on Debian based systems by invoking:
```console
sudo apt-get install python3.7 python3-pip && python3 -m pip install pip && python3.7 -m pip install pip
```

## Installation

The project can be installed using Python's package manager pip:
```console
sudo python3.7 -m pip install wolk-gateway-module
```

or installed from source by cloning the repository and running:

```console
sudo python3.7 -m pip install -r requirements.txt
python3.7 setup.py install
```


## Example Usage

### Creating devices

```python
import wolk_gateway_module as wolk

# Create device sensors

# Use data_type parameter where reading type & unit symbol are not important
generic_sensor = wolk.SensorTemplate(
    name="Generic sensor",
    reference="G",  # References must be unique per device
    data_type=wolk.DataType.NUMERIC,
    description="Optional description",
    minimum=0,  # Optional minimum value
    maximum=100,  # Optional maximum value
)
temperature_sensor = wolk.SensorTemplate(
    name="Temperature",
    reference="T",
    reading_type_name=wolk.ReadingTypeName.TEMPERATURE,
    unit=wolk.ReadingTypeMeasurementUnit.CELSIUS,
    minimum=-20,
    maximum=85,
    description="Temperature sensor with range -20 to 85 Celsius",
)
# Create a device template used to register the device
device_template = wolk.DeviceTemplate(
    sensors=[generic_sensor, temperature_sensor]
)
# Create a device
device = wolk.Device(
    name="Device",
    key="DEVICE_KEY",  # Unique device key
    template=device_template
)
```

### Establishing connection with WolkGateway

```python
# Implement a device status provider


def get_device_status(device_key: str) -> wolk.DeviceStatus:
    """Return current device status."""
    if device_key == "DEVICE_KEY":
        # Handle getting current device status here
        return wolk.DeviceStatus.CONNECTED


wolk_module = wolk.Wolk(
    host="localhost",  # Host address of WolkGateway
    port=1883,  # TCP/IP port used for WolkGateway's MQTT broker
    module_name="Python module",  # Used for connection authentication
    device_status_provider=get_device_status,
)

wolk_module.connect()
```

### Disconnecting from WolkGateway

```python
wolk_module.disconnect()
```

### Adding devices

Devices need to be registered on the Platform before their data is considered valid.
This is achieved by calling:
```python
wolk_module.add_device(device)
```
To stop listening for commands for a specific device use:
```python
wolk_module.remove_device(device)
```
This will only stop acknowledging inbound commands, to delete the device completely use WolkGateway or the web application, depending on who has control over devices.

### Publishing device status
Device status is obtained by calling provided `device_status_provider` function
```python
wolk_module.publish_device_status("DEVICE_KEY")
```

### Adding sensor readings

```python
wolk_module.add_sensor_reading("DEVICE_KEY", "REFERENCE", "value")
# For reading with data size > 1, like location or acceleration use tuples
wolk_module.add_sensor_reading("DEVICE_KEY", "LOC", (24.534, -34.325))
# Add timestamps to store when reading occurred to preserve history, otherwise
# Platform will assign timestamp when it receives the reading
wolk_module.add_sensor_reading("KEY", "R", 12, int(round(time.time() * 1000)))
```

This method will put serialized messages in storage.

### Publishing stored messages

```python
wolk_module.publish()  # Publish all stored messages
wolk_module.publish("DEVICE_KEY")  # Publish all stored messages for device
```

### Alarms
```python
humidity_alarm = wolk.AlarmTemplate(
    name="High Humidity",
    reference="HH",
    description="High humidity has been detected"
)
device_template = wolk.DeviceTemplate(alarms=[humidity_alarm])

# Create device, Wolk instance, add device, connect...

# Will place alarm message into storage, use publish method to send
wolk_module.add_alarm("DEVICE_KEY", "HH", active=True, timestamp=None)
```

### Actuators

In order to control device actuators, provide an `actuation_handler` and `actuator_status_provider`.

```python
switch_actuator = wolk.ActuatorTemplate(
    name="Switch",
    reference="SW",
    data_type=wolk.DataType.BOOLEAN,
    description="Light switch",
)
slider_actuator = wolk.ActuatorTemplate(
    name="Slider",
    reference="SL",
    data_type=wolk.DataType.NUMERIC,
    minimum=0,
    maximum=100,
    description="Light dimmer",
)
device_template = wolk.DeviceTemplate(
    actuators=[switch_actuator, slider_actuator]
)
device = wolk.Device("Device", "DEVICE_KEY", device_template)


def handle_actuation(
    device_key: str, reference: str, value: Union[bool, int, float, str]
) -> None:
    """
    Set device actuator identified by reference to value.

    Must be implemented as non blocking.
    Must be implemented as thread safe.
    """
    if device_key == "DEVICE_KEY":
        if reference == "SW":
            # Handle setting the value here
            switch.value = value

        elif reference == "SL":
            slider.value = value


def get_actuator_status(
    device_key: str, reference: str
) -> Tuple[wolk.ActuatorState, Union[bool, int, float, str]]:
    """
    Get current actuator status identified by device key and reference.

    Reads the status of actuator from the device
    and returns it as a tuple containing the actuator state and current value.

    Must be implemented as non blocking.
    Must be implemented as thread safe.
    """
    if device_key == "DEVICE_KEY":
        if reference == "SW":
            # Handle getting current actuator value here
            return wolk.ActuatorState.READY, switch.value

        elif reference == "SL":
            return wolk.ActuatorState.READY, slider.value


# Pass functions to Wolk instance
wolk_module = wolk.Wolk(
    host="localhost",
    port=1883,
    module_name="Python module",
    device_status_provider=get_device_status,
    actuation_handler=handle_actuation,
    acutator_status_provider=get_actuator_status,
)

wolk_module.add_device(device)

wolk_module.connect()

# This method will call the provided actuator_status_provider function
# and publish the state immediately or store message if unable to publish
wolk_module.publish_acutator_status("DEVICE_KEY", "SW")
wolk_module.publish_acutator_status("DEVICE_KEY", "SL")
```

### Configurations

Similar to actuators, using device configuration options requires providing a `configuration_handler` and a `configuration_provider` to the `Wolk` instance.

```python
logging_level_configuration = wolk.ConfigurationTemplate(
    name="Logging level",
    reference="LL",
    data_type=wolk.DataType.STRING,
    default_value="INFO",
    description="eg. Set device logging level",
)
logging_interval_configuration = wolk.ConfigurationTemplate(
    name="Logging interval",
    reference="LI",
    data_type=wolk.DataType.NUMERIC,
    size=3,
    labels=["seconds", "minutes", "hours"],
    description="eg. Set logging intervals",
)
device_template = wolk.DeviceTemplate(
    configurations=[logging_level_configuration, logging_level_configuration]
)
device = wolk.Device("Device", "DEVICE_KEY", device_template)


def get_configuration(
    device_key: str
) -> Dict[
    str,
    Union[
        int,
        float,
        bool,
        str,
        Tuple[int, int],
        Tuple[int, int, int],
        Tuple[float, float],
        Tuple[float, float, float],
        Tuple[str, str],
        Tuple[str, str, str],
    ],
]:
    """
    Get current configuration options.

    Reads device configuration and returns it as a dictionary
    with device configuration reference as key,
    and device configuration value as value.
    Must be implemented as non blocking.
    Must be implemented as thread safe.
    """
    if device_key == "DEVICE_KEY":
        # Handle getting configuration values here
        return {
            "LL": get_log_level(),
            "LI": get_log_inteval(),
        }


def handle_configuration(
    device_key: str,
    configuration: Dict[
        str,
        Union[
            int,
            float,
            bool,
            str,
            Tuple[int, int],
            Tuple[int, int, int],
            Tuple[float, float],
            Tuple[float, float, float],
            Tuple[str, str],
            Tuple[str, str, str],
        ],
    ],
) -> None:
    """
    Change device's configuration options.

    Must be implemented as non blocking.
    Must be implemented as thread safe.
    """
    if device_key == "DEVICE_KEY":
        for reference, value in configuration.items():
            # Handle setting configuration values here
            if reference == "LL":
                set_log_level(value)
            elif reference == "LI":
                set_log_interval(value)


# Pass functions to Wolk instance
wolk_module = wolk.Wolk(
    host="localhost",
    port=1883,
    module_name="Python module",
    device_status_provider=get_device_status,
    configuration_provider=get_configuration,
    configuration_handler=handle_configuration,
)

wolk_module.add_device(device)

wolk_module.connect()

# This method will call the provided configuration_provider function
# and publish the state immediately or store message if unable to publish
wolk_module.publish_configuration("DEVICE_KEY")
```

### Firmware update
In order to enable firmware update for devices, provide an implementation of `FirmwareHandler` and pass to `Wolk` instance.

```python

device_template = wolk.DeviceTemplate(supports_firmware_update=True)
device = wolk.Device("Device", "DEVICE_KEY", device_template)


class FirmwareHandlerImplementation(wolk.FirmwareHandler):
    """Handle firmware installation and abort commands, and report version.

    Once an object of this class is passed to a Wolk object,
    it will set callback methods `on_install_success` and
    `on_install_fail` used for reporting the result of
    the firmware update process. Use these callbacks in `install_firmware`
    and `abort_installation` methods."""

    def install_firmware(
        self, device_key: str, firmware_file_path: str
    ) -> None:
        """
        Handle the installation of the firmware file.

        Call `self.on_install_success(device_key)` to report success.
        Reporting success will also get new firmware version.

        If installation fails, call `self.on_install_fail(device_key, status)`
        where:
        `status = FirmwareUpdateStatus(
            FirmwareUpdateState.ERROR,
            FirmwareUpdateErrorCode.INSTALLATION_FAILED
        )`
        or use other values from `FirmwareUpdateErrorCode` if they fit better.
        """
        if device_key == "DEVICE_KEY":
            print(
                f"Installing firmware: '{firmware_file_path}' "
                f"on device '{device_key}'"
            )
            # Handle the actual installation here
            if install_success:
                self.on_install_success(device_key)
            else:
                status = wolk.FirmwareUpdateStatus(
                    wolk.FirmwareUpdateState.ERROR,
                    wolk.FirmwareUpdateErrorCode.INSTALLATION_FAILED,
                )
                self.on_install_fail(device_key, status)

    def abort_installation(self, device_key: str) -> None:
        """
        Attempt to abort the firmware installation process for device.

        Call `self.on_install_fail(device_key, status)` to report if
        the installation process was able to be aborted with
        `status = FirmwareUpdateStatus(FirmwareUpdateState.ABORTED)`
        If unable to stop the installation process, no action is required.
        """
        if device_key == "DEVICE_KEY":
            # Manage to stop firmware installation
            status = wolk.FirmwareUpdateStatus(
                wolk.FirmwareUpdateState.ABORTED
            )
            self.on_install_fail(device_key, status)

    def get_firmware_version(self, device_key: str) -> str:
        """Return device's current firmware version."""
        if device_key == "DEVICE_KEY":
            # Handle getting the current firmware version here
            return version


wolk_module = wolk.Wolk(
    host="localhost",
    port=1883,
    module_name="Python module",
    device_status_provider=get_device_status,
    firmware_handler=FirmwareHandlerImplementation(),
)

wolk_module.add_device(device)

wolk_module.connect()
```

### Debugging

Enable debug logging with:
```python
wolk.logging_config("debug", log_file=None)
```

### Data persistence

Data persistence mechanism used **by default** stored messages in-memory.
In cases when provided in-memory persistence is suboptimal, it it possible to use custom persistence by implementing `OutboundMessageQueue` and passing it in the following manner:
```python
wolk_module = wolk.Wolk(
    host="localhost",
    port=1883,
    module_name="Python module",
    device_status_provider=get_device_status,
    outbound_message_queue=CustomPersistence()
)
```
