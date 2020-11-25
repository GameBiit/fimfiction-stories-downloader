import argparse
from bs4 import BeautifulSoup
import requests
import re
import os
import os.path
import sys
import urllib.parse as urlparse


def main_program():

    format_choices = {
        '/txt': ['1', 'txt', '1-txt'],
        '/html': ['2', 'html', '2-html'],
        '/epub': ['3', 'epub', '3-epub']
    }

    class FfsdError(Exception):
        pass

    def parse_command_line_arguments():
        default_out_dir = 'downloaded_stories'

        cla_parser = argparse.ArgumentParser()
        cla_parser.add_argument('-o', '--out', default=default_out_dir,
                                help='set the directory to which all stories will be downloaded '
                                     f"(default is {default_out_dir})")
        cla_parser.add_argument('-a', '--adult', help='set whether to download mature rated stories (y/n)')
        cla_parser.add_argument('-f', '--format', choices=sum(format_choices.values(), []),
                                help='set the file format for all downloaded stories')
        cla_parser.add_argument('-r', '--range', choices=['1', '2'],
                                help='set whether to download only from the current page (1) '
                                     'or from all pages starting with the current one (2)')
        cla_parser.usage = __file__ + ' [options] [URLs]'
        cla_parser.epilog = "If any numbers of URLs are passed, the program will process them and quit. Otherwise " \
                            "it'll ask the user to input them until an interrupt signal or EOF is encountered." \
                            "If the rating, format or range isn't passed, the user will be asked to specify the " \
                            "missing settings for each URL."
        return cla_parser.parse_known_args()

    def create_download_folder():
        """
        Create a download folder if it does not exist
        """
        try:
            os.mkdir(cla_args[0].out)
        except FileExistsError:
            pass

    def get_the_website_address():
        """
        Get the url from a user and store the url for further use
        """
        if list_link_id == -1:
            url = input(
                "Enter the address of a public or unlisted bookshelf or folder.\nIt has to start with 'https://www': ")
        else:
            url = cla_args[1][list_link_id]
            print('Downloading from:', url)

        if 'fimfiction.net/story' in url:
            raise FfsdError(
                "This program cannot download single stories. You need the website address with a list of stories.")

        parsed = list(urlparse.urlparse(url))
        query = dict(urlparse.parse_qsl(parsed[4]))  # 4 as an equivalent to parsed_url.query
        query['view_mode'] = '2'                     # sometimes the cookie doesn't work, so double tap it
        parsed[4] = urlparse.urlencode(query)
        url = urlparse.urlunparse(parsed)
        return url, parsed, query

    def establish_a_session():
        """
        Create a session with cookies
        """
        new_session = requests.Session()
        jar = requests.cookies.RequestsCookieJar()

        if cla_args[0].adult:
            mature_content = cla_args[0].adult
        else:
            mature_content = input("\nDo you want to include adult stories? (y/n): ")
        if mature_content.lower() in ['y', 'yes', 'on', '1']:
            jar.set('view_mature', 'true')

        jar.set('d_browse_bookshelf', '2')  # grid-like view
        new_session.cookies = jar
        return new_session

    def get_the_website_data():
        """
        Get the source code of a website and check if the address is correct
        """
        try:
            source = session.get(website_url).text
        except requests.exceptions.MissingSchema:
            raise FfsdError("Incorrect address. Check it for mistakes.\n"
                            "Remember that it has to start with 'https://www'. Try again.")
        return BeautifulSoup(source, "lxml")

    def choose_file_format():
        """
        Choose the format of story
        """
        if cla_args[0].format:
            return next(key for key, values in format_choices.items() if cla_args[0].format in values)

        while True:
            try:
                chosen_file_format = input('\nChoose the file format (enter a number): 1-txt, 2-html, 3-epub: ').lower()
                return next(key for key, values in format_choices.items() if chosen_file_format in values)
            except StopIteration:
                print("You entered something incorrect. Try again.")

    def range_of_pages(soup):
        """
        Get the current page and the total number of pages. If there is more than one page, you can choose the range.
        """
        current_page = int(url_query.get('page', '1'))
        if not soup.find(class_='fa fa-chevron-right'):
            end_page = current_page  # last page or only 1 page

            # it downloads the current page of stories from the 'popular stories', 'newest stories' etc.
            # it also prevents from downloading thousands of stories at once from the search results by accident
        elif 'fimfiction.net/stories?' in website_url:
            end_page = current_page

        else:
            list_of_pages = soup.find(class_='page_list')  # more than one page and not the last page
            end_page = int(list_of_pages.findAll('a', href=True)[-2].text)

            if cla_args[0].range == '1':
                end_page = current_page
            elif not cla_args[0].range:
                while end_page != current_page:
                    users_range_of_pages = input("\nWhat do you want to download? (enter '1' or '2'):\n"
                                                 "1-only stories from the current page\n"
                                                 "2-stories from all pages starting from the current one\n")
                    if users_range_of_pages == "1":
                        end_page = current_page
                    elif users_range_of_pages == "2":
                        break
                    else:
                        print("You entered something incorrect. Try again!")
        return current_page, end_page

    def stories_and_pages_loop():
        """
        Get links to stories from a page and move to the next ones
        """
        all_links = []
        soup = get_the_website_data()
        current_page, end_page = range_of_pages(soup)

        while True:
            beginning = 'https://www.fimfiction.net/story/download/'

            for story in soup.findAll(class_=['story_link', 'story_name']):
                link = story.attrs["href"]
                identifier = link.split("/")[2]
                all_links.append(beginning + identifier + output)

            if current_page == end_page:
                break
            current_page += 1

            url_query['page'] = str(current_page)
            parsed_url[4] = urlparse.urlencode(url_query)
            next_page = urlparse.urlunparse(parsed_url)
            next_source = session.get(next_page).text
            soup = BeautifulSoup(next_source, "lxml")
        return all_links

    def get_filename_from_cd(cd):
        """
        Get filename from content-disposition
        """
        if not cd:
            return None
        fetched_name = re.findall('filename=(.+)', cd)
        if len(fetched_name) == 0:
            return None

        filename = fetched_name[0].encode('latin-1').decode('utf-8')
        try:
            return eval(filename.rstrip(';'))
        except SyntaxError:
            return filename

    def check_filepath(path, story_id):
        if os.path.exists(path):
            in_id = path.rfind('.')
            return path[:in_id] + '_' + story_id + path[in_id:] if in_id != -1 else path + '_' + story_id
        return path

    def save_files():
        """
        Save the stories
        """
        translator = {'/': ''}
        if sys.platform in ['win32', 'cygwin']:
            translator.update({'<': '', '>': '', ':': '', '"': '', '\\': '', '|': '', '?': '', '*': ''})

        for story_link in stories_and_pages_loop():
            story_id = story_link.split('/')[-2]
            fetched_file = session.get(story_link, allow_redirects=True)
            filename = get_filename_from_cd(fetched_file.headers.get('content-disposition'))
            if not filename:
                filename = story_id + '.' + story_link.split('/')[-1]  # fallback to 'id.ext'

            stripped_filename = filename.translate(str.maketrans(translator))
            download_path = check_filepath(os.path.join(cla_args[0].out, stripped_filename), story_id)
            with open(download_path, 'wb') as file:
                file.write(fetched_file.content)
        print(f'Your stories have been downloaded to "{os.path.join(os.getcwd(), cla_args[0].out)}".')

    cla_args = parse_command_line_arguments()
    list_link_id = -1 if len(cla_args[1]) == 0 else 0
    while list_link_id < len(cla_args[1]):
        try:
            website_url, parsed_url, url_query = get_the_website_address()
            session = establish_a_session()
            output = choose_file_format()
            create_download_folder()
            save_files()
        except FfsdError as err:
            print(err)
        list_link_id += 1 if list_link_id != -1 else 0


if __name__ == "__main__":
    main_program()
