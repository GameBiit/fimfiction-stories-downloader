# Fimfiction_downloader
It downloads multiple stories from bookshelfs, folders and other lists of stories on fimfiction.net. You can choose one of three file formats that are available on fimfiction.net.

It can download:
- public or unlisted bookshelfs,
- folders with stories in groups,
- stories from the current page of a list of popular, stories, latest stories etc.,
- stories from the current page of a list of search results,
- stories from the homepage.

It cannot download:
- individual stories after you enter links to them,
- story chapters,

# Requirements:
1. Python 3+. You can download it here: https://www.python.org/downloads/. If you have to install it, make sure that you mark 'add Python ... to PATH' and click 'Install Now' to avoid potential problems.
2. The Python libraries below are required to run this program. If you use windows you can run the 'python libraries installer.bat' to download them automatically. You can also install them manually with the command line/prompt/console/terminal:

**pip install requests**

**pip install lxml**

**pip install beautifulsoup4**
  
# How to run it?
1. Download the the whole package or at least these files:
- fimfiction_stories_downloader.py,
- python libraries installer.bat,
- script starter.bat,
2. There are at least two ways you can run this program (Applies only to Windows. If you have linux or a different operating system, check yourself how to run python scripts in your system):
- Open python libraries installer.bat if you are missing the libraries and then open script starter.bat
- Go to the folder with this program. Then press Shift + right click mouse button anywhere in the folder window and Select the “Open command window here” option from the context menu. Then enter 'python fimfiction_stories_downloader.py'.
3. Answer a few simple questions to indicate what you want to download.
