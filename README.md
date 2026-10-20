# fimfiction-stories-downloader

It downloads multiple stories from bookshelves, folders and other lists of stories on fimfiction.net. You can choose one of three file formats that are available on fimfiction.net.

It can download:
- public or unlisted bookshelves,
- folders with stories in groups,
- stories from the current page of a list of popular, stories, latest stories etc.,
- stories from the current page of a list of search results,
- stories from the homepage.

It cannot download:
- individual stories after you enter links to them,
- story chapters.

## How to Run the AutoHotkey Script

1. Download the [FimfictionDownloader.exe](https://github.com/GameBiit/fimfiction-stories-downloader/raw/refs/heads/main/FimfictionDownloader.exe).
2. Open Google Chrome or Mozilla Firefox and log in to fimfiction.net.
3. Set the “View Mature” toggle at the top of the page accordingly.
4. Go to the page where you want to download the stories and copy its URL from the address bar.
5. Minimise your browser window and open the file you downloaded earlier.
6. Enter parameters according to the instructions below and click 'OK':

Options:
```
-o, --out     Output folder
-a, --adult   y or n
-f, --format  txt, html, epub
-r, --range   1=current page, 2=all pages
Enter the URL last.
```

An example: ```-o downloaded_stories -a n -f epub -r 1 https://www.fimfiction.net/bookshelf/12345```

The example above creates a folder named 'downloaded_stories' in the folder containing the script, it switches off the visibility of mature content, sets the format to .epub and downloads only the stories on the first page.

6. Go back to your browser. The script will start running in a moment. 
7. Do not do anything on your computer until all the stories have finished downloading. This may take a while, so it's a good idea to take a break from your computer during this time. The script will show you the download status.

## The Python script described below is currently not working because it cannot handle Cloudflare's security mechanisms. Please use the AutoHotkey script described above instead.

To view the the program's command line arguments, run it with the '-h' or '--help' flag. If no arguments are specified, the program behaves as described below.

# Requirements:
1. Windows (7, 8 or 10), Linux or macOS.
2. Python 3+ (the compatibility was confirmed for Python 3.8 and 3.9).
3. Python libraries: requests, lxml, beautifulsoup4 and urllib3.

# How to run it on Windows?

## For users who do not know much about computers

1. Download and install the newest version of Python from https://www.python.org/downloads (make sure that you mark 'add Python ... to PATH' and click 'Install Now' in the installer to avoid potential problems),
2. Download this program from GitHub by clicking the green button with the word "<> code" on the top of the page,
3. Unpack the zip file somewhere,
4. Go do the unpacked folder with the program and open the 'python libraries installer.bat',
5. Open 'script starter.bat',
6. Answer a few simple questions to indicate what you want to download. The program uses the card view to count the number of stories and pages so you have to keep that in mind when you paste links into it.
7. Stories will be saved to the folder 'downloaded_stories' that will be automatically created in the folder with the program.

## For computer enthusiasts
1. Install the newest version of Python if you don't have it yet. You can download it here: https://www.python.org/downloads/. Make sure that you mark 'add Python ... to PATH' and click 'Install Now' in the installer to avoid potential problems.
2. Install the Python libraries if they are missing or if you are not sure if you have them. You just have to double-click on the 'python libraries installer.bat'. The other method is to use these commands in the command line:
```
pip install requests
pip install lxml
pip install beautifulsoup4
pip install urllib3
```
3. Download the whole package by clicking the green button at the top of this page (but don't forget to unpack it) or at least these files:
- 'fimfiction_stories_downloader.py',
- 'python libraries installer.bat',
- 'script starter.bat',
4. There are a few ways to run this program:
- Open the 'script starter.bat' to launch the script.
- Go to the folder with this program. Then press Shift + right click mouse button anywhere in the folder window and select the 'Open command window here' option from the context menu. Then enter 'python fimfiction_stories_downloader.py' and click Enter.
- Open the 'command line' and go to the directory with the program files using the 'cd' command. Then enter 'python fimfiction_stories_downloader.py' to launch the script. You can also add the full path after 'python'.
5. Answer a few simple questions to indicate what you want to download. The program uses the card view to count the number of stories and pages so you have to keep that in mind when you paste links into it.
6. Stories will be saved to the folder 'downloaded_stories' that will be automatically created in the current working directory.

# How to run it on Linux?
1. Python 3+ is installed by default in the newest versions of Linux distributions. Normally the only things that are missing are the 'pip' and libraries. You have to open the terminal and enter:
```
sudo apt install python-3 pip
```
2. Then provide the root password and either run 'python_libraries_installer.sh' or install the libraries manually by running these commands:
```
pip3 install requests
pip3 install lxml
pip3 install beautifulsoup4
pip3 install urllib3
```
3. Download the 'fimfiction_stories_downloader.py'
4. Now find out the address of the file by checking its properties and enter it into the terminal after 'python3" to start the program. It should looks similar to this one:
```
python3 /home/user/Desktop/fimfiction_stories_downloader.py
```
5. Answer a few simple questions to indicate what you want to download. The program uses the card view to count the number of stories and pages so you have to keep that in mind when you paste links into it.
6. Stories will be saved to the folder 'downloaded_stories' that will be automatically created in the current working directory.

# How to run it on macOS?
You have to figure it out yourself.
