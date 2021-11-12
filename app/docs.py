from app.constants import constants


title = "Apptitude 2021"
version="0.0.1"

__nl = "<br>"


description = f"""

## Authenticate into the API

* Uses **Bearer** Authentication
* Send the ID Token from the client side in the header of every request
* <a href="https://firebase.google.com/docs/auth/admin/verify-id-tokens#android">Reference</a>

## Feats

You can **Generate Random Features and assign it to your team**.

## Team

You will be able to:

* **Create Team** 
* **Join Team** 

## Errors: 
{__nl.join(constants.values())}

"""
