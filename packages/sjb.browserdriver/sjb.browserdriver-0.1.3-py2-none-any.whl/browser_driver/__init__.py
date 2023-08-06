"""browser_driver is a wrapper for selenium components to manipulate testing with a browser.  We purposely wrap
the native functionality to protect from version issues.  It is not uncommon for a browser to make a change which
breaks automation.  We have found we can make easier updates to accommodate, if our calls go through a central method.
For instance one change to the browser caused links which were previously found when out of view, to stop being found.
You thus needed to scroll it into view and then find it.  This wrapper provides ability for that."""
