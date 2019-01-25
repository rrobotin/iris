# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Session restore can be performed from a new window'
        self.test_case_id = 'C117040'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        hamburger_menu_button_pattern = NavBar.HAMBURGER_MENU
        restore_previous_session_pattern = HamburgerMenu.RESTORE_PREVIOUS_SESSION

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        website_one_loaded = exists(LocalWeb.FIREFOX_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, website_one_loaded, 'Page 1 successfully loaded, firefox logo found.')

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        website_two_loaded = exists(LocalWeb.MOZILLA_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, website_two_loaded, 'Page 2 successfully loaded, mozilla logo found.')

        restart_firefox(self, self.browser.path, self.profile_path, self.base_local_web_url)

        click(hamburger_menu_button_pattern, DEFAULT_UI_DELAY)

        restore_previous_session_located = exists(restore_previous_session_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, restore_previous_session_located,
                    'The "Hamburger" menu is successfully displayed. "Restore previous session" menu item located')
        click(restore_previous_session_pattern)

        select_tab(4)
        website_one_loaded = exists(LocalWeb.MOZILLA_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, website_one_loaded, 'Page 1 successfully restored from previous session.')

        select_tab(3)
        website_two_loaded = exists(LocalWeb.FIREFOX_LOGO, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, website_two_loaded, 'Page 2 successfully restored from previous session.')


