Project keywords: CustomTkinter, REST-API, Cloud-based NoSQL, Data processing, Mailtrap e-mail integration

DOCUMENTATION IS UNDER CONSTRUCTION. 

ABOUT THE APPLICATION

The idea behind the application is to provide the user with various financial information such as information on stocks, 
commodities and precious metals that the user is looking for. Depending on the user's choices, the application uses 
REST API interfaces (e.g. API-Ninjat, Newsapi) or RSS sources to search for information.

Communication between the REST API and the application takes place using Python's Requests library.
API results are received in json format, which are parsed into a readable format and displayed in the
application's textbox component. The Feedparser library is used for retrieving and parsing RSS feeds.

The user interface is implemented with the customTkinter library and it is possible to store the retrieved
data in the NoSQL cloud database used by the application. The cloud database is located in the Mongo Cloud Atlas service.

Example image of the application's start view

![alt text](images/FinancialMain.png)

CREDENTIAL SECURITY

All credentials used by the application, such as API keys, database usernames and passwords, are stored in a Python
environment variable. The environment variable is in Gitignore mode. The application retrieves credentials using the
Python OS library if necessary with the environ.get method.

VOICE COMMANDS

The user can control some of the application's functions with their own speech.
The application uses a library called SpeechRecognition and the device's microphone when listening to commands given by the user. For now these voice commands are available:

CLEAR = Clears the application's text box

STOCKS = Create an input field and two checkboxes in the user interface. The user needs them when looking for information about stocks

CRYPTO= Create an input field in the user interface. The user can use this input field when searching for information about cryptocurrencies.

STOCK INFO = Retrieves data from the API based on the trading ID of the stock entered by the user

SAVE = Saves the contents of the application's text box to the MongoDB cloud database used by the application

DATA STORAGE OPTIONS (Database,CSV,PDF)

All data retrieved from the API can be stored in a cloud-based Mongo NoSQL database or in a local csv/Pdf file. The user can choose which method to use. When using the database option, the application connects to the Mongo Cloud atlas using the MongoClient and ServerAPI classes. In the CSV file option, the application uses Panda Dataframe methods to save the data to the file. When using the csv saving method, the application uses the customTkinter file window, where the user can choose the name of the file and the storage location.

In the PDF option, the file is created using the Python reportlab library.

FORWARDING SAVED DATA BY E-MAIL

The user can forward the saved pdf file by e-mail. The application uses the Python Mailtrap client to send emails.

EMAIL VALIDATION

Before sending the email, the program checks that the entered email address is in the correct format. Validation is done with the API-NINJAS Validate Email API. When the user leaves the email field, the program executes a method that sends the entered email address to the Validate Email API. If the API check passes, the send button is enabled. Otherwise, the send button is disabled.

![alt text](images/emailValidReady.png)


STOCK & CRYPTO CURRENCY INFORMATION SEARCH

Stock/crypto information is searched using the stock's or crypto trading ID. For example, information on the Apple stock
is retrieved by entering the text AAPL in the input field of the application. The entered text is passed as a parameter to
the method that communicates with the REST API and retrieves the data using the Requests library. Finally, the result is 
displayed as parsed in the Customtinter textbox component. When searching for stock information, the user can also select
the "show earnings" check box. By clicking on that check box, the user sees not only the share information but also
the share's estimated earnings information.

FIND NEWS BY STOCK / CRYPTO / COMMODITY NAME

The application user can also search for the latest news based on the name of the stock, cryptocurrency or commodity of her choice by clicking on the "News" checkbox. This feature uses the Newsapi.org API to which the user-supplied keyword is passed as a parameter.

Example image where a user searches for news from NewsAPI using a Microsoft keyword. The program displays the news in relevant order using the 'relevancy' parameter in the API call sent to NewsApi.

![alt text](images/newsMicrosoft.png)


SEARCH RSS FEEDS

The application has 3 checkboxes for RSS feeds, Kauppalehti RSS, Investing RSS and a custom RSS url.
By clicking the Kauppalehti RSS or Investing RSS check box, the program retrieves the RSS feed of the
selected service using the Feedparser library, parses the result into XML tags and displays the feed 
in text form in the application's text field component. By clicking the checkbox of the custom URL address, 
the program creates an input field where the user can enter his own address, from which the RSS feed is retrieved.

CREATING GRAPHICS FROM SEARCHED VALUES

The application uses the Matplotlib library to create graphs of, for example, stock prices searched by the user.
A finished chart containing the name of a stock, cryptocurrency or commodity and its current value as a bar chart.

The user can also create more complex stock value charts. This figure shows the next three estimated EPS numbers for Apple stock. The EPS numbers are taken from the API's JSON response and stored in a Python list.
The Matplotlib library draws the figure based on the list values. List values ​​are sorted from smallest to largest using the Python List Sort method.

![alt text](images/plotApple.png)

