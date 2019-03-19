# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os

from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
import Xlib.XK

import logging

logger = logging.getLogger(__name__)


class XKeyboard(object):

    def __init__(self):
        self.display = Display(os.environ['DISPLAY'])

    def keyDown(self, key):
        logger.info('KEY_DOWN')
        logger.debug('KEY :')
        logger.debug(key)
        """
        Performs a keyboard key press without the release. This will put that
        key in a held down state.
    
        Args:
          key (str): The key to be pressed down. The valid names are listed in
          Key class
    
        Returns:
          None
        """

        logger.debug('I type(key) %s: ' % type(key))
        if self.keyboardMapping(key) is None:
            return

        logger.debug('II type(key) %s: ' % type(key))
        if type(key) == int:
            fake_input(self.display, X.KeyPress, key)
            self.display.sync()
            return

        needsShift = isShiftCharacter(key)
        if needsShift:
            fake_input(self.display, X.KeyPress, self.keyboardMapping('shift'))

        fake_input(self.display, X.KeyPress, self.keyboardMapping(key))

        if needsShift:
            fake_input(self.display, X.KeyRelease, self.keyboardMapping('shift'))
        self.display.sync()

    def keyUp(self, key):
        logger.info('KEY_UP')
        logger.debug('KEY :')
        logger.debug(key)
        """
        Performs a keyboard key release (without the press down beforehand).
    
        Args:
          key (str): The key to be released up. The valid names are listed in
          Key Class
    
        Returns:
          None
        """

        logger.debug('I type(key) %s: ' % type(key))
        if self.keyboardMapping(key) is None:
            return

        logger.debug('II type(key) %s: ' % type(key))
        if type(key) == int:
            keycode = key
        else:
            keycode = self.keyboardMapping(key)

        logger.debug('keycode %s: ' % keycode)

        fake_input(self.display, X.KeyRelease, keycode)
        self.display.sync()

    def keyboardMapping(self, iriskey):
        logger.debug('keyboardMapping')
        logger.debug(Xlib.XK.string_to_keysym(iriskey))
        return self.display.keysym_to_keycode(Xlib.XK.string_to_keysym(iriskey))

    def _screen_size(self):
        """
            Returns:
                 Screen Width and Height of the virtual screen
        """

        return self.display.screen().width_in_pixels, self.display.screen().height_in_pixels


def isShiftCharacter(character):
    """
    Returns True if the key character is uppercase or shifted.
    """
    logger.debug('isShiftCharacter')
    return character.isupper() or character in '~!@#$%^&*()_+{}|:"<>?'
