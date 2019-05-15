## Local installation
0. `Make sure you have python 3.7 and pip installed`
1. `git clone https://github.com/OnshaBogdan/Kin-Server.git`
2. `cd Kin-Server/`
3. `virtualenv -p python3 .venv`
4. `source .venv/Scripts/activate`
5. `pip3 install --upgrade -r requirements.txt`
6. `Replace config.py with your firebase data`
```
  config = {
      "apiKey": "",
      "authDomain""": "",
      "databaseURL": "",
      "projectId": "",
      "storageBucket": "",
      "messagingSenderId": ""
  }
```
7. Change your firebase rules as in the example below
```
{
  "rules": {
        "users" : {
          ".indexOn": ["email", "uid"]
        },
        "transactions" : {
          ".indexOn": ["uid"]
        },
        ".read": true,
        ".write": true
    }
}
```
8. Change `app.secret_key` in `application.py`

## Deployment (Ubuntu 16.04)
#### Install python3.7, pip and virtualenv
1. `sudo apt update`
2. `sudo apt install software-properties-common`
3. `sudo add-apt-repository ppa:deadsnakes/ppa`
4. `sudo apt update`
5. `sudo apt install python3.7`
6. `sudo apt install python3-pip`
7. `sudo apt install python3.7-dev`
8. `python3.7 -m pip install virtualenv`

#### Clone project and install dependencies
1. `mkdir /var/Kin`
2. `cd /var/Kin`
3. `git clone https://github.com/OnshaBogdan/Kin-Server.git`
4. `cd Kin-Server/`
5. `virtualenv -p python3.7 .venv`
6. `source .venv/bin/activate`
7. `python3.7 -m pip install -r requirements.txt`
8. `gunicorn -k uvicorn.workers.UvicornWorker --bind="0.0.0.0:5000" wsgi:app --daemon --access-logfile access-log.txt --error-logfile error-log.txt`
## Project Structure
```bash
.
├── .venv                   # virtual environment
├── static                  # Folder with staticfiles (.css, .js)
├── templates               # Folder with .html templates
├── application.py          # Main Script, runs the app
├── configuration.py        # Configuration of firebase db
├── errors.py               # Custom Exceptions
├── firebase_service.py     # Firebase driver
├── kin-service.py          # Kin-sdk driver
├── limits.py               # Script that refreshes user limits periodically
├── create-admin.py         # Creates user with admin panel access
├── wsgi.py                 # Gunicorn/Uvicorn entry point
└── requirements.txt.md     # Project dependencies
```

## API

### 1. Sign up user:  `/api/v1/user/register`

#### Input: 
```
 body{
 "email":"YourMail@gmail.com",
 "password": "yourpassword228"
 }
 ```
 #### Output:
 ```
{
    "balance": 0,
    "email": "YourMail@gmail.com",
    "is_admin": false,
    "limits": {
        "day": "1000",
        "month": "15000",
        "week": "5000"
    },
    "public_address": "GDYXLK2MLGNTWMDTBTCJ2C7X6GQVYGV4234EZDOLNGPATUS64EUJ5M3W",
    "seed": "SB2COATQYWFZ6TE5NRZBWDYC3ZKVA3KXGSLKD3DLYNMKJRX3C242LHII",
    "token": "a6e2347889404034a4f442d27269ca29",
    "uid": "U7y8MR1c6eTa4qb62JICaxn4jBr2"
}
```

### 2. Sign in user:  `/api/v1/user/auth`

#### Input: 
```
 body{
 "email":"YourMail@gmail.com",
 "password": "yourpassword228"
 }
 ```
 #### Output:
 ```
{
    "is_admin": false,
    "token": "9188dace30f34f31b0bf172d570e55fb"
}
```

### 3. Send kins to user: `/api/v1/user/replenish`

#### Input: 
```
headers{
    "uid" : "ml3UADqweOXYznUaQPGLPmDklOz1"
}
body{
   "token":"eyJhbGciOiJSUzI1NiIsImtpZCII7RQx2UrCZ9RuKvRJraFVg...",
   "amount":100,
   "description" : "example-descr"
}
 ```
 #### Output:
 ```
{
    "amount": 10,
    "balance": 79.998,
    "id": "b4a520698fd5b114fe3c2c1c4fa6f174a587064629eacad4668897d28a53ec04",
    "memo": "1-NM8e-api",
    "recipient_address": "GC3DZ7PIJL4NADTAPWIJXAOANQ37KJB3BQWQADXAEDIWM3TOIRTSDXAF",
    "sender_address": "GCW25THTQ6YP32QV6JVMRKX2SYWLBM345WKN2PBTCTTDZET2HMSPMIAY",
    "uid": "ml3UADqweOXYznUaQPGLPmDklOz1"
}
```


### 4. Send kins to server: `/api/v1/user/pay`

#### Input: 
```
headers{
    "uid" : "ml3UADqweOXYznUaQPGLPmDklOz1"
}
body{
   "token":"eyJhbGciOiJSUzI1NiIsImtpZCII7RQx2UrCZ9RuKvRJraFVg...",
   "amount":100,
   "description" : "example-descr"
}
 ```
 #### Output:
 ```
{
    "amount": 10,
    "balance": 69.997,
    "id": "f7a761b97be8c4fa10ddd9329c214bd97c13663bb36504cf9b501d696cd029cb",
    "memo": "1-NM8e-api",
    "recipient_address": "GCW25THTQ6YP32QV6JVMRKX2SYWLBM345WKN2PBTCTTDZET2HMSPMIAY",
    "sender_address": "GC3DZ7PIJL4NADTAPWIJXAOANQ37KJB3BQWQADXAEDIWM3TOIRTSDXAF",
    "uid": "ml3UADqweOXYznUaQPGLPmDklOz1"
}
```
### 5. Get user balance: `/api/v1/user/balance`

#### Input: 
```
headers{
    "uid" : "ml3UADqweOXYznUaQPGLPmDklOz1"
}
body{
    "token":"703392294f934aa0b9ce823a70a2e800"
}
 ```
#### Output:
 ```
[
    69.997
]
```

### 6. Get current server wallet public address: `/api/v1/server-wallet`

#### Input: 
```
headers{
    "uid" : "ml3UADqweOXYznUaQPGLPmDklOz1"
}
body{
    "token":"703392294f934aa0b9ce823a70a2e800"
}
 ```
#### Output:
 ```
[
    "GCW25THTQ6YP32QV6JVMRKX2SYWLBM345WKN2PBTCTTDZET2HMSPMIAY"
]
```

### 7. Get user transaction history: `/api/v1/user/history`

#### Input: 
```
headers{
    "uid" : "ml3UADqweOXYznUaQPGLPmDklOz1"
}
{
 "token":"703392294f934aa0b9ce823a70a2e800"
}
 ```
#### Output:
 ```
[
    {
        "amount": 100,
        "id": "85206471492e4b02cf0c3bbccc93a439d42a155256029a083bea6faf1b273567",
        "memo": "1-NM8e-example-descr",
        "recipient_address": "GBW4NQFQH6IOOPKY5ZXKS2U4D5FDW6PIXCFJQIXM2GXP2OR4COBQGHIR",
        "sender_address": "GCW25THTQ6YP32QV6JVMRKX2SYWLBM345WKN2PBTCTTDZET2HMSPMIAY",
        "uid": "Oy46pOMn6lfJrMJnBMForPaDDyT2"
    }
]
```

### 8. Logout user: `/api/v1/user/logout`

#### Input: 
```
headers{
    "uid" : "ml3UADqweOXYznUaQPGLPmDklOz1"
}
 ```
#### Output:
 ```
{
true
}
```

## Admin panel

#### 1. Create admin user
In project folder
`python create_admin.py YourMail@gmail.com  YourPassword228`

#### 2. Open `/admin`
