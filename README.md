# Apptitude2021 Backend

[![](https://img.shields.io/badge/Documentation-see%20docs-green?logo=appveyor)](http://apptitude2021.herokuapp.com/docs) &nbsp; &nbsp;
[![](https://img.shields.io/badge/api-root-orange)](http://apptitude2021.herokuapp.com/)

![](https://github.com/akri16/Apptitude2021-Backend/blob/main/assets/docs.PNG)

## Project Structure
    .
    ├── app 
    |   |-- firebase
    |   |   |-- service-account.json
    |   |   |-- auth.py
    |   |   |-- feats.py
    |   |   |-- user.py
    |   |   |-- submission.py
    |   |   |-- teams.py
    |   |   |-- static.py
    |   |   └- common.py
    |   |-- models
    |   |   └- schemas.py
    |   |-- constants.py 
    |   └─- app.py          
    ├── docs.py                     
    ├── main.py                  
    ├── LICENSE
    └── README.md


## Environmental Variables

* `SENTRY_DSN` -> The DSN of SENTRY for logging errors (Optional)
* `SENTRY_RATE` -> Logging Rate for SENTRY (Optional)
* `GOOGLE_CREDENTIALS` -> Service Account file of the FIREBASE project (**REQUIRED** or 'service-aacount.json' file to be added to *app/firebase*)


## Running the Project
1. Clone the Project with:

        git clone https://github.com/akri16/Apptitude2021-Backend
2. Set the [Environmental Variables](#environmental-variables)

3. Run
    1. Run with __python3__
        1. Install the Dependencies 
        
                pip install -r requirements.txt
        
        2. Run with *python3* 
      
                python3 main.py 
        
        3. Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) <br/><br/>
    2. Run with __Docker__ 
        1. Build the image 
            
                docker build -t apptitude-image .
            
        2. Run the image
            
                docker run -d --name mycontainer -p 80:80 apptitude-image
            
        3. Go to [http://127.0.0.1/docs](http://127.0.0.1/docs)


## Database Schema

```json
{
  "adminControl" : {
    "allowSubmission" : false,
    "discordLink" : "-",
    "eventStartTime" : 1637940600
  },
  "admins" : {
    "+918921816808" : {
      "level" : 2,
      "login" : "1595330145",
      "name" : "Amit Krishna",
      "phone" : "+918921816808"
    }
  },
  "features" : {
    "easy" : [ "abc"],
    "hard" : [ "def"],
    "medium" : [ "ghi"]
  },
  "participants" : {
    "0fy2NZRWv3cRcNVoSb1kLHVahxr2" : {
      "emailId" : "xyz@gmail.com",
      "name" : "John Martin",
      "phoneNo" : "+918455986398",
      "team" : 79441271637
    }
  },
  "sponsors" : [{
    "link" : "https://firebasestorage.googleapis.com/v0/b/app-hackathon-d1655.appspot.com/o/cb_new.png",
    "website" : "https://xyz.com/"
  }],
  "teams" : {
    "79425983493" : {
      "featGenCnt" : 3,
      "features" : {
        "easy" : "abc",
        "hard" : "def",
        "medium" : "ghi"
      },
      "members" : [ "Xot1V6pKm0OS7X49CDGZDc9tXKO2", "OdbtrnX5i7c9VJT56KKI8EzWeVh2" ],
      "name" : "xyz"
    }
  }
}

```

## Authentication
- Uses Bearer Authentication
- Send the ID Token from the client side in the header of every request [(Reference)](https://firebase.google.com/docs/auth/admin/verify-id-tokens#android)

## License

    MIT License

    Copyright (c) 2021 Amit Krishna A

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
