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
1. Windows 7, 8 or 10. Linux or macOS are not officially supported.
2. Python 3+. You can download it here: https://www.python.org/downloads/. If you have to install it, make sure that you mark 'add Python ... to PATH' and click 'Install Now' in the installer to avoid potential problems.
3. The Python libraries below are required to run this program. If you use windows, you can run the 'python libraries installer.bat' to download them automatically. You can also install them manually with the command line/prompt/console/terminal:
```
pip install requests

pip install lxml

pip install beautifulsoup4
```
  
# How to run it?
1. Download the the whole package or at least these files:
- fimfiction_stories_downloader.py,
- python libraries installer.bat,
- script starter.bat,
2. There are a few ways to run this program:
- If you are missing the python libraries or if you are not sure if you have them, open the 'python libraries installer.bat'. Otherwise skip this step. Then open the 'script starter.bat' to launch the script.
- Go to the folder with this program. Then press Shift + right click mouse button anywhere in the folder window and select the 'Open command window here' option from the context menu. Then enter 'python fimfiction_stories_downloader.py' and click enter.
- Open the 'command line' and go to the directory with the program files using the 'cd' command. Then enter 'python fimfiction_stories_downloader.py' to launch the script.
3. Answer a few simple questions to indicate what you want to download. The program uses the card view to count the number of stories and pages (except for search results, popular stories etc.) so you have to keep that in mind when you paste links into it.
4. Stories will be saved to the folder 'downloaded stories' that will be automatically created in the same folder where you put the program.
