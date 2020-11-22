# fimfiction-stories-downloader
It downloads multiple stories from bookshelfs, folders and other lists of stories on fimfiction.net. You can choose one of three file formats that are available on fimfiction.net.

It can download:
- public or unlisted bookshelfs,
- folders with stories in groups,
- stories from the current page of a list of popular, stories, latest stories etc.,
- stories from the current page of a list of search results,
- stories from the homepage.

It cannot download:
- individual stories after you enter links to them,
- story chapters.

# Requirements:
1. Windows (7, 8 or 10), Linux or macOS.
2. Python 3+ (the compatibility was confirmed for Python 3.8 and 3.9).
3. Python libraries: requests, lxml and beautifulsoup4. 
  
# How to run it on Windows?
1. Install the newest version of Python if you don't have it yet. You can download it here: https://www.python.org/downloads/. Make sure that you mark 'add Python ... to PATH' and click 'Install Now' in the installer to avoid potential problems.
2. Install the Python libraries if they are missing or if you are not sure if you have them. You just have to double-click on the 'python libraries installer.bat'. The other method is to use these commands in the command line:
```
pip install requests
pip install lxml
pip install beautifulsoup4
```
3. Download the whole package (but don't forget to unpack it) or at least these files:
- 'fimfiction_stories_downloader.py',
- 'python libraries installer.bat',
- 'script starter.bat',
4. There are a few ways to run this program:
- Open the 'script starter.bat' to launch the script.
- Go to the folder with this program. Then press Shift + right click mouse button anywhere in the folder window and select the 'Open command window here' option from the context menu. Then enter 'python fimfiction_stories_downloader.py' and click Enter.
- Open the 'command line' and go to the directory with the program files using the 'cd' command. Then enter 'python fimfiction_stories_downloader.py' to launch the script. You can also add the full path after 'python'.
5. Answer a few simple questions to indicate what you want to download. The program uses the card view to count the number of stories and pages (except for search results, popular stories etc.) so you have to keep that in mind when you paste links into it.
6. Stories will be saved to the folder 'downloaded stories' that will be automatically created in the same folder where you put the program.

# How to run it on Linux?
1. Python 3+ is installed by default in the newest versions of Linux distributions. Normally the only things that are missing are the 'pip' and libraries. You have to open the terminal and enter:
```
sudo apt install python-3 pip
```
2. Then provide the root password and enter:
```
pip3 install requests
pip3 install lxml
pip3 install beautifulsoup4
```
3. Download the 'fimfiction_stories_downloader.py'
4. Now find out the address of the file by checking its properties and enter it into the terminal afer 'python3" to start the program. It should looks similar to this one:
```
python3 /home/user/Desktop/fimfiction_stories_downloader.py
```
5. Answer a few simple questions to indicate what you want to download. The program uses the card view to count the number of stories and pages (except for search results, popular stories etc.) so you have to keep that in mind when you paste links into it.
6. Stories will be saved to the folder 'downloaded stories' that will be automatically created in the same folder where you put the program.

# How to run it on macOS?
You have to figure it out yourself.
