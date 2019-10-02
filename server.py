# This code serves as a backend for domcek_appka, a Flutter based mobile application for Domcek
#
# The communication between the server and the app is done using websockets.
#
# Users can do multiple things on the app, such as give feedback about the action, ask the current guest a question.
# The moderators have a special functionality, ask_guest. This sends the list of user-submitted questions through the websocket.
# 
# The app opens a connection to the server only when a user submits the form and when the communication will take place.
# To determine which actions the app wants to perform, function request() is called after establishing the connection
#
# Server is always hosted on 192.168.0.182 on port 44332


import websockets
import asyncio

ip = "192.168.0.182"
port = 44332

possible_requests = ['feedback', 'question_for_guest', 'ask_guest']
connected = set()
data = "nothing"

feedback_questions = ["Q1", "Q2", "Q3"]
questions_for_guest = []

def save_in_file(data, file_name):
    with open(file_name, "a") as file:
        file.write(data)
        file.write("\n")
        file.flush()
        file.close()

async def handler(websocket, path):
    # Register the user
    connected.add(websocket)
    print("Connection accepted from " + str(websocket.remote_address))
    while True:
        try:
            await websocket.send("Ready")
            request = await websocket.recv()
            print(request)
            if request in possible_requests:
                if request == 'feedback':
                    print("Receiving feedback")
                    for question in feedback_questions:
                        print("Ready " + question)
                        await websocket.send("Ready " + question)
                        data = await websocket.recv()
                        print(data)
                        save_in_file(str(data), "feedback/" + question + ".txt")

                elif request == 'question_for_guest':
                    await websocket.send("Receiving question: ")
                    data = await websocket.recv()
                    print(data)
                    save_in_file(data, "guest/guestQuestions.txt")
                    print("Question saved")
                
                elif request == 'ask_guest':
                    print("Sending questions for guest")
                    with open("guest/guestQuestions.txt", "r") as file:
                        questions_for_guest = file.readlines()
                        print(questions_for_guest)
                        for question in questions_for_guest:
                            await websocket.send(question)
                        await websocket.send("done")
            else:
                await websocket.send("Dunno what that is")
                
        except websockets.exceptions.ConnectionClosed as userDisconnect:
            print("User disconnect: " + str(websocket.remote_address))
            break


   


print("Hosting server on " + ip + " on port " + str(port))  
start_server = websockets.serve(handler, ip, 44332)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()




