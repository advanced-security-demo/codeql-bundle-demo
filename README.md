# What is vAPI

vAPI is an API written specifically to illustrate common API vulnerabilities.
It is implemented using the Bottle Python Framework and consists of a user database and a token database.

## How is different from all the other vulnerable-API forks on GitHub?

1. It adds basic application logging (vAPI.log) for purple teaming demo purposes! 
2. Log format is Splunk CIM comliant key=value right out of the box.

## Usage

1. git clone https://github.com/jorritfolmer/vulnerable-api.git
2. yum install python-lxml
3. yum install python-paste
4. yum install python-pip
5. pip install bottle
6. python ./vAPI.py -p \<port\>
7. have fun with OWASP ZAP or Burp

## vAPI Process flow

1. Request token from /tokens
  * Returns an auth token
  * Returns expiration date of auth token
  * Returns a user id
2. Request user record from /user/<user_id>
  * Requires the auth token
  * Returns the user record for the user specfied, provided the auth token is not expired and is valid for the user id specified
  * Each user can only access their own record
3. Request widget reservation from /widget

## Swagger and OpenAPI Spec 3

Also contained in this repo are API specification files to load in e.g. Burp or OWASP ZAP for fun and profit.

- A Swagger 2.0 definition file: vAPI-oas2.json
- An OpenAPI Spec 3 (OAS3) file: vAPI-oas3.yaml

## Known vulnerabilities

1. Insecure transport
2. User enumeration
3. Information disclosure
4. Authentication bypass
5. No input validation
6. SQL injection
8. Weak session token crypto
9. Poor session validation
10. Plaintext storage of secrets
11. Command injection
12. Regex denial of service
13. Cross Site Scripting
14. XML XXE and billion laughs
15. Missing security headers 

### Vulnerabilities per endpoint

| method | endpoint       | input               | vuln            
|--------|----------------|---------------------|-----------------
| GET    | /              | -                   | 15              
| GET    | /tokens        | -                   | 10              
| POST   | /tokens        | post                | 14              
| POST   | /tokens        | post:username       | 2, 6, 8, 13, 14 
| POST   | /tokens        | post:password       | 2, 6, 8, 13, 14 
| GET    | /user/{userid} | header:x-auth-token | 4, 6, 8, 9      
| GET    | /user/{userid} | get: userid         | 2, 6, 10, 12    
| POST   | /user          | header:x-auth-token | 4, 6, 8, 9      
| POST   | /user          | post:username       | 6, 9, 12, 13    
| POST   | /user          | post:username       | 6, 9, 13        
| GET    | /uptime        | -                   |                 
| POST   | /uptime        | post:flag           | 11, 13          
| POST   | /widget        | header:x-auth-token | 4, 6, 8, 9      
| POST   | /widget        | post:widget         | 12              


