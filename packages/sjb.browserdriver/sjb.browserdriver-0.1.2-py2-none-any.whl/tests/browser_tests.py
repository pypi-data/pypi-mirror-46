# PEP8: Group imports
# 1) Standard library imports.
import logging
import logging.handlers
import os
import sys
# 2) Related third party imports.
import unittest2
# 3) Local application/library specific imports.
from browser_driver import browser


class BrowserDriverTests(unittest2.TestCase):
    @classmethod
    def log_directory(cls, create_not_found=True):
        """Returns the directory where the log file should be stored

            create_not_found being True will create the directory if it doesn't exist
        """
        project_name = "browser_driver"

        # Are we running from within PyCharm or starting from command line at the root directory?
        if os.getcwd().find("tests"):
            base_dir = os.getcwd().replace("\\tests", "")
        else:
            base_dir = os.getcwd()

        source_dir = "{0}\\{1}".format(base_dir, project_name)
        test_dir = "{0}\\{1}".format(base_dir, "tests")
        test_log_dir = "{0}\\{1}".format(test_dir, "logs")

        if not os.path.exists(test_log_dir) and create_not_found:
            os.makedirs(test_log_dir)

        return test_log_dir

    def setUp(self):
        self.browser = browser.WebBrowser(logger=self.log)

    @classmethod
    def setUpClass(cls):
        cls.log = logging.getLogger(__name__)

        stdout_log = logging.StreamHandler(sys.stdout)
        stdout_log.setFormatter(logging.Formatter(fmt=""))
        stdout_log.setLevel(logging.INFO)
        # stdout_log.setLevel(logging.DEBUG)

        file_log_path = cls.log_directory(True)
        file_name = "{0}\{1}.log".format(file_log_path, cls.__getattribute__(cls, "__name__"))
        file_log = logging.handlers.TimedRotatingFileHandler(filename=file_name, when="D", interval=1, backupCount=30)
        file_log.setFormatter(logging.Formatter(fmt="%(asctime)s | %(levelname)s\t| %(message)s"))
        file_log.setLevel(logging.DEBUG)

        cls.log.addHandler(file_log)
        cls.log.addHandler(stdout_log)
        # Important to set overall logger to catch all statements which it can then route to handlers
        cls.log.setLevel(logging.DEBUG)

        # For some reason, at least running in PyCharm, a newline is not created.  Explicitly adding it.
        cls.log.debug("Logger {0} obtained for usage by {1} \n".format(cls.log.name, cls.__name__))

    def tearDown(self):
        """A set of actions to be used by all unittest2.TestCase.tearDown() methods.  This will
        enable functionality such as leaving the browser open if the test failed (and we are running
        with the browser visible).  This is a clean-up method to standardize across all tests.

            Args:
                test_case is an instance of unittest2.TestCase

            Example:
                class myTests(unitests2.TestCase):
                    def tearDown(self):
                        helper_selenium_functions.py.tear_down(self)
        """
        if self._outcome.errors[1][1] is None:
            self.log.info("{0}() completed successfully and no errors were observed.".format(self._testMethodName))
            self.browser.quit()
        else:
            self.log.warn("WARNING: Errors observed in execution of {0}().".format(self._testMethodName))
            if self.browser.name is not "phantomjs":
                self.log.warn("Did not call driver.quit() leaving {0} browser open for debugging.".format(self.browser.name))
            else:
                self.browser.quit()

    def test_browser_Firefox(self):
        """Test that a Firefox browser can be used.  Test the name is not case sensitive."""
        # Close out the browser already created to prevent ResourceWarning: unclosed <socket.socket fd=
        self.browser.quit()
        # Now let's make sure we have a FireFox browser to start with
        self.browser = browser.WebBrowser("FireFOX")
        self.assertIsNotNone(self.browser)
        self.assertEqual(self.browser.name.lower(), "firefox")

    def test_click_element(self):
        """This test ensures that the mouse clicks on a given element"""
        # url = "file://{0}/test_click.html".format(os.getcwd()).replace('\\', '/')
        url = "https://www.google.com/"
        self.browser.url = url
        self.assertEqual(self.browser.url, url)
        self.browser.send_keys_by_name('q', 'great quotes of history')
        xpath = r'//*[@id="tsf"]/div[2]/div/div[3]/center/input[1]'
        self.browser.click_element_by_xpath(xpath)
        element = self.browser.find_element_by_id("resultStats")
        self.assertIsNotNone(element, "Did not find results statistics element on page.")
        self.log.info("Search button clicked, and results returned as expected.")

    # @unittest2.skip("test definition in progress")
    def test_click_to_new_page(self):
        """This test will click a link and wait for the page to load."""
        url = "file://{0}/test_html.html".format(os.getcwd()).replace('\\', '/')
        self.browser.url = url
        self.browser.click_to_new_page_by_id("mozilla")
        element = self.browser.find_element_by_id("license")

        self.log.info(self.browser.url)

    def test_navigate(self):
        """Tests that the browser navigates to a page."""
        url = "https://www.google.com/"
        self.browser.url = url
        self.assertEqual(url, self.browser.url)

    def test_find_element_by_link_text(self):
        """Tests that the browser can find an element using a partial link text."""
        url = "file://{0}/test_html.html".format(os.getcwd())
        url.replace('\\', '/')
        self.browser.url = url
        element = self.browser.find_element_by_partial_link_text("Testing Goat")
        url = "http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html"
        self.assertEqual(element.get_attribute("href"), url)

    def test_find_element_by_partial_link_text(self):
        """Tests that the browser can find an element using a partial link text."""
        url = "file://{0}/test_html.html".format(os.getcwd())
        url.replace('\\', '/')
        self.browser.url = url
        element = self.browser.find_element_by_partial_link_text("Goat")
        url = "http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html"
        self.assertEqual(element.get_attribute("href"), url)

    def test_find_element_by_xpath(self):
        """Tests that the browser can find an element using an xPath statement."""
        url = "https://www.google.com/"
        self.browser.url = url
        element = self.browser.find_element_by_xpath('//*[@id="hplogo"]')
        self.assertIsNotNone(element)

    def test_find_element_by_id(self):
        """Tests that the browser can find an element using an id value."""
        url = "https://www.google.com/"
        self.browser.url = url
        element = self.browser.find_element_by_id("hplogo")
        self.assertIsNotNone(element)

    def test_checkboxes(self):
        """Ensures checking a box, unchecking it, and toggling the state work as expected."""
        url = "https://mdn.mozillademos.org/en-US/docs/Web/HTML/Element/input/checkbox$samples/Value?revision=1389331"
        self.browser.url = url
        element_id = "subscribeNews"
        element = self.browser.find_element_by_id(element_id)
        # Verify it's unchecked
        self.assertFalse(element.is_selected())
        # Check the box
        self.browser.check_by_id(element_id)
        self.assertTrue(element.is_selected())
        # Make sure check method is not toggling
        self.browser.check_by_id(element_id)
        self.assertTrue(element.is_selected())
        # Uncheck
        self.browser.uncheck_by_id(element_id)
        self.assertFalse(element.is_selected())
        # Make sure check method is not toggling
        self.browser.uncheck_by_id(element_id)
        self.assertFalse(element.is_selected())

    def test_click_not_in_view(self):
        """This test ensure the box can be clicked even if it is not initially in the viewable
        screen area"""
        url = "file://{0}/test_html.html".format(os.getcwd())
        url.replace('\\', '/')
        self.browser.url = url
        element = self.browser.check_by_id("horns")
        self.assertTrue(element.is_selected())

    def test_send_keys(self):
        """This test ensures the class can send keys to a text box"""
        url = "file://{0}/test_html.html".format(os.getcwd()).replace('\\', '/')
        self.browser.url = url
        test_string = "test by id"
        element = self.browser.send_keys_by_id("text_by_id", test_string)
        self.assertEqual(element.get_attribute("value"), test_string)
        test_string = "test by name"
        element = self.browser.send_keys_by_name("send_keys_by_name", test_string)
        self.assertEqual(element.get_attribute("value"), test_string)
        test_string = "test by xpath"
        element = self.browser.send_keys_by_xpath('//*[@id="text_by_xpath"]', test_string)
        self.assertEqual(element.get_attribute("value"), test_string)

