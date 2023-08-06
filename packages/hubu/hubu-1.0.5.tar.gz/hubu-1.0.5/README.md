# Humble Bundle Archiver

## Install / update

```
$ pip install -U hubu
# or in user space
$ pip install -U --user hubu
```

## Use

Only two ENVs are required:

```
HUMBLE_BUNDLE_SESSION='"humble bundle _simpleauth_sess"'
BUCKET_NAME=humble-bundle
$ hubu
```

For the rest, you can use `AWS_PROFILE` or specify them as environment variables (see below).

## Wasabi

```
HUMBLE_BUNDLE_SESSION='"humble bundle _simpleauth_sess"'
BUCKET_NAME=humble-bundle
ENDPOINT_URL="https://s3.eu-central-1.wasabisys.com"
AWS_ACCESS_KEY_ID="xxxxxxxxxxxxxxx"
AWS_SECRET_ACCESS_KEY="xxxxxxxxxxxxxxxxx"
```

## AWS

```
HUMBLE_BUNDLE_SESSION='"humble bundle _simpleauth_sess"'
BUCKET_NAME=humble-bundle
AWS_ACCESS_KEY_ID="xxxxxxxxxxxxxxx"
AWS_SECRET_ACCESS_KEY="xxxxxxxxxxxxxxxxx"
```
