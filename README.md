# domcek_appka_backend

This code serves as a backend for domcek_appka, a Flutter based mobile application for Domcek

The communication between the server and the app is done using websockets.

Users can do multiple things on the app, such as give feedback about the action, ask the current guest a question.
The moderators have a special functionality, ask_guest. This sends the list of user-submitted questions through the websocket.
 
The app opens a connection to the server only when a user submits the form and when the communication will take place.
To determine which actions the app wants to perform, function request() is called after establishing the connection

Server is configured to be hosted on 192.168.0.189 on port 44332. 
Change this only after you change variable socketChannelAddress in main.dart in repo domcek_appka.
