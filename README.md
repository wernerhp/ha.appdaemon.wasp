[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

<a href="https://www.buymeacoffee.com/wernerhp" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

# Wasp in a Box

## Introduction
Wasp in a Box is an AppDaemon app for detecting occupancy using door and motions sensors.

If the box (door) is open, we assume there is no wasp (person) in the box.  
If I see a wasp (motion), then there is a wasp in the box.  
If I close the box, then there is a wasp in the box.  
If the box has not been opened, we assume the wasp is still in the box.  
  
The state of the generated binary sensor can be used for triggering automations.

### Example
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
  name: Bathroom Occupancy
  door_sensors:
    - binary_sensor.bathroom_door_sensor
  motion_sensors:
    - binary_sensor.bathroom_motion_sensor
```

key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | The module name of the app.
`class` | False | string | | The name of the Class.
`name` | True | string | Defaults to the app name, e.g. Bathroom Wasp | The friendly_name of the sensor. 
`door_sensors` | False | list | | A list of door sensor entity_ids.
`motion_sensors` | False | list | | A list of motion sensor entity_ids.
