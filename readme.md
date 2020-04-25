# Invoice Generator
A simple application which generated invoice and mails the invoice to the customer.
- Kivy and KivyMD is used to create the user interface of the application.
- Node JS is used to create an api, which accepts the GET request along with the invoice details in JSON format, generated the invoice pdf and mails it to the customer.
- Sqlite is used to store the details in the local machine.

------------
### How to setup and run?
###### Python
- Install Kivy and KivyMD using pip commands.
- Run invoice.py and you should be able to view the UI
- Make sure you have the MyTable.py and kivytoast.py in the same location as invoice.py

###### Node JS
- The Node Application is built and deployed in Heroku.

### UI Snippets
>Menu

![Launch Screen](https://github.com/balajiRchandran/Invoice-Generator/blob/master/UI%20Snippets/First.PNG)

>Add Items

![Add Item](https://github.com/balajiRchandran/Invoice-Generator/blob/master/UI%20Snippets/Second.PNG)

>View Records

![Records](https://github.com/balajiRchandran/Invoice-Generator/blob/master/UI%20Snippets/Three.PNG)

>Generated Invoice

![Invoice](https://github.com/balajiRchandran/Invoice-Generator/blob/master/UI%20Snippets/GenInv.PNG)

>Mail Screenshot

![Mail](https://github.com/balajiRchandran/Invoice-Generator/blob/master/UI%20Snippets/Mail.PNG)

