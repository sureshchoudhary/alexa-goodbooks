# alexa-goodbooks
This is a project for creating Amazon Alexa Skill "Good Books".

##Getting Started ##
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

###Prerequisites ###
1. Python3
  * Download Python3 for your OS from ftp server (https://www.python.org/ftp/python)
  * Install Python3
  
2. pip 3 - python package management system
   ~~~~
   yum install python-pip3
   ~~~~

3. Install the modules required
   ~~~~
   pip install -r requirements.txt
   ~~~~

###Steps to test the app locally:###
1. Run the app using python3:
   ~~~~
   python goodbooks_app.py
   ~~~~

2. Open another terminal and serve using ngrok (https://ngrok.com/download)
   ~~~~
   ./ngrok http 8080
   ~~~~
  You will obtain urls pointing to your app. Enter the https URL into your ASK Configuration -> Endpoint.

###Steps to deploy the app on AWS Lambda:###
1. Set the aws access credentials. Create ~/.aws/credentials file, if it does not already exist, with the following content (replace the place holders with appropriate values:
   ~~~~
   [default]
   aws_access_key_id=<accesskey>
   aws_secret_access_key=<secretaccess>
   ~~~~

2. Set the default region. Create ~/.aws/config file, if it does not already exist, with the following content:
   ~~~~
   [default]
   region=us-east-1
   ~~~~

3. Run the scripts using python3:
   ~~~~
   zappa deploy test
   ~~~~
  You will obtain the apigateway URL. Enter this URL into your ASK Configuration -> Endpoint.
