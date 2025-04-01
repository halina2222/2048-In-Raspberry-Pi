Introduction:
This project focuses on developing a gesture classification system in Raspberry Pi and Sense Hat.
Aims to recognize and classify hand gestures in 
real-time, allowing players to control game (2048) through a natural and 
intuitive way instead of traditional controllers/keyboard. By integrating 
machine learning techniques, the embedded system processes input from the
camera to detect specific gestures, like open palm and close palm. Then, 
translate them into game commands. This approach makes gaming more 
interactive and interesting.
Gesture Detection
The provided file: model, point_histor_classification.ipynb, app.py, simple.py,
and call.py are used for model training and the execution the gesture 
classification. The referenced project designed by Kazuhito00, translated by 
kiniv, Hand-gesture-recognition-using-mediapipe, provide an easier approach
for hand-landmark capturing, and fit in to the MediapPipe framework, thus to 
do the gesture classification. The referenced project gives a simpler way to
input a new gesture and test the model(app.py). The training process in
point_histor_classification.ipynb and output to the model folder. In this project, 
total 4 gestures are used: they are Open palm, Close palm, Peace Sign and 
Thumbs up(may check in 
/model/keypoint_classifier/keypoint_classifier_label.csv). The model can 
recognizer the input from both hands, but only one hand can be the input of 
the game command. Then the simple.py will run the model in real time, can 
return the classified gesture from the camera. Last, the call.py will check the 
changes of the gesture, to prevent the one gesture be detected more than 
once.

Modified “2048” Game:
The provided file: 2048.py control the whole embedded system’s workflow. 
1) At the first, the sensehat will show prompt: “Welcome to the 2048 tile!!” on 
the 8*8 LED Matrix.
2) Then, it will show the gameboard of the 2048 game. In the initial state, 
there will be 6 tiles for merging or moving.
Next, the game will check whether the board is winning or losing. 
3) In terms of the wining condition, if the player can get an orange color
(255,165,0) tile (512), the player will win. Otherwise, continue the game.
When the game is won, there will be a prompt “Congratulation” show on 
SenseHat. Then, the player may choose to continue the game, restart the 
game or exit the game. there will be a prompt “Continue?Again?” show on 
SenseHat.
a) For continue the game, player must input a “Open Palm” gesture. If the 
input is successfully received, there will be a prompt “To be continue”
show on SenseHat. Then, the game will continue will the same 
gameboard until the game is lose. There will not be any win checking 
for the continued game. Other word, it will skip the step 3.
b) For restart the game, player must input a “Peace Sign” gesture. If the 
input is successfully received, there will be a prompt “Restarting” show 
on SenseHat. Then, the game will initialize the gameboard and restart.
c) For exit the game, player must input a gesture other than “Open palm” 
and Peace Sign”. If the input is successfully received, there will be a 
prompt “Thanks for playing?” show on SenseHat. Then, the program
will terminate.
4) In terms of losing condition, if there are no possible movement or the 
gameboard cannot add the new tiles, the game consider lose. Otherwise, 
continue the game.
When the game is lose, there will be a prompt “Game Over!” show on 
SenseHat. Then, the player may choose to restart the game or exit the 
game. there will be a prompt “Again?” show on SenseHat.
a) For restart the game, it is the same to 3b.
b) For exit the game, player must input a gesture other than Peace Sign”.
Other process is same to 3c.
The corresponding color on sense hat and number are shown below:
Number Color RGB representation

0 Blank (0,0,0)
2 Red (255, 0, 0)
4 Green (0, 255, 0)
8 Blue (0, 0, 255)
16 Yellow (255, 255, 0)
32 Purple (255, 0, 255)
64 Light blue (0, 255, 255)
128 Grey (128, 128, 128)
256 Light orange (255, 160, 97)
512 Orange (255, 165, 0)
1024 Pink (255, 105, 180)
2048 White (255, 255, 255)
4096 Light grey (238, 228, 218

6) After the checking, the program will activate the call.py program to get the 
gesture detected from the camera. If the movement it not available, it will 
activate the call.py program again until a valid movement is made.
Then, according to the gesture received, do the corresponding operation.
Gesture received Operation
Thumbs up Move Up
Peace Sign Move Down
Open palm Move Left
Close palm Move Right
7) After the execution of operation, two tiles will be added to the gameboard. 
And return to Step 2.

Experiment test
To ensure the game operates smoothly, we conducted thorough testing to 
identify any existing or potential errors in the game script, as well as to 
evaluate the performance of the gesture recognition system in terms of 
accuracy and latency.
For accuracy testing, we assessed how effectively the system recognized 
gestures by performing 50 trials with various random hand movements (e.g., 
open → close → PeaceSign → thumbs up → open, etc.). Out of these, 47 
gestures were correctly identified, resulting in an accuracy rate of 
approximately 94%. The most possible confusion is the thumbs up and close. 
When the thumbs up in certain rotated angle, the model may have confusion, 
but other performance performing well. This demonstrates that the gesture 
recognition system is highly reliable for the game's functionality.
For latency testing, we measured the response time between performing a 
gesture and the Sense HAT updating its display. Using a stopwatch and 
visual observation, we recorded an average response time of 0.7 seconds 
over 50 trials.
To detect any logical errors in the game script, we played the game multiple 
times to identify potential issues such as calculation errors, incorrect 
movements, or problems displaying win/lose messages. No errors were found 
during this testing phase, confirming the script's stability.
Discussions
The difference of a normal CPU architecture and the Raspberry Pi's CPU 
architecture brings a huge difficulty for this project. As the Raspberry Pi's CPU
architecture (ARM processors) are less powerful than the normal CPU 
architecture (x86 processors). A simpler program is needed due to limited 
computing power. In this project, we have simple_app.py to capture the 
gesture. Compared to the original app.py, the new program will not show the
real-time video stream captured by the camera. Instead, it will only give the 
result string of the detected gesture as output because rendering the video 
stream requires huge computing power which slow down the performance of 
our program. This approach indeed improves the performance in terms of 
latency. 
In addition, Raspberry Pi does not support Scalable Vector Extension (SVE)
which is a vector instruction set designed to improve the performance of 
workloads that involve large amounts of data in parallel. Since the gesture 
detection is a computing intensive task and the pretrained model in mediapipe 
expects SVE to deal with the huge amount of workload, Raspberry Pi may fail 
to handle the program and the excessive CPU usage and resource leaks may
freeze the whole OS. In our experiment, if the length of playing time is long 
enough (>3 minutes), the OS will probably freeze, and it requires rebooting to 
unfreeze. Our solution is to shorten the game playing time by making the goal 
easier (512) to reach and also making each step harder (add two tiles) to play. 
Therefore, the game has high probability to terminate before the Raspberry 
system breakdown.
