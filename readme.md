# Workplace_frontline_users

This python script pulls all Active users from the Workplace API and then checks them against a ruleset to see if those users should be in the Frontline people set. It then updates the people set with the correct people.

## Install

- The script requires a host with Python 3.8 or above installed
- Create an integration in Workplace. Give the integration the "Manage work profiles" permission
- Create an access token for the integration and make a note of it (do not lose this as it cannot be recovered)
- Create an environment variable (the script accepts .env files) called "accessToken". Set its value to the access token you created above
- Create a second environment variable called "prodMode". This is a failsafe. By default, the script will run in a test mode; printing out to the console but not apply any changes to Workplace. To make the script function, set this to True
- Create your ruleset in the rules.py file

## Disclaimer

This script is provided "as is" with no warranty or guarantee.

[#WeAreCoolr](https://www.wearecoolr.com/workplace)
