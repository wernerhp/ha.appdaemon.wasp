[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

<a href="https://www.buymeacoffee.com/wernerhp" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

# Wasp in a Box

## Introduction
Wasp in a Box is an AppDaemon app for detecting occupancy using multiple sensors.

If the box (door sensor) is open, we assume there is no wasp (person) in the box.  
If we see a wasp (motion sensor), then there is a wasp in the box.  
If we close the box, then there is a wasp in the box.  
If the box has not been opened, we assume the wasp is still in the box.  
  
The state of the generated binary sensor can be used for triggering automations.

### Example:
If someone enters the bathroom and motion is detected, then turn on the light.  
If the door is closed and motion is detected, then keep the light on as long as the door is closed.  
If the door is open and no motion is detected, then turn off the light.  

## Installation
Download the `wasp` directory from inside the `apps` directory to your local `apps` directory, then configure the `wasp` module in `apps.yaml`.

## App configuration
```yaml
bathroom_wasp:
  module: wasp
  class: Wasp
  device_class: occupancy
  name: Bathroom Occupancy
  delay: 5
  box_sensors:
    - binary_sensor.bathroom_door_sensor
  wasp_sensors:
    - binary_sensor.bathroom_motion_sensor
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | The module name of the app.
`class` | False | string | | The name of the Class.
`device_class` | True | string | occupancy | The device class of the binary sensor.
`name` | True | string | Defaults to the app name, e.g. Bathroom Wasp | The friendly_name of the sensor. 
`delay` | True | int | 0 | The number of seconds after closing the box before a wasp will be detected.
`box_sensors` | False | list | | A list of sensor entity_ids, e.g. door sensors.
`wasp_sensors` | False | list | | A list of sensor entity_ids, e.g. motion sensors.
