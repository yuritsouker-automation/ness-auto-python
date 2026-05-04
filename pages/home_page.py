from playwright.sync_api import Page, expect


class HomePage:
    URL = "https://www.demoblaze.com/"

    # Locators
    LOGIN_NAV_BUTTON = "#login2"
    USERNAME_INPUT = "#loginusername"
    PASSWORD_INPUT = "#loginpassword"
    LOGIN_SUBMIT_BUTTON = "button[onclick='logIn()']"
    WELCOME_USER_LINK = "#nameofuser"

    def __init__(self, page: Page):
        self.page = page

    def navigate(self):
        """Navigate to the DemoBlaze home page."""
        self.page.goto(self.URL)

    def login(self, username: str, password: str):
        """
        Perform login on DemoBlaze.

        :param username: The username (email) to log in with.
        :param password: The password to log in with.
        """
        # Click the Login nav button to open the login modal
        self.page.click(self.LOGIN_NAV_BUTTON)

        # Wait for the login modal to appear
        self.page.wait_for_selector(self.USERNAME_INPUT, state="visible")

        # Fill in credentials
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)

        # Click the Log in submit button
        self.page.click(self.LOGIN_SUBMIT_BUTTON)

    def get_welcome_user_locator(self):
        """Return the locator for the welcome user element."""
        return self.page.locator(self.WELCOME_USER_LINK)

    def logout(self):
        """Click the logout button and validate the login nav button is visible again."""
        self.page.click("#logout2")
        expect(self.page.locator(self.LOGIN_NAV_BUTTON)).to_be_visible()

    def validate_logged_in(self, expected_username: str):
        """
        Validate that the user is logged in by checking the welcome message.

        :param expected_username: The username expected in the welcome text.
        """
        welcome_locator = self.get_welcome_user_locator()
        expect(welcome_locator).to_be_visible()
        expect(welcome_locator).to_have_text(f"Welcome {expected_username}")

