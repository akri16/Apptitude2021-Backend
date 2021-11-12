import os
from app.firebase import common

# cred = os.getenv('GOOGLE_CREDENTIALS', None)

# if cred is not None:
#     with open('app/firebase/service-account.json', 'w+', encoding='utf-8') as f:
#         f.write(cred)

common.init()