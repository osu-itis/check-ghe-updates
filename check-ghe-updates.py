import requests
import json
import re
import os
import sys
import smtplib
from email.mime.text import MIMEText

# get variables from environment
CHECK_GHE_UPDATES_SOURCE = os.getenv('CHECK_GHE_UPDATES_SOURCE', 'https://github-enterprise.s3.amazonaws.com/release/latest.json')
CHECK_GHE_UPDATES_SMTP = os.getenv('CHECK_GHE_UPDATES_SMTP', 'localhost')
CHECK_GHE_UPDATES_FROM = os.getenv('CHECK_GHE_UPDATES_FROM', 'check-ghe-updates@unknown')
CHECK_GHE_UPDATES_RECIPIENT = os.getenv('CHECK_GHE_UPDATES_RECIPIENT', 'root@localhost').split(',')
CHECK_GHE_UPDATES_CACHE = os.getenv('CHECK_GHE_UPDATES_CACHE', '/tmp/check_ghe_version.cache')
if os.getenv('CHECK_GHE_UPDATES_DEBUG', '0') == '1':
    DEBUG = True
else:
    DEBUG = False

def main():
    # load previous check results from cache
    if os.path.isfile(CHECK_GHE_UPDATES_CACHE):
        if DEBUG: print "found cache file"
        with open(CHECK_GHE_UPDATES_CACHE, 'r') as f:
            try:
                previous_check = json.load(f)
                cache_file_loaded = True
            except ValueError:
                if DEBUG: print "cache file does not contain valid JSON, forcing update check"
                cache_file_loaded = False
    else:
        if DEBUG: print "no cache file found, forcing update check"
        cache_file_loaded = False

    if cache_file_loaded == False:
        previous_check = {"latest": ""}

    # get current version details from update source
    r = requests.get(CHECK_GHE_UPDATES_SOURCE)
    current_json = json.loads(r.text)

    # check for version change
    if previous_check['latest'] != current_json['latest']:
        # indicate change in cache file
        current_json['has_update'] = True

        # save cache
        with open(CHECK_GHE_UPDATES_CACHE, 'w') as f:
            json.dump(current_json, f)

        # send email
        output = "version change detected: {} -> {}".format(previous_check['latest'], current_json['latest'])
        subject = "new GitHub Enterprise release is available: {}".format(current_json['latest'])
        if DEBUG: print output
        send_email(subject, output)
        if DEBUG: print "email sent!"
    else:
        current_json['has_update'] = False

        # save cache
        with open(CHECK_GHE_UPDATES_CACHE, 'w') as f:
            json.dump(current_json, f)

        if DEBUG: print "latest version has not changed (is: {})".format(current_json['latest'])


def send_email(msg_subject, msg_text):
    msg = MIMEText(msg_text)
    msg['Subject'] = msg_subject
    msg['From'] = CHECK_GHE_UPDATES_FROM
    msg['To'] = ','.join(CHECK_GHE_UPDATES_RECIPIENT)

    s = smtplib.SMTP(CHECK_GHE_UPDATES_SMTP)
    s.sendmail(CHECK_GHE_UPDATES_FROM, CHECK_GHE_UPDATES_RECIPIENT, msg.as_string())
    s.quit()


if __name__ == "__main__":
    main()
