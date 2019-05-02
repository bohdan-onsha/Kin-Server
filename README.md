## Installation
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
7. `Change your firebase rules as in the example below`
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
8. `python application.py &`

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
└── requirements.txt.md     # Project dependencies
```

## API

### 1. Sign up user:  `/api/v1/user/register`

#### Input: 
```
{
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
    "public_address": "GBW4NQFQH6IOOPKY5ZXKS2U4D5FDW6PIXCFJQIXM2GXP2OR4COBQGHIR",
    "seed": "SC6WPRW4ORYAAJVJ2KQC6GSTPSVL7IC2CQFG7ITMASGPH4NSBSSQTPSO",
    "uid": "Oy46pOMn6lfJrMJnBMForPaDDyT2"
}
```

### 2. Sign in user:  `/api/v1/user/auth`

#### Input: 
```
{
 "email":"YourMail@gmail.com",
 "password": "yourpassword228"
 }
 ```
 #### Output:
 ```
 [
    "eyJhbGciOiJSUzI1NiIsImtpZCI6IjM4MDEwNjVlNGI1NjNhZWVlZWIzNTkwOTEwZDlmOTc3YTgxMjMwOWEiLCJ0eXAiOiJKV1QifQ.e
    yJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20va2luc2VydmVyLTUyZWU4IiwiYXVkIjoia2luc2VydmVyLTUyZWU4Ii
    wiYXV0aF90aW1lIjoxNTU2Nzk2NTEzLCJ1c2VyX2lkIjoiT3k0NnBPTW42bGZKck1KbkJNRm9yUGFERHlUMiIsInN1YiI6Ik95NDZwT01u
    NmxmSnJNSm5CTUZvclBhRER5VDIiLCJpYXQiOjE1NTY3OTY1MTMsImV4cCI6MTU1NjgwMDExMywiZW1haWwiOiJvbnNoYS5ib2dkYW4yMD
    AwQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJvbnNoYS5i
    b2dkYW4yMDAwQGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.QAEp_gS2eyqkMF0ssaJAeH3aLXs60lDiv
    60GgOUzn1T6nJJJiuf4-ieWuDF9SCrDhpyx5Ca-5xI4W5KXtkUvJCFY8BWx5vQn5oxa4PmQ1j6auFkWFqdad9FHfSIsLZ2_R65B550-jPu
    YYbkOVFsL_f3GRwNk5hYzau65a_kJEa1OWp_TkhQ1NbCzHHv92X6DqYpZXQMa_6LbKokbwLGie5Ll79NQrAcBegfadvxqE7pdo-8eWKxGb
    DyttOqJauahg0HDiNI7RQ6MWjMqHzsTAyLPq5jKrxna_IMiHKp4sW_ZykQaPr8TArvOwezSVAqyDLJBx2UrCZ9RuKvRJraFVg"
]
```

### 3. Send kins to user: `/api/v1/user/get-kins`

#### Input: 
```
{
   "uid": "Oy46pOMn6lfJrMJnBMForPaDDyT2",
   "token":"eyJhbGciOiJSUzI1NiIsImtpZCII7RQx2UrCZ9RuKvRJraFVg...",
   "amount":100,
   "description" : "example-descr"
}
 ```
 #### Output:
 ```
{
   "amount": 100,
   "id": "85206471492e4b02cf0c3bbccc93a439d42a155256029a083bea6faf1b273567",
   "memo": "1-NM8e-example-descr",
   "recipient_address": "GBW4NQFQH6IOOPKY5ZXKS2U4D5FDW6PIXCFJQIXM2GXP2OR4COBQGHIR",
   "sender_address": "GCW25THTQ6YP32QV6JVMRKX2SYWLBM345WKN2PBTCTTDZET2HMSPMIAY",
   "uid": "Oy46pOMn6lfJrMJnBMForPaDDyT2"
}
```


### 4. Get current server wallet public address: `/api/v1/server-wallet`

#### Input: 
```
{
 "uid": "Oy46pOMn6lfJrMJnBMForPaDDyT2",
 "token":"eyJhbGciOiJSUzI12VydmVyLTUyZWU4IiwiYk0NnBPTW4siaWRlbng..."
}
 ```
#### Output:
 ```
[
    "GCW25THTQ6YP32QV6JVMRKX2SYWLBM345WKN2PBTCTTDZET2HMSPMIAY"
]
```

### 5. Get user transaction history: `/api/v1/user/history`

#### Input: 
```
{
 "uid": "Oy46pOMn6lfJrMJnBMForPaDDyT2",
 "token":"eyJhbGciOiJSUzI12VydmVyLTUyZWU4IiwiYk0NnBPTW4siaWRlbng..."
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

## Admin panel

#### 1. Create admin user
In project folder
`python create_admin.py YourMail@gmail.com  YourPassword228`

#### 2. Open `/admin`
