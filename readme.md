# Invoice Generator
A simple application which generated invoice and mails the invoice to the customer.
- Kivy and KivyMD is used to create the user interface of the application.
- Node JS is used to create an api, which accepts the GET request along with the invoice details in JSON format, generated the invoice pdf and mails it to the customer.
- Sqlite is used to store the details in the local machine.

------------
### How to setup and run?
###### Python
1. Install Kivy and KivyMD using pip commands.
1. Run invoice.py and you should be able to view the UI
1. Make sure you have the MyTable.py and kivytoast.py in the same location as invoice.py

###### Node JS
1. Create a new directory and change to the new created directory.
1. Run the following commands to initialise the project and to install the required modules
		npm init
		npm install express --save
		npm install pdfkit --save
		npm install nodemailer --save
1. Move the downloaded node script files to the created project and change the mail id and password in index.js script
1. Start the server/invoice api using the command,
		node index.js
1. Now your server is running in the port 3000 and you can send request to it by http://localhost:3000
1. The python application gets the user input, convert it into JSON and sends the data to the Node api, which will generate and sends the invoice through mail.

### UI Snippets


