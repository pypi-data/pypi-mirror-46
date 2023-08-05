"""
strings for the mimir cli
"""
import os


MIMIR_DIR = os.path.expanduser("~/.mimir/")
MIMIR_CREDS_PATH = "{dir}.credentials".format(dir=MIMIR_DIR)
ZIP_LOC = "{}sub.zip".format(MIMIR_DIR)

AUTH_SUCCESS = "Successfully logged into Mimir Classroom!"
API_AUTH_SUCCESS = "Successfully saved Mimir Classroom API token!"
LOGOUT_SUCCESS = "Successfully logged out of Mimir Classroom!"

ERR_NOT_AUTH = "Please log into Mimir Classroom first!"
ERR_INVALID_CRED = "Invalid email or password!"
ERR_INVALID_FILE = "Failed to open file `{}`."

PROJECT_PROMPT = "Type the number of the project you want to submit to"
PROJECT_ERR_0_TO_N = "Input a number 0 through {} please!"

EMAIL_PROMPT = "Email"
EMAIL_HELP = "Mimir Classroom Email"
PW_HELP = "Mimir Classroom Password"
API_TOKEN_HELP = "Mimir Classroom API Token"


SUB_WARNING = "\nWARNING"
SUB_CONFIRM_FORCE = "Would you like to force this submission anyway?"
SUB_SUCCESS_URL = "\nSubmission successful! Click here for your results: "
