## Description

This repository contains an example Python API that is vulnerable to several different web API attacks.

## Requirements

* [Ansible][ansible]

## Install


Update vulnerable-api/ansible/roles/api/tasks/app.yaml
* provide a user with sudo privileges in these two sections(replace **vagrant** sudo_user)

```
- name: Stop supervisord
  shell: killall supervisord
  args:
    sudo: yes
    sudo_user: vagrant

- name: Start supervisord
  shell: supervisord -c /etc/supervisor/supervisord.conf
  args:  
    sudo: yes
    sudo_user: vagrant
```

Run ansible-playbook
```
ansible-playbook -i "localhost," -c local vulnerable-api/ansible/main.yml
```

## API Details

The example API can be accessed on the system at port 8081.

### What is vAPI

vAPI is an API written specifically to illustrate common API vulnerabilities.

vAPI is implemented using the Bottle Python Framework and consists of a user database and a token database.

### How is vAPI Used

#### vAPI Process flow

1. Request token from /tokens
  * Returns an auth token
  * Returns expiration date of auth token
  * Returns a user id
2. Request user record from /user/<user_id>
  * Requires the auth token
  * Returns the user record for the user specfied, provided the auth token is not expired and is valid for the user id specified
  * Each user can only access their own record

#### Test Users 

Included with install

| Username | Password |
|----------|----------|
|user{1-9} |pass{1-9} |
|admin1    |pass1     |

#### API Reference

##### URL

SYSTEM_IP:8081

##### POST /tokens
Request an Auth Token for a user

###### Request Headers
1. Accept: application/json
2. Content-Type: application/json

###### Request JSON Object
1. username (string) - Name of user requesting token
2. password (string) – Password of user requesting a token

###### Response JSON Object
1. token
  * expires (string) – The Auth Token expiration date/time
  * token - id (string) – Auth Token
  * user - id (string) – Unique user ID
  * name (string) – Username

###### Status Code
1. 200 OK - Request completed successfullyi

###### Request

```
POST /tokens HTTP/1.1
Accept: application/json
Content-Length: 36
Content-Type: application/json
Host: 192.168.13.37:8081

{"auth":
    {"passwordCredentials":
        {"username": "USER_NAME",
          "password":"PASSWORD"}
    }
}

 
```
###### Response
```
HTTP/1.0 200 OK
Date: Tue, 07 Jul 2015 15:34:01 GMT
Server: WSGIServer/0.1 Python/2.7.6
Content-Type: text/html; charset=UTF-8
 
{
    "access":
        {
            "token":
                {
                    "expires": "Tue Jul  7 15:39:01 2015",
                    "id": "AUTH_TOKEN"
                },
            "user":
                {
                    "id": 10,
                    "name": "USER_NAME"
                }
        }
}
```

##### GET /user/USER_ID
Retrieve the user's entry in the user database

###### Request Headers
1. Accept: application/json
2. Content-Type: application/json
3. X-Auth-Token: <TOKEN_ID> (from /tokens POST)

###### Request JSON Object
1. None

###### Response JSON Object
1. User 
  * id (string) – Unique user ID
  * name (string) – Username
  * password (string) – Password

###### Status Codes
1. 200 OK - Request completed successfully

###### Request
```
GET /user/1 HTTP/1.1
Host: 192.168.13.37:8081
X-Auth-Token: AUTH_TOKEN
Content-type: application/json
Accept: text/plain
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 0


```

###### Response
```
HTTP/1.0 200 OK
Date: Mon, 06 Jul 2015 22:08:56 GMT
Server: WSGIServer/0.1 Python/2.7.9
Content-Length: 73
Content-Type: application/json
 
{
    "response":
        {
            "user":
                {
                    "password": "PASSWORD",
                    "id": USER_ID,
                    "name": "USER_NAME"
                }
        }
}
```

## Problems with install

