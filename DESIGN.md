# final project design

First off we start in the homepage, where we can either log in or register. We decided to start with Login becasue usually other websites start that way too. If you have an account and sucessfully log in then the homepage will display more options in your nav var (quiz, workout, weight log, tutorials and calendar) else you will continue to be in that page until you have registered or logged in. Meanwhile if you enter information wrong an error message will appear. You will be logged in if your username and password is in the database users, and if you register your information will be inserted in the same table so you can later log back in.

Once you have logged in, you are transported to the greet slide, where you can choose any of the options in the nav var and it will take you to the corresponding slides. If you go to quiz, you will be prompted with two questions that ask you your choices to workout, after you have answered the questions with one answer each, the workout_style comlumn in the users database will be updated with the designated number that the style of workout has (you can take the quiz multiple times and it will update each time). If this is your first time in the website and you do not take the quiz first, you will not be able to see any videos in tutorials or your workout plan in workout.

If you have taken the quiz, then you will be able to use the workout slide. It will display the workout that you chose based on your answers to the quiz, each combination of answers has a specific number assigned to it that will based on this display a different workout plan depending on it. In this page you will be able to log your weights if you chose in the quiz that you will be workout in the gym because those worokouts will have weights included. So at the end of the workouts you will have the option to log your weights by inputting the name and weight of the exercise. Once the user hits record, the userid, name of exercise, weight and date will be recorded in the weight-log database (or inputted). You will be able to see your progress in the weight log slide, where a table will appear with all the inputs that the account user has done. 

In the tutorials page you will be able to see guiding videos depending on the workout setting that you chose in the quiz. In the database videos, we have inputted all of the urls of the videos and its designed category with a number. For example, we have home upper body and lower body and gym upper body and lower body. So that is 4 categories, however, in the tutorials page you will not have all of them because it is counter productive, so the videos will be displayed only based on the environment that you chose in the quiz, so if you chose gym only gym guiding videos will appear. 

We have the calendar slide which will have a space for the user to input events in their to do list for the month. The user may input the event name, day, month, and year, and this will be recorded in the calendar database together with the current userid to sort out the different users events. Then under we have the calendar of the current month and year, where the user can have a visual representation of their month and under it a table that will display the events that the user has planned for the current month. 

Lastly, if the user presses the log out button in the nav var, it will redirect him to the log in page so they would have to sign in again.

Thank you for your time,

Celeste and Dalila

