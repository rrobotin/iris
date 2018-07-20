# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from platform import Platform
from util.core_helper import get_os, get_os_version
from util.parse_args import parse_args


DEFAULT_MIN_SIMILARITY = 0.8
DEFAULT_SLOW_MOTION_DELAY = 2
DEFAULT_MOVE_MOUSE_DELAY = parse_args().mouse
DEFAULT_OBSERVE_MIN_CHANGED_PIXELS = 50
DEFAULT_TYPE_DELAY = 0
DEFAULT_CLICK_DELAY = 0
DEFAULT_WAIT_SCAN_RATE = 3
DEFAULT_OBSERVE_SCAN_RATE = 3
DEFAULT_AUTO_WAIT_TIMEOUT = 3
DEFAULT_DELAY_BEFORE_MOUSE_DOWN = 0.3
DEFAULT_DELAY_BEFORE_DRAG = 0.3
DEFAULT_DELAY_BEFORE_DROP = 0.3
DEFAULT_FX_DELAY = 0.5
DEFAULT_UI_DELAY = 1
DEFAULT_UI_DELAY_LONG = 2.5
DEFAULT_SYSTEM_DELAY = 5


class _IrisSettings(object):

    def __init__(self):
        self._wait_scan_rate = DEFAULT_WAIT_SCAN_RATE
        self._type_delay = DEFAULT_TYPE_DELAY
        self._move_mouse_delay = DEFAULT_MOVE_MOUSE_DELAY
        self._click_delay = DEFAULT_CLICK_DELAY
        self._min_similarity = DEFAULT_MIN_SIMILARITY
        self._auto_wait_timeout = DEFAULT_AUTO_WAIT_TIMEOUT
        self._delay_before_mouse_down = DEFAULT_DELAY_BEFORE_MOUSE_DOWN
        self._delay_before_drag = DEFAULT_DELAY_BEFORE_DRAG
        self._delay_before_drop = DEFAULT_DELAY_BEFORE_DROP
        self._slow_motion_delay = DEFAULT_SLOW_MOTION_DELAY
        self._observe_scan_rate = DEFAULT_OBSERVE_SCAN_RATE
        self._observe_min_changed_pixels = DEFAULT_OBSERVE_MIN_CHANGED_PIXELS
        self._fx_delay = DEFAULT_FX_DELAY
        self._ui_delay = DEFAULT_UI_DELAY
        self._ui_delay_long = DEFAULT_UI_DELAY_LONG
        self._system_delay = DEFAULT_SYSTEM_DELAY

    @property
    def FX_DELAY(self):
        return self._fx_delay

    @FX_DELAY.setter
    def FX_DELAY(self, value):
        self._fx_delay = value

    @property
    def UI_DELAY(self):
        return self._ui_delay

    @UI_DELAY.setter
    def UI_DELAY(self, value):
        self._ui_delay = value

    @property
    def UI_DELAY_LONG(self):
        return self._ui_delay_long

    @UI_DELAY_LONG.setter
    def UI_DELAY_LONG(self, value):
        self._ui_delay_long = value

    @property
    def SYSTEM_DELAY(self):
        return self._system_delay

    @SYSTEM_DELAY.setter
    def SYSTEM_DELAY(self, value):
        self._system_delay = value

    @property
    def wait_scan_rate(self):
        return self._wait_scan_rate

    @wait_scan_rate.setter
    def wait_scan_rate(self, value):
        self._wait_scan_rate = value

    @property
    def type_delay(self):
        return self._type_delay

    @type_delay.setter
    def type_delay(self, value):
        if value > 1:
            self._type_delay = 1
        else:
            self._type_delay = value

    @property
    def move_mouse_delay(self):
        return self._move_mouse_delay

    @move_mouse_delay.setter
    def move_mouse_delay(self, value):
        self._move_mouse_delay = value

    @property
    def click_delay(self):
        return self._click_delay

    @click_delay.setter
    def click_delay(self, value):
        if value > 1:
            self._click_delay = 1
        else:
            self._click_delay = value

    @property
    def min_similarity(self):
        return self._min_similarity

    @min_similarity.setter
    def min_similarity(self, value):
        if value > 1:
            self._min_similarity = 1
        else:
            self._min_similarity = value

    @property
    def auto_wait_timeout(self):
        return self._auto_wait_timeout

    @auto_wait_timeout.setter
    def auto_wait_timeout(self, value):
        self._auto_wait_timeout = value

    @property
    def delay_before_mouse_down(self):
        return self._delay_before_mouse_down

    @delay_before_mouse_down.setter
    def delay_before_mouse_down(self, value):
        self._delay_before_mouse_down = value

    @property
    def delay_before_drag(self):
        return self._delay_before_drag

    @delay_before_drag.setter
    def delay_before_drag(self, value):
        self._delay_before_drag = value

    @property
    def delay_before_drop(self):
        return self._delay_before_drop

    @delay_before_drop.setter
    def delay_before_drop(self, value):
        self._delay_before_drop = value

    @property
    def slow_motion_delay(self):
        return self._slow_motion_delay

    @slow_motion_delay.setter
    def slow_motion_delay(self, value):
        self._slow_motion_delay = value

    @property
    def observe_scan_rate(self):
        return self._observe_scan_rate

    @observe_scan_rate.setter
    def observe_scan_rate(self, value):
        self._observe_scan_rate = value

    @property
    def observe_min_changed_pixels(self):
        return self._observe_min_changed_pixels

    @observe_min_changed_pixels.setter
    def observe_min_changed_pixels(self, value):
        self._observe_min_changed_pixels = value

    @staticmethod
    def get_os():
        """Get the type of the operating system your script is running on."""
        return get_os()

    @staticmethod
    def get_os_version():
        """Get the version string of the operating system your script is running on."""
        return get_os_version()

    @staticmethod
    def is_linux():
        """Checks if we are running on a Linux system.

        :return: True if we are running on a Linux system, False otherwise
        """
        return get_os() == Platform.LINUX

    @staticmethod
    def is_mac():
        """Checks if we are running on a Mac system.

        :return: True if we are running on a Mac system, False otherwise
        """
        return get_os() == Platform.MAC

    @staticmethod
    def is_windows():
        """Checks if we are running on a Windows system.

        :return: True if we are running on a Windows system, False otherwise
        """
        return get_os() == Platform.WINDOWS


Settings = _IrisSettings()