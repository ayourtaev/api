s4u
==============

# Installation
--------------
* Create virtualenv
**mkvirtualenv env -p python3.5**
* turn on your virtualenvironment. 
* instal dev utils into virtual environment
**pip install -r req.txt**


# Running tests
--------------
* ./manage.py tests

# Running
--------------
* Migrate database
**./manage.py migrate**
* Load fixtures
**./manage.py loaddata api/fixtures/initial_data.json**
* Run application
**./manage.py runserver**

## Additional
--------------
create new auth token key: 
**./manage.py create_auth_token**
![Example](http://joxi.ru/8235YNNhJY1dpr.png)

## URL desctiption:
---------------
## Accounts API
--------------

Method: POST **/api/v1/accounts**

# Parameters
**Header parameters:**

 NAME  | Is Mandatory? | Description  
------------ | ------------- | -------
Content-Type |  Yes  | Data exchange takes place by means of json messaging
Authorization| Yes  | Shared key for authorization

**Body parameters:**

 NAME  | Is Mandatory? | Description  
------------ | ------------- | -------
    currency   |      Yes      | Type of currecny. Can be EUR, USD, GBP or CHF
    balance    |      No      | Start balance on you account can't be more then 99999999.99 and less then 0. Max length - 10 digits            
      

**Response Codes:**

  Code   |                      Description                      
-------- | ------------------------------------------------------
   201   | Account successful created    
   422   | "currency" is required field                             
   422   | "currency" should be one of "USD", "EUR", "GBR" or "CHF"               
   422   | negative balance on any account are not permitted.                

**Request example**

```json
{
	"currency":"EUR",
	"balance": "578.38",
}
```
**Response example**

```json
{
    "data": {"accountNumber": "88205324"},
    "error": "false"
}
```
## Transaction api
--------------

Method: POST **/api/v1/transactions**

Parameters
**Header parameters:**

 NAME  | Is Mandatory? | Description  
------------ | ------------- | -------
Content-Type|      Yes      |Data exchange takes place by means of json messaging
Authorization| Yes  | Shared key for authorization

**Body parameters:**

 NAME  | Is Mandatory? | Description  
------------ | ------------- | -------
    sourceAccount   |      No      | Source account number, should be if destAccount is absent. Max length - 10 digits
  destAccount  |      No      | Destination account number, should be if sourceAccount is absent. Max length - 10 digits
  amount | Yes | Amount of transaction, change balance for account or accounts, can't be more then 99999999.99


**Response Codes:**

  Code   |                      Description                      
---------|-------------------------------------------------------
   201   | Transaction successful created 
   422   | Amount can't be less then 0
   422 | "sourceAccount" and "destAccount" are not specified
   422 | "sourceAccount" and "destAccount" numbers are identical
   422 | "sourceAccount" or "destAccount" contain less than 8 digits
   422 | wrong number of sourceAccount
   422 | wrong number of destAccount
   422 | the amount  is too lage for that account balance

**Request example**

```json
{
	"sourceAccount": "44882998",
	"destAccount": "88205324",
	"amount": 77233
}
```
```json
{
	"sourceAccount": "64183998",
	"destAccount": "",
	"amount": 77
}
```
**Response example**

```json
{
    "data": {
        "transaction_state": "completed",
        "transactionNumber": "27117685"
    },
    "error": "false"
}
```
## UI
--------------
List of accaunts availabl with help of links: **/api/v1/list_of_accounts**

![Example](http://joxi.ru/8AnBl44Fj46eaA.png)

List of transactions for the specific account availabl by clicking on the account number
or with help of direct link: **/api/v1/account_transactions/44882998/**

![Example](http://joxi.ru/KAxjkZZhMDxgom.png)
