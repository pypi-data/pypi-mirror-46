# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s collective.embeddedpage -t test_embeddedpage.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src collective.embeddedpage.testing.COLLECTIVE_EMBEDDEDPAGE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_embeddedpage.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open chrome browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a EmbeddedPage
  Given a logged-in site administrator
    and an add embeddedpage form
   When I type 'My EmbeddedPage' into the title field
    and I type 'https://plone.org' into the URL field
    and I submit the form
   Then a embeddedpage with the title 'My EmbeddedPage' has been created
   Debug

Scenario: As a site administrator I can view a EmbeddedPage
  Given a logged-in site administrator
    and a embeddedpage 'My EmbeddedPage'
   When I go to the embeddedpage view
   Then I can see the embeddedpage title 'My EmbeddedPage'


*** Keywords *****************************************************************

# --- Setup ------------------------------------------------------------------

Open chrome browser
  ${options}=  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys, selenium.webdriver
  Call Method  ${options}  add_argument  disable-extensions
  Call Method  ${options}  add_argument  disable-web-security
  Call Method  ${options}  add_argument  window-size\=1280,1024
  # Call Method  ${options}  add_argument  remote-debugging-port\=9223
  Create WebDriver  Chrome  chrome_options=${options}


# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add embeddedpage form
  Go To  ${PLONE_URL}/++add++EmbeddedPage

a embeddedpage 'My EmbeddedPage'
  Create content  type=EmbeddedPage  id=my-embeddedpage  title=My EmbeddedPage


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I type '${url}' into the URL field
  Input Text  name=form.widgets.url  ${url}

I submit the form
  Click Button  Save

I go to the embeddedpage view
  Go To  ${PLONE_URL}/my-embeddedpage
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a embeddedpage with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the embeddedpage title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
