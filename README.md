[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

<a href="https://www.buymeacoffee.com/wernerhp" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: auto !important;width: auto !important;" ></a>

# Wasp in a Box

## Introduction
Wasp in a Box is an [AppDaemon](https://github.com/hassio-addons/addon-appdaemon) app for detecting occupancy using multiple sensors.

### Wasp
The wasp is a person or entity detected by a motion or presence sensor.  

### Box
The box is a room or area with one or more door sensors.  

### How it works
- If we see a wasp, then there is a wasp in the box.  
- If we close the box while there is a wasp in the box, then the wasp remains in the box.
- If the box remains closed when there is a wasp in the box, and the wasp stops moving, we assume it's still in the box.  
- If the box is opened, and the wasp is not moving, we assume that the wasp has escaped (there is no wasp in the box).  

The state of the generated binary sensor can be used for triggering automations.

### Example:
If someone enters the bathroom and motion is detected, then turn on the light.  
If the door is closed and motion is detected, then keep the light on as long as the door is closed.  
If the door is open and no motion is detected, then turn off the light.  

# Prerequisites
- [Home Assistant](https://www.home-assistant.io/) 
- [AppDaemon](https://github.com/hassio-addons/addon-appdaemon)
  - [An important note](https://github.com/hassio-addons/addon-appdaemon/issues/287#issuecomment-1815365717) on breaking changes in 0.15.0+
- [HACS](https://hacs.xyz/) for easy installation

# Installation
- Go to HACS ❯ Automation ❯ + Explore & Download Repositories
- Search for "Wasp in a Box" and Download
- Wasp in a Box will be installed to `/config/appdaemon/wasp`   
- Configure the `wasp` module in `/config/appdaemon/apps/apps.yaml`  

## Example
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

## Configuration
key | optional | type | default | description
-- | -- | -- | -- | --
`module` | False | string | | The module name of the app.
`class` | False | string | | The name of the Class.
`device_class` | True | string | occupancy | The device class of the binary sensor.
`name` | True | string | Defaults to the app name, e.g. Bathroom Wasp | The friendly_name of the sensor. 
`delay` | True | int | 0 | The number of seconds after closing the box before a wasp will be detected.
`box_sensors` | False | list | | A list of sensor entity_ids, e.g. door sensors.
`wasp_sensors` | False | list | | A list of sensor entity_ids, e.g. motion sensors.
