# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Width, height and position of each window are restored.'
        self.window_size = None
        self.test_case_id = '114826'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        hamburger_menu_button_pattern = NavBar.HAMBURGER_MENU
        firefox_test_site_tab_pattern = LocalWeb.FIREFOX_TAB_ICON_TEXT
        mozilla_test_site_tab_pattern = LocalWeb.MOZILLA_TAB_ICON_TEXT
        restore_previous_session_pattern = HamburgerMenu.RESTORE_PREVIOUS_SESSION
        iris_pattern = Pattern('iris_tab.png')
        console_output_height_500 = Pattern('console_output_height_500.png')
        console_output_width_500 = Pattern('console_output_width_500.png')
        console_output_height_400 = Pattern('console_output_height_400.png')
        console_output_width_600 = Pattern('console_output_width_600.png')
        console_output_width_1000 = Pattern('console_output_width_1000.png')

        if not Settings.is_mac():
            hamburger_menu_quit_item_pattern = HamburgerMenu.EXIT.similar(0.95)
            minimize_window()

        default_window_location = Location(x=(SCREEN_WIDTH / 20), y=(SCREEN_HEIGHT / 20))

        iris_tab_on_start_position = find(iris_pattern)
        drag_drop(iris_tab_on_start_position, default_window_location)
        maximize_window()
        change_preference('devtools.chrome.enabled', True)

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        tab_one_loaded = exists(firefox_test_site_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, tab_one_loaded, 'First tab loaded')

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        tab_two_loaded = exists(mozilla_test_site_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, tab_two_loaded, 'Second tab loaded')

        if not Settings.is_mac():
            minimize_window()

        open_browser_console()
        paste('window.resizeTo(1000, 400)')
        type(Key.ENTER)

        if not Settings.is_mac():
            click_window_control('close')
        else:
            type('w', KeyModifier.CMD)

        tabs_located_after_size_changed = exists(mozilla_test_site_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, tabs_located_after_size_changed, 'Tabs located after size of main window had changed.')

        default_tabs_position = find(mozilla_test_site_tab_pattern)
        default_tabs_region = Region(0, default_tabs_position.y, width=SCREEN_WIDTH, height=SCREEN_HEIGHT / 10)

        tab_two_drop_location = Location(x=0, y=(default_tabs_position.y + 2 * SCREEN_HEIGHT / 5))

        drag_drop(default_tabs_position, tab_two_drop_location)
        open_browser_console()
        paste('window.resizeTo(600, 400)')
        type(Key.ENTER)
        click_window_control('close')

        tab_two_relocated = not exists(mozilla_test_site_tab_pattern, in_region=default_tabs_region)
        active_tab_switched = exists(firefox_test_site_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, tab_two_relocated and active_tab_switched, 'Second tab relocated')

        tab_one_location = find(firefox_test_site_tab_pattern)
        tab_one_drop_location = Location(x=(tab_one_location.x + SCREEN_WIDTH / 5),
                                         y=(tab_one_location.y + SCREEN_HEIGHT / 10))

        drag_drop(tab_one_location, tab_one_drop_location)

        open_browser_console()
        paste('window.resizeTo(500, 500)')
        type(Key.ENTER)
        click_window_control('close')

        tab_one_moved = exists(firefox_test_site_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, tab_one_moved,
                    'Changes to height and width performed. First tab\'s first relocation completed.')
        tab_one_intermediate_location = find(firefox_test_site_tab_pattern)

        tab_one_drop_location.offset(SCREEN_WIDTH / 10, SCREEN_HEIGHT / 20)
        drag_drop(tab_one_intermediate_location, tab_one_drop_location)

        tab_one_relocated = not exists(firefox_test_site_tab_pattern, in_region=default_tabs_region)
        assert_true(self, tab_one_relocated,
                    'First opened tab relocated. Two tabs were dragged outside the main browser window.')

        tab_one_window_region = Region(0, tab_one_drop_location.y, width=SCREEN_WIDTH, height=SCREEN_HEIGHT / 5)

        tab_one_moved_twice = exists(firefox_test_site_tab_pattern)
        assert_true(self, tab_one_moved_twice, 'Tabs positioned in different places.')

        if not Settings.is_mac():
            click(hamburger_menu_button_pattern, DEFAULT_UI_DELAY, in_region=tab_one_window_region)
            hamburger_menu_quit_displayed = exists(hamburger_menu_quit_item_pattern, DEFAULT_FIREFOX_TIMEOUT)
            assert_true(self, hamburger_menu_quit_displayed, 'Close Firefox from the "Hamburger" menu.')
            click(hamburger_menu_quit_item_pattern, DEFAULT_UI_DELAY)
        else:
            type('q', KeyModifier.CMD)

        status = self.firefox_runner.process_handler.wait(Settings.FIREFOX_TIMEOUT)
        if status is None:
            self.firefox_runner.stop()
            self.firefox_runner = None

        self.firefox_runner = launch_firefox(self.browser.path, self.profile_path, self.base_local_web_url)
        self.firefox_runner.start()

        firefox_restarted = exists(hamburger_menu_button_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, firefox_restarted, 'Firefox restarted successfully')
        click(hamburger_menu_button_pattern, DEFAULT_UI_DELAY)

        restore_previous_session_located = exists(restore_previous_session_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, restore_previous_session_located, 'The "Hamburger" menu is successfully displayed. '
                                                            '"Restore previous session" menu item located')
        click(restore_previous_session_pattern)

        mozilla_site_restored = exists(mozilla_test_site_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        firefox_test_site_restored = exists(firefox_test_site_tab_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, mozilla_site_restored and firefox_test_site_restored, 'Session restored successfully')

        firefox_test_site_restored_position = find(firefox_test_site_tab_pattern)
        mozilla_site_restored_position = find(mozilla_test_site_tab_pattern)
        iris_tab_restored_position = find(iris_pattern)

        firefox_test_site_most_right = firefox_test_site_restored_position.x > max(iris_tab_restored_position.x,
                                                                                   mozilla_site_restored_position.x)

        firefox_test_site_middle_height = \
            mozilla_site_restored_position.y > firefox_test_site_restored_position.y > iris_tab_restored_position.y

        assert_true(self, firefox_test_site_most_right and firefox_test_site_middle_height,
                    'First restored window is located in the right position')

        mozilla_site_the_lowest = mozilla_site_restored_position.y > max(iris_tab_restored_position.y,
                                                                         firefox_test_site_restored_position.y)

        assert_true(self, mozilla_site_the_lowest, 'Second restored window is located in the right position')

        click(firefox_test_site_restored_position, DEFAULT_UI_DELAY)
        open_browser_console()
        paste('window.innerHeight')
        type(Key.ENTER)
        test_site_window_height_matched = exists(console_output_height_500, DEFAULT_FIREFOX_TIMEOUT)

        paste('window.innerWidth')
        type(Key.ENTER)

        test_site_window_width_matched = exists(console_output_width_500, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, test_site_window_width_matched and test_site_window_height_matched,
                    'First window size matched')
        click_window_control('close')

        click(mozilla_site_restored_position, DEFAULT_UI_DELAY)
        open_browser_console()
        paste('window.innerHeight')
        type(Key.ENTER)
        mozilla_site_window_height_matched = exists(console_output_height_400, DEFAULT_FIREFOX_TIMEOUT)

        paste('window.innerWidth')
        type(Key.ENTER)
        mozilla_site_window_width_matched = exists(console_output_width_600, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, mozilla_site_window_height_matched and mozilla_site_window_width_matched,
                    'Second window size matched')

        click_window_control('close')

        click(iris_tab_restored_position)
        open_browser_console()

        paste('window.innerHeight')
        type(Key.ENTER)
        iris_window_height_matched = exists(console_output_height_400, DEFAULT_FIREFOX_TIMEOUT)

        paste('window.innerWidth')
        type(Key.ENTER)
        iris_window_width_matched = exists(console_output_width_1000, DEFAULT_FIREFOX_TIMEOUT)

        assert_true(self, iris_window_height_matched and iris_window_width_matched, 'Iris window size matched. '
                    'The previous session is successfully restored and the width, '
                    'height and position of each tab is displayed as in the previous session.')

        click_window_control('close')

        close_window()
        close_window()
