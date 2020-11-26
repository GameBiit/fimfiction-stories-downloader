from bs4 import BeautifulSoup
import requests
import re
import os.path
import sys
import urllib.parse as urlparse


def main_program():

    class FfsdError(Exception):
        pass

    def create_download_folder():
        """
        Create a download folder if it does not exist
        """
        try:
            os.mkdir('downloaded_stories')
        except FileExistsError:
            pass

    def get_the_website_address():
        """
        Get the url from a user and store the url for further use
        """
        website_url = input(
            "Enter the address of a public or unlisted bookshelf or folder.\nIt has to start with 'https://www': ")
        if 'fimfiction.net/story' in website_url:
            raise FfsdError("This program cannot download single stories. You need the website address with a list of stories.")

        parsed_url = list(urlparse.urlparse(website_url))
        url_query = dict(urlparse.parse_qsl(parsed_url[4]))  # 4 as an equivalent to parsed_url.query
        url_query['view_mode'] = '2'                         # sometimes the cookie doesn't work, so double tap it
        parsed_url[4] = urlparse.urlencode(url_query)
        website_url = urlparse.urlunparse(parsed_url)
        return website_url, parsed_url, url_query

    def establish_a_session():
        """
        Create a session with cookies
        """
        session = requests.Session()
        jar = requests.cookies.RequestsCookieJar()
        mature_content = input("\nDo you want to include adult stories?(y/n): ").lower()
        if mature_content == 'y' or mature_content == 'yes':
            jar.set('view_mature', 'true')
        jar.set('d_browse_bookshelf', '2')  # grid-like view
        session.cookies = jar
        return session

    def get_the_website_data():
        """
        Get the source code of a website and check if the address is correct
        """
        source = ""
        try:
            source = session.get(website_url).text
        except requests.exceptions.MissingSchema:
            raise FfsdError(
                "Incorrect address. Check it for mistakes.\nRemember that it has to start with 'https://www'. Try again.")
        soup = BeautifulSoup(source, "lxml")
        return soup

    def choose_file_format():
        """
        Choose the format of story
        """
        output = ""
        while True:
            chosen_file_format = input('\nChoose the file format (enter a number): 1-txt, 2-html, 3-epub: ').lower()
            if chosen_file_format == '1' or chosen_file_format == 'txt' or chosen_file_format == '1-txt':
                output = '/txt'
                break
            elif chosen_file_format == '2' or chosen_file_format == 'html' or chosen_file_format == '2-html':
                output = '/html'
                break
            elif chosen_file_format == '3' or chosen_file_format == 'epub' or chosen_file_format == '3-epub':
                output = '/epub'
                break
            else:
                print("You entered something incorrect. Try again.")
        return output

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
            while end_page != current_page:
                users_range_of_pages = input(
                    "\nWhat do you want to download? (enter '1' or '2'):\n1-only stories from the current page\n2-stories from all pages starting from the current one\n")
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
        return fetched_name[0]

    def save_files():
        """
        Save the stories
        """
        all_links = stories_and_pages_loop()
        for item in all_links:
            fetched_file = session.get(item, allow_redirects=True)
            filename = get_filename_from_cd(fetched_file.headers.get('content-disposition'))
            translator = {'!': '', '?': '', ':': '', '': '', 'ã': '', '/': '', '<': '', '>': '', '\\': '', '"': '',
                          '|': '', '*': ''}
            if output == '/txt' or output == '/html':
                stripped_filename = filename[1:-1].translate(str.maketrans(translator))
            else:
                stripped_filename = filename[1:-2].translate(str.maketrans(translator))
            download_path = 'downloaded_stories/' + stripped_filename

            with open(download_path, 'wb') as file:
                file.write(fetched_file.content)
        print("Your stories have been downloaded. Check the folder 'downloaded_stories' in the folder with this program.\n")

    while True:
        try:
            website_url, parsed_url, url_query = get_the_website_address()
            session = establish_a_session()
            create_download_folder()
            output = choose_file_format()
            save_files()
        except FfsdError as err:
            print(err)

if __name__ == "__main__":
    main_program()
