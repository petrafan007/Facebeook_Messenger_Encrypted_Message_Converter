This file was created when my girlfriend got another android phone and when she logged into her Facebook Messenger account, all of our past interactions were gone. She was very sad and nothing we tried worked. Like any good boyfriend, I worked hard for a solution! 
Unfortunately, requesting and downloading all your information from Facebook do not include Encrypted Messages. To retrieve those, you must download them from Facebook Messengers Secure Storage.
In my research, I found that there were SOME scripts and programs that supposedly offered a solution, but either they didn't work or they didn't work with Encrypted Messages. THIS does!

Instructions:
1. Request a download of your secure storage from Facebook Messenger (instructions can be found online).
   Note: You will recieve a zip file with all of your encrypted messages in JSON files and also a media folder which will contain all of the pictures, videos and voice memos sent and recieved from everyone in the list. Be cautious!
2. Extract files and put the JSON files and the media folder in a new folder on your computer.
3. Download the facebookmessengerconvert.py file and put it in the same directory as your JSON files.
4. Right click inside the folder and select "Open in terminal".
5. type 'python facebookmessengerconvert.py without the single quotes and press enter.
6. The program will open. You have 2 options: either select a single JSON to convert or "Convert All". The first option allows you to select a single file and will automatically run. The second will have you select the existing folder you are in and press ok.

   And that's it! This will create a new HTML file(s) that will display the names, dates & times, messages and reactions of each person. Any Media files that were sent and/or recieved will also display right in the HTML file as well. All media will be placed in their
   respective folders.

   Note: A results window will appear at the end. If any files do not contain messages, they will be skipped.

   Please reach out to me if you notice any issues or bugs with the process or would like to request any enhancements. Thank you kindly! <3

   Joseph J. Cavallaro Jr.
