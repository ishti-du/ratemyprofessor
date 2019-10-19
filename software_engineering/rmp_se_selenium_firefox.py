from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import time
import json


def parse_professor(info_on_professor, driver):
    """
    :param university_name: professor's university name
    :param professor_overall: is a list of overall summary, e.g., ['1.6', 'Quick, Susan', '277 RATINGS']
    :param webdriver: handle to the driver/webpage of a professor's RateMyProfessor.com page
    :return: output should be a list with [University Name, Dept., Professor Name, Overall Ratings,
    Num. of ratings, latest_comment_date, oldest_comment_date, Courses List, Tag Count, comments]
    """

    try:

        aggregated_output = []

        output = []
        set_courses = set()
        tag_dictionary = {}

        output.append(info_on_professor[0])
        output.append("Computer Science")  # TODO: remove hard coded department name
        # output.append(info_on_professor[1] + ", " + info_on_professor[2])  # Prof. LastName, FirstName
        output.append(info_on_professor[1])  # Prof. LastName, FirstName
        avg_rating = driver.find_element_by_class_name('grade')
        avg_rating = avg_rating.text
        output.append(float(avg_rating))  # Avg. rating

        number_of_ratings = driver.find_elements_by_xpath('//*[@id="mainContent"]/div[1]/div[5]')
        number_of_ratings = number_of_ratings[0].text
        output.append(int(number_of_ratings.split()[0]))  # Num. of ratings

        # Now let's handle other items from the webpage

        '''
        # load only good ratings, scroll down
        ratings_textbox = driver.find_element_by_id('sratingCommentForm')
        driver.execute_script("arguments[0].scrollIntoView();", ratings_textbox)

        # Click Ratings dropdown and select good
        ratings_dropdown = driver.find_element_by_class_name('sort-type')
        ratings_dropdown.click()
        driver.find_element_by_xpath(
            '/html/body/div[3]/div[4]/div/div[1]/div[7]/div[1]/table/tbody/tr[1]/th[1]/div/div/div[2]/span[2]').click()
        '''

        # time.sleep(2)

        # First load all comments
        while True:
            table = driver.find_element_by_class_name('tftable')
            all_rows = table.find_elements_by_tag_name('tr')
            driver.execute_script("arguments[0].scrollIntoView();", all_rows[-1])

            try:
                load_more_button = driver.find_element_by_id('loadMore')
            except:
                break

            if len(load_more_button.text) > 0:
                load_more_button.click()
            else:
                break

        # Now that all comments are loaded, start parsing them
        # Some rows can be advertisements, ignore those. Valid comment starts with a date

        """
         Example Row
          0   05/04/2019
          1   GOOD
          2   4.0
          3   OVERALL QUALITY
          4   1.0
          5   LEVEL OF DIFFICULTY
          6   CMPSC131
          7   For Credit:Yes
          8   Attendance: Not Mandatory
          9   Textbook Used: No
          10  Would Take Again: Yes
          11  Grade Received: A
          []  TAGS
          ...
          []  TAGS               
          n-2 Weird class in that we only had maybe two formal lectures by Al, with the rest being through an external site (similar to taking a course through coursera). Assignments could be somewhat arbitrarily graded, but overall very lenient and easy grading and very easy to get an A with potential for 15% final grade increase through extra credit.
          n-1 0 people found this useful 0 people did not find this useful
          n   report this rating
         """
        flag_first_comment = True

        for i, comment_row in enumerate(all_rows):
            single_comment = []
            driver.execute_script("arguments[0].scrollIntoView();", comment_row)
            text = comment_row.text

            # Comments always starts with a date in MM/DD/YYYY format, check for '/' in index 2, if not skip
            if len(text) < 3 or not comment_row.text[2] == '/':
                continue

            parsed_text = text.split('\n')

            single_comment += parsed_text[0: 12]  # date

            tags = ""

            # Get the tags
            if len(parsed_text) > 15:
                tags = "-".join(parsed_text[12: -3])
            single_comment.append(tags)

            # add comments
            single_comment += parsed_text[-3:]

            single_row = output + single_comment
            aggregated_output.append(single_row)

        # End of for loop, we are ready with all the data to populate output

        return aggregated_output

    except:
        with open(LOG_FILE, 'a') as fObj:
            fObj.write('Exception occurred, ignoring this professor...' + '\n')

        return None


def remove_cookie_alert(driver):
    """
    Clicks the close button of the cookie alert if shown
    :param driver: webdriver
    :return: None, fails silently if no alert pop-up is shown
    """
    try:
        wait.until(lambda driver: driver.find_element_by_xpath("/html/body/div[1]/a[1]"))
        close_btn = driver.find_element_by_xpath("/html/body/div[1]/a[1]")
        close_btn.click()
    except:  # Fail silently if no alert was shown
        with open(LOG_FILE, 'a') as fObj:
            fObj.write("Could not close the Cookie pop up.\n")
        pass


def find_and_click_professor_from_target_university(university, driver):
    """
    From the search result, finds the professor with the university name and clicks it
    :param university: target university name
    :param driver: webdriver
    :return: None
    """

    wait.until(lambda driver: driver.find_element_by_id("searchResultsBox"))
    result = driver.find_element_by_id("searchResultsBox")
    listings = result.find_element_by_tag_name('ul')
    rows = listings.find_elements_by_tag_name('li')

    target = None

    for row in rows:
        # example row: 'Professor\nMehran, Shahmi\nStanford University'
        row_text = row.text

        # ignore empty strings and strings without any newline character
        if row_text == "" or '\n' not in row_text:
            continue

        university_name = row_text.split('\n')[2]

        # get rid of '-'s, white spaces. Make one word, all lower case letters
        university_name = str(''.join(university_name.lower().replace('-', '').split()))
        # example university = massachusettsinstituteoftechnology,computerscience
        # TODO: Verify professor of Computer Science
        university_name = university_name.split(',')[0]
        university = str(''.join(university.lower().replace('-', '').split()))

        # if university.lower() in university_name.lower():
        if university_name.lower().startswith(university.lower()):
            target = row
            break

    if target is None:
        with open(LOG_FILE, 'a') as fObj:
            fObj.write('University "' + university + '" could not be found!\n')
            return False

    # time.sleep(2)

    school_link = target.find_element_by_tag_name('a')
    school_link.click()

    return True


def save_result_as_json(json_file_name):
    """
    Save result as JSON in the provided file
    :param json_file_name: filename to store JSON result
    :return:
    """

    with open(json_file_name, 'w') as fObj:
        json.dump(popular_professors_json, fObj)


def save_result_as_plain_text(filename):
    """
    Flattens nested lists into a single list and saves rows as '\t' delimited file
    :param filename:
    :return:
    """

    for each_best_professor in popular_professors_json:
        single_best_professor_plain = []
        for item in each_best_professor:
            if isinstance(item, list):
                temp = ", ".join([str(x) for x in item])
                single_best_professor_plain.append(str(temp))
            else:
                single_best_professor_plain.append(str(item))
        popular_professors_plain_text.append('\t'.join(single_best_professor_plain))

    with open(filename, 'w') as fObj:
        fObj.write('\n'.join(popular_professors_plain_text))


def search_for_professor(parts, driver):
    wait.until(lambda driver: driver.find_element_by_id("searchr"))
    elem = driver.find_element_by_id("searchr")

    # parts = {University Name, Instructor Name}
    elem.send_keys(parts[1])
    elem.send_keys(Keys.RETURN)


"""Global variables"""
# University names should not have any '-'s in them


UNIVERSITY_NAMES = ['University of Michigan']

TARGET_NUM_RATINGS = 10
AVERAGE_RATING = 3.5
DEPARTMENT = 'English'
JSON_FILE_NAME = 'soft_eng.json'
PLAIN_TEXT_FILE_NAME = 'soft_eng.txt'
popular_professors_json = []
popular_professors_plain_text = []

LOG_FILE = 'rmp.log'

with open(LOG_FILE, 'w') as fObj:
    fObj.write('Starting experiment ... ...\n')

with open('soft_eng_professors.txt') as fileObj:
    lines = fileObj.readlines()

try:
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get("https://www.ratemyprofessors.com/")
    wait = ui.WebDriverWait(driver, 10)

    time.sleep(5)
    # with open(LOG_FILE, 'a') as fObj:
    #    fObj.write('Waiting 5 seconds for web page to load ...\nStarting experiment for ' + DEPARTMENT + ' of ' + UNIVERSITY + ' ... ...\n')

    remove_cookie_alert(driver)

    for line in lines:
        parts = line.split(',')
        parts = [x.strip() for x in parts]

        search_for_professor(parts, driver)

        time.sleep(2)

        wait.until(lambda driver: driver.find_element_by_id("searchResultsBox"))
        result_box = driver.find_element_by_id('searchResultsBox')
        results_count = result_box.find_element_by_class_name('result-count')

        if results_count.text == "Your search didn't return any results.":
            with open(LOG_FILE, 'a') as fObj:
                fObj.write('Could not find: ' + line + ' ... ...\n')
            continue

        found = find_and_click_professor_from_target_university(parts[0], driver)
        if not found:
            with open(LOG_FILE, 'a') as fObj:
                fObj.write('Could not find: ' + line + ' ... ...\n')
            continue

        # if you find course-code, then it implies professor not found
        try:

            if driver.find_element_by_id("course-code"):
                with open(LOG_FILE, 'a') as fObj:
                    fObj.write('Could not find: ' + line + ' ... ...\n')
                continue
        except:
            pass

        summeries = parse_professor(parts, driver)

        # add only valid summary
        if summeries:
            for summary in summeries:
                popular_professors_json.append(summary)
            # print(summary)
        else:
            with open(LOG_FILE, 'a') as fObj:
                fObj.write('Some error occurred or could not find: ' + line + ' ... ...\n')

except:
    with open(LOG_FILE, 'a') as fObj:
        fObj.write('Some error occurred or could not find: ' + line + ' ... ...\n')
        pass

finally:
    driver.close()

with open(LOG_FILE, 'a') as fObj:
    fObj.write('Finalizing the result, writing to the json and txt files ... \n')

save_result_as_json(JSON_FILE_NAME)
save_result_as_plain_text(PLAIN_TEXT_FILE_NAME)
