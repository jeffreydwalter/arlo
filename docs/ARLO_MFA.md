# Arlo MFA via Gmail

Arlo now requires MFA for login. This feature adds support for retrieving the relevant OTP code from any Gmail account.

This process does not require external services or subscriptions and accesses the Gmail account via the official Google API.

## Instructions

1. Login with a new or existing Gmail account.
   * The script will have *read-only* permissions on this gmail account.
   * Care is taken to only search and load emails relevant to Arlo MFA but the script does have access to the entire mailbox.
   * While this implementation is completely private, it's recommended to use a separate gmail account for Arlo login purposes.
1. Create or use an existing Google Cloud project.
   * Go to the [Google Cloud console](https://console.cloud.google.com)
   * Create or use an existing project.
1. Enable the Gmail API
   * Go to APIs & Services -> Library
   * Search for Gmail
   * Enable the Gmail API
1. Setup the OAuth consent screen
   * Go to APIs & Services -> OAuth consent screen
   * Setup OAuth consent screen
     * The app name and emails can be anything.
   * Scopes
     * Add Scopes
     * Filter for "Gmail API"
     * Add the scope ".../auth/gmail.readonly"
   * Test Users
     * Add the gmail address of your Arlo login
1. Create OAuth 2.0 Client ID credentials
   * Click on Create Credentials -> OAuth client id
   * Under Application type, select "Web application"
   * Name can be anything
   * Under "Authorized redirect URIs", add "http://localhost:7788"
   * Click Create
   * Close the window with the credentials, we will save them in the next step.
1. Save the OAuth client credential package
   * For the newly client id row, click the download button (down arrow) on the right side
   * Save this credential in your project as "google_client_credentials.json"
1. Run the `gmail_oauth.py` script
   * This will open a browser and ask you to login and authenticate with Google
   * It may warn you that this is a test application, please force continue
   * Approve of the gmail read only scope on the next screen
   * This script will save a file called `gmail.credentials`. This file will allow us to persistently access the gmail account programmatically.
1. Update your project to pass the name of this file into the Arlo class.
   * For example, instead of `arlo = Arlo(USERNAME, PASSWORD)`
   * Call `arlo = Arlo(USERNAME, PASSWORD, '/path/to/gmail.credentials)`

## How it works

We are creating an OAuth application and registering it with Google. The `gmail_oauth.py` script forwards you to authenticate with this application and grant your application read-only access to your mailbox.

When we initialize the Arlo class, the `LoginMFA` function:
  * Authenticates against the Arlo API
  * Fetches valid MFA factors
  * Selects the "EMAIL" factor
  * Begins authentication with this factor
  * Waits 5 seconds
  * Checks your gmail account by searching for new emails (postmarked AFTER the beginning of authentication) with an arlo authentication code.
  * Extract this code and complete the authentication process.