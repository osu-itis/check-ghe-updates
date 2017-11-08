# check-ghe-updates

A python script that checks for new GitHub Enterprise releases and sends email accordingly

## Requirements

* python 2.7.x
* [Requests](http://docs.python-requests.org/) > 2.9.x

## Configuration

Configuration is performed via environment variables:

* `CHECK_GHE_UPDATES_DEBUG` - if set to 1, print debut output to stdout; if set to 0, no debug output (defaults to: 0)
* `CHECK_GHE_UPDATES_SOURCE` - update site to check for updates (defaults to: https://github-enterprise.s3.amazonaws.com/release/latest.json)
* `CHECK_GHE_UPDATES_SMTP` - SMTP server for sending email (defaults to: localhost)
* `CHECK_GHE_UPDATES_FROM` - email address to send from (defaults to: check-ghe-updates@unknown)
* `CHECK_GHE_UPDATES_RECIPIENT` - email address(es) to send to; multiple email addresses must be comma-separated
* `CHECK_GHE_UPDATES_CACHE` - path to cache file (defaults to: `/tmp/check_ghe_version.cache`)

## Usage

```
$ python check-ghe-updates.py
```
