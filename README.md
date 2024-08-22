# Blum-Hack - automation of the crypto game “Blum”

A program that automates actions in the crypto game “Blum”

# Quick Start

*  Download [latest version from Releases page](https://github.com/Argona7/Blum-Hack/releases), and run the program.

# How does it work 

**The program does automation with post queries, the actions it automatically performs:**

* Get daily reward
* Claim farming reward
* Start farming
* Claim points for friends
* Start game
* Claim points for game

Requests are sent to the server thanks to an access token, which can be obtained by sending a post **_refresh_** request with the body of the request:
```
{
  "refresh" : "your_refresh_token"
}

```
Response to this request:
```
{
"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiQUNDRVNTIiwiaXNzIjoiYmx1bSIsInN1YiI6IjQxMjMzZjAxLWJlY2EtNDJmZi1hYzVlLTU1YWYwNDc1N2QzNyIsImV4cCI6MTcyNDMyMDM2NywiaWF0IjoxNzI0MzE2NzY3fQ.vbVSWcJIsGDrEtrtzwyqiLyhNjuhh0ryjEGUQdaifIs",
"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiUkVGUkVTSCIsImlzcyI6ImJsdW0iLCJzdWIiOiI0MTIzM2YwMS1iZWNhLTQyZmYtYWM1ZS01NWFmMDQ3NTdkMzciLCJleHAiOjE3MjQ0MDMxNjcsImlhdCI6MTcyNDMxNjc2N30._sryyhaxPoL8rDI6-GS_pHQfawc7DlntDZ7qEBTb7xg",
"user":null
}

```
Refresh token from the response we have to use next time in the same request to get the access token and the next refresh token and so on in a circle.

The refresh request should be sent after an hour from the previous request.

# How to track a request

**In order to trace the request you need to [run Blum in web telegram and bypass the protection](https://www.youtube.com/watch?v=IirK5IDyNVU). With the help of the ***DevTools*** in the ***Network*** section you will be able to find the request “refresh”**

###

# How to use

Download [latest version from Releases page](https://github.com/Argona7/Blum-Hack/releases) and run.
After that, the program will create a json document called **_refresh_tokens_** which must be filled in manually on the path **“C:\Users\ Your user.“**

* ### How the json file should be filled in:
```
{
    "accounts": {
        "@YouTelegramAccountName": {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiUkVGUkVTSCIsImlzcyI6ImJsdW0iLCJzdWIiOiI2NjZkMWRlNi04ODI3LTQxYjgtOGJlZS0wYjJkNTkxZmViMTIiLCJleHAiOjE3MjQ0MDI2ODYsImlhdCI6MTcyNDMxNjI4Nn0.EgeIyXlUMXCN7U0aKZYlvzDpE75rluOCtQahtVYBkpY",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiQUNDRVNTIiwiaXNzIjoiYmx1bSIsInN1YiI6IjY2NmQxZGU2LTg4MjctNDFiOC04YmVlLTBiMmQ1OTFmZWIxMiIsImV4cCI6MTcyNDMxOTg4NiwiaWF0IjoxNzI0MzE2Mjg2fQ.OrP-5k2tcC_cXaKAbkVq11K4t9vr6cOJyEwRBiOZoT8",
            "refreshed": false,
            "timestamp": 0
        },
        "@YouTelegramAccountName": {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiUkVGUkVTSCIsImlzcyI6ImJsdW0iLCJzdWIiOiJmNjZkN2Y5MS1kMzBmLTQ3ZWQtYjg4Mi02NjZjNGVkY2YwNGQiLCJleHAiOjE3MjQ0MDI5MjYsImlhdCI6MTcyNDMxNjUyNn0.VFxItO6PVOIDlk15kiJOyRnyax2bsDECNMqNgcuB_Ks",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiQUNDRVNTIiwiaXNzIjoiYmx1bSIsInN1YiI6ImY2NmQ3ZjkxLWQzMGYtNDdlZC1iODgyLTY2NmM0ZWRjZjA0ZCIsImV4cCI6MTcyNDMyMDEyNiwiaWF0IjoxNzI0MzE2NTI2fQ.2MQOSl2uGIDjyynPTdIdTzNvve2ceesmVzY6mKPDT4U",
            "refreshed": false,
            "timestamp": 0
        },
        "@YouTelegramAccountName": {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiUkVGUkVTSCIsImlzcyI6ImJsdW0iLCJzdWIiOiI0MTIzM2YwMS1iZWNhLTQyZmYtYWM1ZS01NWFmMDQ3NTdkMzciLCJleHAiOjE3MjQ0MDMxNjcsImlhdCI6MTcyNDMxNjc2N30._sryyhaxPoL8rDI6-GS_pHQfawc7DlntDZ7qEBTb7xg",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiQUNDRVNTIiwiaXNzIjoiYmx1bSIsInN1YiI6IjQxMjMzZjAxLWJlY2EtNDJmZi1hYzVlLTU1YWYwNDc1N2QzNyIsImV4cCI6MTcyNDMyMDM2NywiaWF0IjoxNzI0MzE2NzY3fQ.vbVSWcJIsGDrEtrtzwyqiLyhNjuhh0ryjEGUQdaifIs",
            "refreshed": false,
            "timestamp": 0
        },
        "@YouTelegramAccountName": {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiUkVGUkVTSCIsImlzcyI6ImJsdW0iLCJzdWIiOiIyZTU1NTk5NC1lOWQxLTQwZjctOWUyOS1jNDI0NTQ5OWVjZTUiLCJleHAiOjE3MjQzNTQzMDgsImlhdCI6MTcyNDI2NzkwOH0.2f2jNW4haLdYeJDnMuirwdLY1Vj_NGKdtN2rBvCJcsE",
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJoYXNfZ3Vlc3QiOmZhbHNlLCJ0eXBlIjoiQUNDRVNTIiwiaXNzIjoiYmx1bSIsInN1YiI6IjJlNTU1OTk0LWU5ZDEtNDBmNy05ZTI5LWM0MjQ1NDk5ZWNlNSIsImV4cCI6MTcyNDI3MTUwOCwiaWF0IjoxNzI0MjY3OTA4fQ.cFEWguWP8KmGvugccl0rw00jhs7UAoYnbyUVptkTe7o",
            "refreshed": false,
            "timestamp": 0
        }
    }
}
```
* ### [Guide on how to get Access token and Refresh Token](#how-to-track-a-request)

**After that, once you have properly modified the file, restart the application
You will be prompted to exclude accounts from the automation list, simply type the account name or account names with a space.  
Enjoy the app!**

# Farewell and Final Thoughts

As I wrap up this journey, I want to extend my heartfelt thanks to everyone who has been a part of it. This project has been an incredible experience, and I'm proud of what we've accomplished together. Although it's time to move on, the memories and lessons learned here will always stay with me. Until we meet again!
