"""Support for custom shell commands to turn a switch on/off."""
import logging
import subprocess

import voluptuous as vol

from homeassistant.components.switch import (
	ENTITY_ID_FORMAT,
	PLATFORM_SCHEMA,
	SwitchDevice,
)
from homeassistant.const import (
	CONF_FRIENDLY_NAME,
	CONF_SWITCHES,
	CONF_HOST,
	CONF_PORT,
)
import homeassistant.helpers.config_validation as cv

from . import DATA_DEVICE_REGISTER, DATA_DEVICE_REGISTER_LOCK, KConnection

_LOGGER = logging.getLogger(__name__)

SWITCH_SCHEMA = vol.Schema(
	{
		vol.Optional(CONF_FRIENDLY_NAME): cv.string,
		vol.Optional("k_id"): cv.string,
	}
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
	{
		vol.Required(CONF_HOST): cv.string,
		vol.Optional(CONF_PORT, default=4196): cv.port,
		vol.Required(CONF_SWITCHES): cv.schema_with_slug_keys(SWITCH_SCHEMA)
	}
)


def setup_platform(hass, config, add_entities, discovery_info=None):
	"""Find and return switches controlled by shell commands."""
	devices = config.get(CONF_SWITCHES, {})
	switches = []

	try:
		_LOGGER.warning(config.get(CONF_HOST, {}))
		_LOGGER.warning(config.get(CONF_PORT, {}))
	except:
		_LOGGER.warning("fail")


	for object_id, device_config in devices.items():

		switches.append(
			CommandSwitch(
				hass,
				object_id,
				device_config.get(CONF_FRIENDLY_NAME, object_id),
				device_config.get("k_id"),
			)
		)

	if not switches:
		_LOGGER.error("No switches added")
		return False

	add_entities(switches)


class CommandSwitch(SwitchDevice):
	"""Representation a switch that can be toggled using shell commands."""

	def __init__(
		self,
		hass,
		object_id,
		friendly_name,
		k_id,
	):
		"""Initialize the switch."""
		self._hass = hass
		self.entity_id = ENTITY_ID_FORMAT.format(object_id)
		self._name = friendly_name
		self._state = False
		self._k_id = k_id
		self._clinet = KConnection(hass.data[DATA_DEVICE_REGISTER], k_id, hass.data[DATA_DEVICE_REGISTER_LOCK])

	@property
	def should_poll(self):
		"""Only poll if we have state command."""
		return True

	@property
	def name(self):
		"""Return the name of the switch."""
		return self._name

	@property
	def is_on(self):
		"""Return true if device is on."""
		return self._state

	@property
	def assumed_state(self):
		"""Return true if we do optimistic updates."""
		return False

	def update(self):
		self._state = self._clinet.getStatus()

	def turn_on(self, **kwargs):
		self._clinet.turnOn()

	def turn_off(self, **kwargs):
		self._clinet.turnOff()