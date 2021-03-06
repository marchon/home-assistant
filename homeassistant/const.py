""" Constants used by Home Assistant components. """
# Can be used to specify a catch all when registering state or event listeners.
MATCH_ALL = '*'

# If no name is specified
DEVICE_DEFAULT_NAME = "Unnamed Device"

# #### CONFIG ####
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"

# This one is deprecated. Use platform instead.
CONF_TYPE = "type"

CONF_PLATFORM = "platform"
CONF_HOST = "host"
CONF_HOSTS = "hosts"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_API_KEY = "api_key"
CONF_ACCESS_TOKEN = "access_token"

# #### EVENTS ####
EVENT_HOMEASSISTANT_START = "homeassistant_start"
EVENT_HOMEASSISTANT_STOP = "homeassistant_stop"
EVENT_STATE_CHANGED = "state_changed"
EVENT_TIME_CHANGED = "time_changed"
EVENT_CALL_SERVICE = "call_service"
EVENT_SERVICE_EXECUTED = "service_executed"
EVENT_PLATFORM_DISCOVERED = "platform_discovered"

# #### STATES ####
STATE_ON = 'on'
STATE_OFF = 'off'
STATE_HOME = 'home'
STATE_NOT_HOME = 'not_home'
STATE_UNKNOWN = "unknown"
STATE_OPEN = 'open'
STATE_CLOSED = 'closed'

# #### STATE AND EVENT ATTRIBUTES ####
# Contains current time for a TIME_CHANGED event
ATTR_NOW = "now"

# Contains domain, service for a SERVICE_CALL event
ATTR_DOMAIN = "domain"
ATTR_SERVICE = "service"

# Data for a SERVICE_EXECUTED event
ATTR_SERVICE_CALL_ID = "service_call_id"

# Contains one string or a list of strings, each being an entity id
ATTR_ENTITY_ID = 'entity_id'

# String with a friendly name for the entity
ATTR_FRIENDLY_NAME = "friendly_name"

# A picture to represent entity
ATTR_ENTITY_PICTURE = "entity_picture"

# The unit of measurement if applicable
ATTR_UNIT_OF_MEASUREMENT = "unit_of_measurement"

# Temperature attribute
ATTR_TEMPERATURE = "temperature"

# #### MISC ####
TEMP_CELCIUS = "°C"
TEMP_FAHRENHEIT = "°F"

# Contains the information that is discovered
ATTR_DISCOVERED = "discovered"

# #### SERVICES ####
SERVICE_HOMEASSISTANT_STOP = "stop"

SERVICE_TURN_ON = 'turn_on'
SERVICE_TURN_OFF = 'turn_off'

SERVICE_VOLUME_UP = "volume_up"
SERVICE_VOLUME_DOWN = "volume_down"
SERVICE_VOLUME_MUTE = "volume_mute"
SERVICE_MEDIA_PLAY_PAUSE = "media_play_pause"
SERVICE_MEDIA_PLAY = "media_play"
SERVICE_MEDIA_PAUSE = "media_pause"
SERVICE_MEDIA_NEXT_TRACK = "media_next_track"
SERVICE_MEDIA_PREV_TRACK = "media_prev_track"

# #### API / REMOTE ####
SERVER_PORT = 8123

AUTH_HEADER = "X-HA-access"

URL_API = "/api/"
URL_API_STATES = "/api/states"
URL_API_STATES_ENTITY = "/api/states/{}"
URL_API_EVENTS = "/api/events"
URL_API_EVENTS_EVENT = "/api/events/{}"
URL_API_SERVICES = "/api/services"
URL_API_SERVICES_SERVICE = "/api/services/{}/{}"
URL_API_EVENT_FORWARD = "/api/event_forwarding"
URL_API_COMPONENTS = "/api/components"
