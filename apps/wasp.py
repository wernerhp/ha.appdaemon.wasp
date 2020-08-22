"""
Wasp in a Box app for detecting occupancy using multiple sensors.
"""

import json
import time
import hassapi as hass

from datetime import datetime

MODULE = 'wasp'
CLASS = 'Wasp'

ATTR_STATE = "state"

CONF_DEVICE_CLASS = 'device_class'
CONF_NAME = 'name'
CONF_DELAY = 'delay'
CONF_BOX_SENSORS = 'box_sensors'
CONF_WASP_SENSORS = 'wasp_sensors'
CONF_DOOR_SENSORS = 'door_sensors' # deprecated. use box_sensors.
CONF_MOTION_SENSORS = 'motion_sensors' # deprecated. use wasp_sensors.

STATE_WASP = "on"
STATE_NO_WASP = "off"
STATE_BOX_OPEN = "on"
STATE_BOX_CLOSED = "off"
STATE_WASP_IN_BOX = "on"
STATE_NO_WASP_IN_BOX = "off"

class Wasp(hass.Hass):

  def initialize(self):
    """Initialize the Wasp app."""
    self.wasp_entity = "binary_sensor.{name}".format(name=self.name)
    self.device_class = self.args.get(CONF_DEVICE_CLASS, "occupancy")
    self.friendly_name = self.args.get(CONF_NAME, self.name.replace("_", " ").title())

    self.delay = self.args.get(CONF_DELAY, 0)
    self.box_sensors = self.args.get(CONF_BOX_SENSORS, []) + self.args.get(CONF_DOOR_SENSORS, [])
    self.wasp_sensors = self.args.get(CONF_WASP_SENSORS, []) + self.args.get(CONF_MOTION_SENSORS, [])

    self.state = STATE_NO_WASP_IN_BOX
    self.wasp_in_a_box(box_state=STATE_BOX_OPEN, wasp_state=STATE_NO_WASP)

    for entity_id in self.box_sensors:
      self.listen_state(self.handle_box_state, entity_id, attribute=ATTR_STATE)

    for entity_id in self.wasp_sensors:
      self.listen_state(self.handle_wasp_state, entity_id, attribute=ATTR_STATE)

  def handle_box_state(self, entity, attribute, old, new, kwargs):
    """Handle box state change."""
    if self.delay:
      self.state = STATE_NO_WASP_IN_BOX
    self.run_in(self.wasp_in_a_box_cb, self.delay, box_state=new, entity=entity)

  def handle_wasp_state(self, entity, attribute, old, new, kwargs):
    """Handle wasp state change."""
    self.run_in(self.wasp_in_a_box_cb, 0, wasp_state=new, entity=entity)

  def wasp_in_a_box_cb(self, kwargs):
    """Wasp in a Box callback"""
    box_state = kwargs.get("box_state", self.box_state())
    wasp_state = kwargs.get("wasp_state", self.wasp_state())
    entity = kwargs.get("entity")

    self.wasp_in_a_box(box_state=box_state, wasp_state=wasp_state, entity=entity)

  def wasp_in_a_box(self, box_state, wasp_state, entity=None, **kwargs):
    """Set Wasp in a Box state."""
    if wasp_state == STATE_WASP:
      self.state = STATE_WASP_IN_BOX
    if wasp_state == STATE_NO_WASP and box_state == STATE_BOX_OPEN:
      self.state = STATE_NO_WASP_IN_BOX
    if wasp_state == STATE_NO_WASP and box_state == STATE_BOX_CLOSED:
      self.state = self.state

    self.set_state(self.wasp_entity, state=self.state, attributes={
        "device_class": self.device_class,
        "friendly_name": self.friendly_name,
        "last_changed": self.datetime().replace(microsecond=0).isoformat(), 
        "entity_id": entity,
        "box": box_state,
        "wasp": wasp_state,
      }
    )

  def box_state(self):
    """Return if the box is open or closed."""
    for entity_id in self.box_sensors:
      state = self.get_state(entity_id, attribute=ATTR_STATE, default=STATE_BOX_CLOSED, copy=False)
      if state == STATE_BOX_OPEN:
        return STATE_BOX_OPEN
    return STATE_BOX_CLOSED

  def wasp_state(self):
    """Return if there's a wasp or not."""
    for entity_id in self.wasp_sensors:
      state = self.get_state(entity_id, attribute=ATTR_STATE, default=STATE_NO_WASP, copy=False)
      if state == STATE_WASP:
        return STATE_WASP
    return STATE_NO_WASP
