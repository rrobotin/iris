import time

import logging

from iris.api.core.keyboard.Xkeyboard import XKeyboard
from iris.api.core.keyboard.key import KeyModifier, _IrisKey, logger
from iris.api.core.keyboard.keyboard_api import DEFAULT_KEY_SHORTCUT_DELAY
from iris.api.core.platform import Platform
from iris.api.core.settings import Settings, DEFAULT_TYPE_DELAY

logger = logging.getLogger(__name__)


fake_Keyboard = XKeyboard()


def virtual_type(text=None, modifier=None, interval=None):
    """
    :param str || list text: If a string, then the characters to be pressed. If a list, then the key names of the keys
                             to press in order.
    :param modifier: Key modifier.
    :param interval: The number of seconds in between each press. By default it is 0 seconds.
    :return: None.
    """
    logger.debug('type method: ')
    logger.debug(isinstance(text, _IrisKey))
    logger.debug(type(text))
    logger.debug('text : %s' % text)

    logger.debug('type modifier: ')
    logger.debug(isinstance(modifier, KeyModifier))
    logger.debug(type(modifier))
    logger.debug('modifier : %s' % modifier)

    if modifier is None:

        if isinstance(text, _IrisKey):
            logger.debug('Scenario 1: reserved key.')
            logger.debug('Reserved key: %s' % text)
            fake_Keyboard.keyDown(str(text))
            fake_Keyboard.keyUp(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
        else:
            if interval is None:
                interval = Settings.type_delay

            logger.debug('Scenario 2: normal key or text block.')
            logger.debug('Text: %s' % text)
            XKeyboard.typewrite(text, interval)
    else:
        logger.debug('Scenario 3: combination of modifiers and other keys.')
        modifier_keys = KeyModifier.get_active_modifiers(modifier)
        num_keys = len(modifier_keys)
        logger.debug('Modifiers (%s): %s ' % (num_keys, ' '.join(modifier_keys)))
        logger.debug('text: %s' % text)
        if num_keys == 1:
            fake_Keyboard.keyDown(str(modifier_keys[0]))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            fake_Keyboard.keyDown(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            fake_Keyboard.keyUp(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            fake_Keyboard.keyUp(modifier_keys[0])
        elif num_keys == 2:
            fake_Keyboard.keyDown(modifier_keys[0])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            fake_Keyboard.keyDown(modifier_keys[1])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            fake_Keyboard.keyDown(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            fake_Keyboard.keyUp(str(text))
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            fake_Keyboard.keyUp(modifier_keys[1])
            time.sleep(DEFAULT_KEY_SHORTCUT_DELAY)
            fake_Keyboard.keyUp(modifier_keys[0])
        else:
            logger.error('Returned key modifiers out of range.')

    if Settings.type_delay != DEFAULT_TYPE_DELAY:
        Settings.type_delay = DEFAULT_TYPE_DELAY


def new_tab_virtual():
    """Open a new browser tab."""
    if Settings.get_os() == Platform.MAC:
        virtual_type(text='t', modifier=KeyModifier.CMD)
    else:
        virtual_type(text='t', modifier=KeyModifier.CTRL)
    # Wait to allow new tab to be opened.
    time.sleep(Settings.FX_DELAY)
