# Mouseshot
Purpose of this program is to monitor and to keep close track of what is happening on your computer. Nowadays, one can easily waste their precious time when using a computer thanks to the thousand of thousands of memes out there in the internet. 
Hopefully, there are programs such as this one in the internet that give human a chance to fight back.

> I don't believe that, with the click of a mouse, you should be able to buy unlimited amounts of ammunition. Bob Menendez


# Usage
After installing required python libraries by entering
`pip install -r requirements.txt`
into a terminal, the program can easily be started with 
`python mouseshot.py`.
Or instead of that, mouseshot and mouseshot-win venvs are provided for linux and windows os respectively, with the required libraries pre-installed. One can activate mouseshot by entering `source mouseshot/bin/activate` in a terminal on linux and `\Scripts\activate.bat` in a cmd on windows. Then run the program normally by entering `python mouseshot.py`. For deactivating just enter `deactivate`.

Change database destination to a static directory in your system and also mess with the height and width of the rectangle to your satisfaction.

# Output
This program screenshots an arbitrary sized rectangular on the screen with the mouse on its center, whenever any mouse button is pressed.


# Caution!
Remember to add the python code folder to exclusion in your system antivirus, as it may prevent the program to run properly.
