# This code serves as a backend for domcek_appka, a Flutter based mobile application for Domcek
#
# The communication between the server and the app is done using websockets.
#
# Users can do multiple things on the app, such as give feedback about the action, ask the current guest a question.
# The moderators have a special functionality, ask_guest. This sends the list of user-submitted questions through the websocket.
# 
# The app opens a connection to the server only when a user submits the form and when the communication will take place.
# To determine which actions the app wants to perform, function request() is called after establishing the connection


import websockets
import asyncio

ip = "192.168.0.189"
port = 44332

possible_requests = ['feedBK', 'qGuest', 'askGst']
connected = set()
data = ""
feedback_questions = ["Q1", "Q2", "Q3"]
questions_for_guest = []

def save_in_file(data, file_name):
    with open(file_name, "a") as file:
        file.write(data)
        file.write("\n")
        file.close()

async def handler(websocket, path):
    # Register the user
    connected.add(websocket)
    print("Connection accepted from " + str(websocket.remote_address))
    try:
        while True:
            data = await websocket.recv()
            print("Received: " + data)
            command = data[:6]
            print("The command is: " + command)
            if command in possible_requests:
        # Give feedback
                if command == 'feedBK':
                    response = data[6:]
                    for question in feedback_questions:
                        q, response = extractQuestions(response)
                        save_in_file(q, "feedback/" + question + ".txt")
                        
        # Question for guest
                elif command == 'qGuest':
                    print("Question for guest")
                    print(data[6:])
                    question = data[6:]
                    save_in_file(question, "guest/guestQuestions.txt")

        # Send over all of the submitted questions
                elif command == 'askGst':

                    with open("guest/guestQuestions.txt", "r") as file:
                        questions_for_guest = file.readlines()
                    print(questions_for_guest)
                    for question in questions_for_guest:
                        await websocket.send(question)
                        




                    
            else:
                print("Unknown command")
                await websocket.send("Unknown command")
          
    except websockets.exceptions.ConnectionClosed as userDisconnect:
            print("User disconnect: " + str(websocket.remote_address))
            connected.remove(websocket)
            data = ""
            command = ""

async def echo(websocket, path):
    while True:
        
        data = await websocket.recv()
        print("Received: " + data)

        await websocket.send(data)
        print("Sent: " + data)


""" The first character of the string is a number, size_response. This number
    carries information about the length of the response, namely how many digits
    does the length of the response have.
    
    This way, strings of virtually any length can be parsed without problems.
    
    The next n characters (dependent on the size_response) is the actual number
    of bytes the reponse takes up, the length_response.

    Next m characters (dependent on the length_response) is the response itself.

    After dividing and storing the parts, they are removed from the string,
    as to allow the same algorithm to be called again.

"""

testCase = "216viem programovat212novy projekt213Ste supeeeer!"

def extractQuestions(data):   
    counter = 0    
    size_response = int(data[counter])
    
    # Move to the first byte of the length of response
    counter += 1
    length_response = int(data[counter: (counter + size_response)])

    # Move to the first byte of the response
    counter += size_response
    response = data[counter:(counter + length_response)]

    # Get rid of the used bytes
    counter += length_response
    data = data[counter:]

    return response, data

print("Hosting server on " + ip + " on port " + str(port))  
start_server = websockets.serve(handler, ip, 44332)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()








