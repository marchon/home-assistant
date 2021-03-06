"""
homeassistant.components.chromecast
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Provides functionality to interact with Chromecasts.
"""
import logging

try:
    import pychromecast
except ImportError:
    # Ignore, we will raise appropriate error later
    pass

from homeassistant.loader import get_component
import homeassistant.util as util
from homeassistant.helpers import extract_entity_ids
from homeassistant.const import (
    ATTR_ENTITY_ID, ATTR_FRIENDLY_NAME, SERVICE_TURN_OFF, SERVICE_VOLUME_UP,
    SERVICE_VOLUME_DOWN, SERVICE_MEDIA_PLAY_PAUSE, SERVICE_MEDIA_PLAY,
    SERVICE_MEDIA_PAUSE, SERVICE_MEDIA_NEXT_TRACK, SERVICE_MEDIA_PREV_TRACK)


DOMAIN = 'chromecast'
DEPENDENCIES = []

SERVICE_YOUTUBE_VIDEO = 'play_youtube_video'

ENTITY_ID_FORMAT = DOMAIN + '.{}'
STATE_NO_APP = 'idle'

ATTR_STATE = 'state'
ATTR_OPTIONS = 'options'
ATTR_MEDIA_STATE = 'media_state'
ATTR_MEDIA_CONTENT_ID = 'media_content_id'
ATTR_MEDIA_TITLE = 'media_title'
ATTR_MEDIA_ARTIST = 'media_artist'
ATTR_MEDIA_ALBUM = 'media_album'
ATTR_MEDIA_IMAGE_URL = 'media_image_url'
ATTR_MEDIA_VOLUME = 'media_volume'
ATTR_MEDIA_DURATION = 'media_duration'

MEDIA_STATE_UNKNOWN = 'unknown'
MEDIA_STATE_PLAYING = 'playing'
MEDIA_STATE_STOPPED = 'stopped'


def is_on(hass, entity_id=None):
    """ Returns true if specified ChromeCast entity_id is on.
    Will check all chromecasts if no entity_id specified. """

    entity_ids = [entity_id] if entity_id else hass.states.entity_ids(DOMAIN)

    return any(not hass.states.is_state(entity_id, STATE_NO_APP)
               for entity_id in entity_ids)


def turn_off(hass, entity_id=None):
    """ Will turn off specified Chromecast or all. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}

    hass.services.call(DOMAIN, SERVICE_TURN_OFF, data)


def volume_up(hass, entity_id=None):
    """ Send the chromecast the command for volume up. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}

    hass.services.call(DOMAIN, SERVICE_VOLUME_UP, data)


def volume_down(hass, entity_id=None):
    """ Send the chromecast the command for volume down. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}

    hass.services.call(DOMAIN, SERVICE_VOLUME_DOWN, data)


def media_play_pause(hass, entity_id=None):
    """ Send the chromecast the command for play/pause. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}

    hass.services.call(DOMAIN, SERVICE_MEDIA_PLAY_PAUSE, data)


def media_play(hass, entity_id=None):
    """ Send the chromecast the command for play/pause. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}

    hass.services.call(DOMAIN, SERVICE_MEDIA_PLAY, data)


def media_pause(hass, entity_id=None):
    """ Send the chromecast the command for play/pause. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}

    hass.services.call(DOMAIN, SERVICE_MEDIA_PAUSE, data)


def media_next_track(hass, entity_id=None):
    """ Send the chromecast the command for next track. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}

    hass.services.call(DOMAIN, SERVICE_MEDIA_NEXT_TRACK, data)


def media_prev_track(hass, entity_id=None):
    """ Send the chromecast the command for prev track. """
    data = {ATTR_ENTITY_ID: entity_id} if entity_id else {}

    hass.services.call(DOMAIN, SERVICE_MEDIA_PREV_TRACK, data)


def setup_chromecast(casts, host):
    """ Tries to convert host to Chromecast object and set it up. """

    # Check if already setup
    if any(cast.host == host for cast in casts.values()):
        return

    try:
        cast = pychromecast.PyChromecast(host)

        entity_id = util.ensure_unique_string(
            ENTITY_ID_FORMAT.format(
                util.slugify(cast.device.friendly_name)),
            casts.keys())

        casts[entity_id] = cast

    except pychromecast.ChromecastConnectionError:
        pass


def setup(hass, config):
    # pylint: disable=unused-argument,too-many-locals
    """ Listen for chromecast events. """
    logger = logging.getLogger(__name__)
    discovery = get_component('discovery')

    try:
        # pylint: disable=redefined-outer-name
        import pychromecast
    except ImportError:
        logger.exception(("Failed to import pychromecast. "
                          "Did you maybe not install the 'pychromecast' "
                          "dependency?"))

        return False

    casts = {}

    # If discovery component not loaded, scan ourselves
    if discovery.DOMAIN not in hass.components:
        logger.info("Scanning for Chromecasts")
        hosts = pychromecast.discover_chromecasts()

        for host in hosts:
            setup_chromecast(casts, host)

    def chromecast_discovered(service, info):
        """ Called when a Chromecast has been discovered. """
        logger.info("New Chromecast discovered: %s", info[0])
        setup_chromecast(casts, info[0])

    discovery.listen(
        hass, discovery.services.GOOGLE_CAST, chromecast_discovered)

    def update_chromecast_state(entity_id, chromecast):
        """ Retrieve state of Chromecast and update statemachine. """
        chromecast.refresh()

        status = chromecast.app

        state_attr = {ATTR_FRIENDLY_NAME:
                      chromecast.device.friendly_name}

        if status and status.app_id != pychromecast.APP_ID['HOME']:
            state = status.app_id

            ramp = chromecast.get_protocol(pychromecast.PROTOCOL_RAMP)

            if ramp and ramp.state != pychromecast.RAMP_STATE_UNKNOWN:

                if ramp.state == pychromecast.RAMP_STATE_PLAYING:
                    state_attr[ATTR_MEDIA_STATE] = MEDIA_STATE_PLAYING
                else:
                    state_attr[ATTR_MEDIA_STATE] = MEDIA_STATE_STOPPED

                if ramp.content_id:
                    state_attr[ATTR_MEDIA_CONTENT_ID] = ramp.content_id

                if ramp.title:
                    state_attr[ATTR_MEDIA_TITLE] = ramp.title

                if ramp.artist:
                    state_attr[ATTR_MEDIA_ARTIST] = ramp.artist

                if ramp.album:
                    state_attr[ATTR_MEDIA_ALBUM] = ramp.album

                if ramp.image_url:
                    state_attr[ATTR_MEDIA_IMAGE_URL] = ramp.image_url

                if ramp.duration:
                    state_attr[ATTR_MEDIA_DURATION] = ramp.duration

                state_attr[ATTR_MEDIA_VOLUME] = ramp.volume
        else:
            state = STATE_NO_APP

        hass.states.set(entity_id, state, state_attr)

    def update_chromecast_states(time):
        """ Updates all chromecast states. """
        if casts:
            logger.info("Updating Chromecast status")

            for entity_id, cast in casts.items():
                update_chromecast_state(entity_id, cast)

    def _service_to_entities(service):
        """ Helper method to get entities from service. """
        entity_ids = extract_entity_ids(hass, service)

        if entity_ids:
            for entity_id in entity_ids:
                cast = casts.get(entity_id)

                if cast:
                    yield entity_id, cast

        else:
            yield from casts.items()

    def turn_off_service(service):
        """ Service to exit any running app on the specified ChromeCast and
        shows idle screen. Will quit all ChromeCasts if nothing specified.
        """
        for entity_id, cast in _service_to_entities(service):
            cast.quit_app()
            update_chromecast_state(entity_id, cast)

    def volume_up_service(service):
        """ Service to send the chromecast the command for volume up. """
        for _, cast in _service_to_entities(service):
            ramp = cast.get_protocol(pychromecast.PROTOCOL_RAMP)

            if ramp:
                ramp.volume_up()

    def volume_down_service(service):
        """ Service to send the chromecast the command for volume down. """
        for _, cast in _service_to_entities(service):
            ramp = cast.get_protocol(pychromecast.PROTOCOL_RAMP)

            if ramp:
                ramp.volume_down()

    def media_play_pause_service(service):
        """ Service to send the chromecast the command for play/pause. """
        for _, cast in _service_to_entities(service):
            ramp = cast.get_protocol(pychromecast.PROTOCOL_RAMP)

            if ramp:
                ramp.playpause()

    def media_play_service(service):
        """ Service to send the chromecast the command for play/pause. """
        for _, cast in _service_to_entities(service):
            ramp = cast.get_protocol(pychromecast.PROTOCOL_RAMP)

            if ramp and ramp.state == pychromecast.RAMP_STATE_STOPPED:
                ramp.playpause()

    def media_pause_service(service):
        """ Service to send the chromecast the command for play/pause. """
        for _, cast in _service_to_entities(service):
            ramp = cast.get_protocol(pychromecast.PROTOCOL_RAMP)

            if ramp and ramp.state == pychromecast.RAMP_STATE_PLAYING:
                ramp.playpause()

    def media_next_track_service(service):
        """ Service to send the chromecast the command for next track. """
        for entity_id, cast in _service_to_entities(service):
            ramp = cast.get_protocol(pychromecast.PROTOCOL_RAMP)

            if ramp:
                next(ramp)
                update_chromecast_state(entity_id, cast)

    def play_youtube_video_service(service, video_id):
        """ Plays specified video_id on the Chromecast's YouTube channel. """
        if video_id:  # if service.data.get('video') returned None
            for entity_id, cast in _service_to_entities(service):
                pychromecast.play_youtube_video(video_id, cast.host)
                update_chromecast_state(entity_id, cast)

    hass.track_time_change(update_chromecast_states, second=range(0, 60, 15))

    hass.services.register(DOMAIN, SERVICE_TURN_OFF,
                           turn_off_service)

    hass.services.register(DOMAIN, SERVICE_VOLUME_UP,
                           volume_up_service)

    hass.services.register(DOMAIN, SERVICE_VOLUME_DOWN,
                           volume_down_service)

    hass.services.register(DOMAIN, SERVICE_MEDIA_PLAY_PAUSE,
                           media_play_pause_service)

    hass.services.register(DOMAIN, SERVICE_MEDIA_PLAY,
                           media_play_service)

    hass.services.register(DOMAIN, SERVICE_MEDIA_PAUSE,
                           media_pause_service)

    hass.services.register(DOMAIN, SERVICE_MEDIA_NEXT_TRACK,
                           media_next_track_service)

    hass.services.register(DOMAIN, "start_fireplace",
                           lambda service:
                           play_youtube_video_service(service, "eyU3bRy2x44"))

    hass.services.register(DOMAIN, "start_epic_sax",
                           lambda service:
                           play_youtube_video_service(service, "kxopViU98Xo"))

    hass.services.register(DOMAIN, SERVICE_YOUTUBE_VIDEO,
                           lambda service:
                           play_youtube_video_service(service,
                                                      service.data.get(
                                                          'video')))

    update_chromecast_states(None)

    return True
