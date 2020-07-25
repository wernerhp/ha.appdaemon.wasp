"""
Wasp in a Box app for detecting occupancy.
"""

import json
import time
import hassapi as hass
import mqttapi as mqtt
import voluptuous as vol

from datetime import datetime

MODULE = 'wasp'
CLASS = 'Wasp'

CONF_DOOR_SENSORS = 'door_sensors'
CONF_MOTION_SENSORS = 'motion_sensors'
CONF_NAME = 'name'

class Wasp(hass.Hass):

  def initialize(self):
    """Initialize the Wasp app."""
    self.door_sensors = self.args.get(CONF_DOOR_SENSORS, [])
    self.motion_sensors = self.args.get(CONF_MOTION_SENSORS, [])

    self.wasp_id = "binary_sensor.{name}".format(name=self.name)
    self.friendly_name = self.args.get("name", self.name.replace("_", " ").title())

    self.sensors = self.door_sensors + self.motion_sensors

    handles = []
    handle = self.listen_event(self.state_changed_callback, "state_changed")
    handles.append(handle)

  def state_changed_callback(self, event, data, kwargs):	
    """Handle state change events."""
    if data.get("entity_id") not in self.sensors:
      return

    self.last_state = self.get_state(self.wasp_id, default="off")

    box_empty = self.last_state == "off"

    if self.box_state() == "open":
      if box_empty and self.detect_wasp():
        self.update_box_state(data=data, wasp=True)
      elif not box_empty and not self.detect_wasp():
        self.update_box_state(data=data, wasp=False)
    else: # closed
      if box_empty and self.detect_wasp():
        self.update_box_state(data=data, wasp=True)

  def box_state(self):
    """Returns whether the box is open or closed."""
    for entity_id in self.door_sensors:
      box_state = self.get_state(entity_id, attribute="state", default="off")
      if box_state == "on":
        return "open"
    return "closed"

  def detect_wasp(self):
    """Detect if there's a wasp in the box."""
    wasp = False
    for entity_id in self.motion_sensors:
      motion_sensor_state = self.get_state(entity_id, attribute="state", default="off") # no motion
      if motion_sensor_state == "on": # motion detected
        wasp = True
        break
    return wasp

  def update_box_state(self, data, wasp=False):
    """Update the box state."""
    state = "on" if wasp else "off"
    last_changed = datetime.fromisoformat(data.get("new_state").get("last_changed"))
    last_changed = last_changed.replace(microsecond=0)
    self.last_state = self.set_state(self.wasp_id, state=state, attributes={
        "last_changed": last_changed.isoformat(), 
        "entity_id": data.get("new_state").get("entity_id"),
        "device_class": "occupancy",
        "friendly_name": self.friendly_name,
        }
      )
