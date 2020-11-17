from bs4 import BeautifulSoup
import requests
import re
import os.path


def main_program():

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
            "Enter the address of a public or unlisted bookshelf or folder. It has to start with 'https://www': ")
        if 'fimfiction.net/story' in website_url:
            print("This program cannot download single stories. You need the website address with a list of stories.")
            main_program()
        return website_url

    def establish_a_session():
        """
        Create a session with cookies
        """
        session = requests.Session()
        jar = requests.cookies.RequestsCookieJar()
        mature_content = input("Do you want to include adult stories?(y/n):").lower()
        if mature_content == 'y' or mature_content == 'yes':
            jar.set('view_mature', 'true')
        else:
            pass
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
            print(
                "Incorrect address. Check it for mistakes.\nRemember that it has to start with 'https://www'. Try again.")
            main_program()
        soup = BeautifulSoup(source, "lxml")
        return soup

    def choose_file_format():
        """
        Choose the format of story
        """
        output = ""
        while True:
            chosen_file_format = input('Choose the file format (enter a number): 1—txt, 2—html, 3—epub: ').lower()
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
                continue
        return output

    def range_of_pages():
        """
        Get the current page and the total number of pages. If there is more than one page, you can choose the range.
        """
        try:
            current_page = int(website_url.split('=', 2)[-1])  # more than 1 page
        except ValueError:
            current_page = 0  # one or first page of many
        if not soup.find(class_='fa fa-chevron-right'):
            end_page = 0  # last page or only 1 page

            # it downloads the current page of stories from the 'popular stories', 'newest stories' etc.
            # it also prevents from downloading thousands of stories at once from the search results by accident
        elif 'fimfiction.net/stories?' in website_url:
            end_page = 0

        else:
            list_of_pages = soup.find(class_='page_list')  # more than one page and not the last page
            last_page = int(list_of_pages.findAll('a', href=True)[-2].text)
            end_page = last_page - current_page
            while True:
                if end_page != 0:
                    users_range_of_pages = input(
                        "What do you want to download? (enter '1' or '2'):\n1-only stories from the current page\n2-stories from all pages starting from the current one")
                    if users_range_of_pages == "1":
                        end_page = 0
                    elif users_range_of_pages == "2":
                        break
                    else:
                        print("You entered something incorrect. Try again!")
                        continue
                else:
                    pass
        return current_page, end_page

    def stories_and_pages_loop():
        """
        Get links to stories from a page and move to the next ones
        """
        start_page = 0
        all_links = []
        soup = get_the_website_data()
        current_page, end_page = range_of_pages()
        while start_page < end_page + 1:
            counter_of_stories = len(soup.findAll(class_="story_link"))
            start = 0
            beginning = 'https://www.fimfiction.net/story/download/'

            while start < counter_of_stories:
                match = soup.findAll(class_="story_link")[start]
                link = match.attrs["href"]
                identifier = link.split("/")[2]
                all_links.append(beginning + identifier + output)
                start = start + 1

            if end_page == 0:
                break
            start_page += 1
            if current_page == 0:
                current_page = 1

            if "&" in website_url:
                next_page = "=".join(website_url.split("=", 2)[:2]) + "=" + str(current_page + 1)
            else:
                next_page = website_url + '?page=' + str(current_page + 1)
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
            open(download_path, 'wb').write(fetched_file.content)
        print("Your stories have been downloaded. Check the folder 'downloaded_stories' in the folder with this program.")

    while True:
        create_download_folder()
        website_url = get_the_website_address()
        session = establish_a_session()
        soup = get_the_website_data()
        output = choose_file_format()
        save_files()
        main_program()


if __name__ == "__main__":
    main_program()
