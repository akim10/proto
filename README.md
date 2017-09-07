# proto
Proto: 15-112 Term Project

This was the final project for 15-112: Fundamentals of Programming and Computer Science. 
I created a collaborative protyping application with Python's built-in graphical library, tkinter.
This uses the socket and pickle modules to allow two or more users to edit and test mobile prototypes together in real time.

# How to launch Proto:

1. Run protoServer.py, it will begin looking for a connection.
2. Run protoClient.py, it will connect to the server that was run in step 1.

NOTE: Make sure that the 'PORT' number on line 8 of protoServer.py is the exact same as the 'PORT' number on line 11 of protoClient.py
If there are any errors, try adding +1 to each 'PORT' number. 

3. Register and log in to begin!
