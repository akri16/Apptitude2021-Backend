import os
from app.firebase import common
import sentry_sdk


dsn = os.getenv('SENTRY_DSN')
rate = os.getenv('SENTRY_RATE')

if dsn and rate:
    sentry_sdk.init(dsn, traces_sample_rate=rate)

cred = os.getenv('GOOGLE_CREDENTIALS')

if cred is not None:
    with open('app/firebase/service-account.json', 'w+', encoding='utf-8') as f:
        f.write(cred)

common.init()

