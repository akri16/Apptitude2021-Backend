# Apptitude2021 Backend

[![](https://img.shields.io/badge/Documentation-see%20docs-green?style=flat-square&logo=appveyor)](http://apptitude2021.herokuapp.com/docs)

![](https://github.com/akri16/Apptitude2021-Backend/blob/master/assets/docs.PNG)

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
```sh
git clone https://github.com/akri16/Apptitude2021-Backend
```

2. Set the [Environmental Variables](#Environmental--Variables)

3. Run
    1. Run with __python3__
        1. Install the Dependencies 
        ```sh
        pip install -r requirements.txt
        ```

        2. Run with *python3* 
        ```sh
        python3 main.py 
        ```
        3. Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) <br/><br/>
    2. Run with __Docker__ 
        1. Build the image 
            ```sh
            docker build -t apptitude-image .
            ```
        2. Run the image
            ```sh
            docker run -d --name mycontainer -p 80:80 apptitude-image
            ```
        3. Go to [http://127.0.0.1/docs](http://127.0.0.1/docs)


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