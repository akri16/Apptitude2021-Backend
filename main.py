import uvicorn
import os


if __name__ == '__main__':
    del os.environ['GOOGLE_CREDENTIALS']
    os.environ['DATABASE_URL'] = "https://apptitude2021-backup-default-rtdb.asia-southeast1.firebasedatabase.app/"
    uvicorn.run("app.app:app", port=8000, reload=True)
