"""Support for custom shell commands to turn a light on/off."""
import logging
import subprocess

import voluptuous as vol

from homeassistant.components.light import (
	LightEntity,
	ENTITY_ID_FORMAT,
	PLATFORM_SCHEMA,
)
from homeassistant.const import (
	CONF_FRIENDLY_NAME,
	CONF_LIGHTS,
	CONF_HOST,
	CONF_PORT,
)
import homeassistant.helpers.config_validation as cv

from . import DATA_DEVICE_REGISTER, KConnection

_LOGGER = logging.getLogger(__name__)

LIGHTS_SCHEMA = vol.Schema(
	{
		vol.Optional(CONF_FRIENDLY_NAME): cv.string,
		vol.Optional("k_id"): cv.string,
	}
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
	{
		vol.Required(CONF_HOST): cv.string,
		vol.Optional(CONF_PORT, default=4196): cv.port,
		vol.Required(CONF_LIGHTS): cv.schema_with_slug_keys(LIGHTS_SCHEMA)
	}
)


def setup_platform(hass, config, add_entities, discovery_info=None):
	devices = config.get(CONF_LIGHTS, {})
	lights = []

	host = config.get(CONF_HOST, {})
	port = config.get(CONF_PORT, {})
	address = (host, port)
	transport = hass.data[DATA_DEVICE_REGISTER]
	transport.setAddress(address)

	for object_id, device_config in devices.items():

		lights.append(
			CommandLight(
				hass,
				object_id,
				device_config.get(CONF_FRIENDLY_NAME, object_id),
				device_config.get("k_id"),
				transport,
			)
		)

	if not lights:
		_LOGGER.error("No lights added")
		return False

	add_entities(lights)


class CommandLight(SwitchEntity):
	def __init__(
		self,
		hass,
		object_id,
		friendly_name,
		k_id,
		transport,
	):
		self._hass = hass
		self.entity_id = ENTITY_ID_FORMAT.format(object_id)
		self._name = friendly_name
		self._state = False
		self._k_id = k_id
		self._clinet = KConnection(transport, k_id)

	@property
	def should_poll(self):
		"""Only poll if we have state command."""
		return True

	@property
	def name(self):
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
