from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
import time
import json


def parse_professor(university_name, department, professor_overall, webdriver):
    """
    :param university_name: professor's university name
    :param professor_overall: is a list of overall summary, e.g., ['1.6', 'Quick, Susan', '277 RATINGS']
    :param webdriver: handle to the driver/webpage of a professor's RateMyProfessor.com page
    :return: output should be a list with [University Name, Dept., Professor Name, Overall Ratings,
    Num. of ratings, latest_comment_date, oldest_comment_date, Courses List, Tag Count, comments]
    """

    print('Processing Professor ' + professor_overall[1] + ' of ' + university_name + ' ... ...')

    with open(LOG_FILE, 'a') as fObj:
        fObj.write('Processing Professor ' + professor_overall[1] + ' of ' + university_name + ' ... ...\n')

    try:

        output = []
        set_courses = set()
        tag_dictionary = {}

        output.append(university_name)
        output.append(department)
        output.append(professor_overall[1])  # Prof. name
        output.append(float(professor_overall[0]))  # Avg. rating
        output.append(int(professor_overall[2].split()[0]))  # Num. of ratings

        # Now let's handle other items from the webpage

        # load only good ratings, scroll down
        ratings_textbox = driver.find_element_by_id('sratingCommentForm')
        driver.execute_script("arguments[0].scrollIntoView();", ratings_textbox)

        # Click Ratings dropdown and select good
        ratings_dropdown = driver.find_element_by_class_name('sort-type')
        ratings_dropdown.click()
        driver.find_element_by_xpath(
            '/html/body/div[3]/div[4]/div/div[1]/div[7]/div[1]/table/tbody/tr[1]/th[1]/div/div/div[2]/span[2]').click()

        time.sleep(2)

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

        latest_date = None
        oldest_date = None

        all_comments = []

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
            driver.execute_script("arguments[0].scrollIntoView();", comment_row)
            text = comment_row.text

            # Comments always starts with a date in MM/DD/YYYY format, check for '/' in index 2, if not skip
            if len(text) < 3 or not comment_row.text[2] == '/':
                continue

            parsed_text = text.split('\n')

            # Collect the latest date and oldest date
            comment_date = parsed_text[0]
            if flag_first_comment:
                latest_date = parsed_text[0]
                flag_first_comment = False
            else:
                oldest_date = parsed_text[0]

            # keep collecting the unique courses
            set_courses.add(parsed_text[6])

            # Get the tags
            if len(parsed_text) > 15:
                for tag in parsed_text[12: -3]:
                    tag_dictionary.setdefault(tag, 0)
                    tag_dictionary[tag] = tag_dictionary[tag] + 1

            # add comments to all_comments list
            all_comments.append(parsed_text[-3])

        # End of for loop, we are ready with all the data to populate output

        output.append(latest_date)
        output.append(oldest_date)
        output.append(sorted(list(set_courses)))

        tag_list = []
        for k, v in tag_dictionary.items():
            tag_list.append(k + ' (' + str(v) + ')')

        output.append(sorted(tag_list))
        output.append(all_comments)

        return output

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


def search_for_unversity_name(university, driver):
    """
    Searches for the provided University name
    :param university: target university name
    :param driver: webdriver
    :return: None
    """
    find_a_school_button = driver.find_element_by_id('findSchoolOption')
    find_a_school_button.click()
    wait.until(lambda driver: driver.find_element_by_id("schoolName"))
    elem = driver.find_element_by_id("schoolName")
    elem.send_keys(university)
    elem.send_keys(Keys.RETURN)


def find_and_click_university_name_from_search_result(university, driver):
    """
    From the search result, finds the university name and clicks it
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
        # example row: 'SCHOOL\nPennsylvania State University\nUNIVERSITY PARK, PA, UNITED STATES'
        row_text = row.text

        # ignore empty strings and strings without any newline character
        if row_text == "" or '\n' not in row_text:
            continue

        university_name = row_text.split('\n')[1]

        # get rid of '-'s, white spaces. Make one word, all lower case letters
        university_name = str(''.join(university_name.lower().replace('-', '').split()))
        university = str(''.join(university.lower().replace('-', '').split()))

        if university.lower() == university_name.lower():
            target = row
            break

    if target is None:
        with open(LOG_FILE, 'a') as fObj:
            fObj.write('University "' + university + '" could not be found!\n')

    school_link = target.find_element_by_tag_name('a')
    school_link.click()


def select_department_from_school_navigation_side_bar(subject, driver):
    """
    From left navigation bar, types department name to load faculties
    :param subject: department or study subject
    :param driver: webdriver
    :return:
    """
    nav_toggle = driver.find_element_by_id("navToggle")
    school = nav_toggle.find_element_by_id('schoolNav')
    school.click()

    department = driver.find_element_by_class_name("combobox")
    department.send_keys(subject)
    department.send_keys(Keys.RETURN)


def load_all_professors_with_minimum_number_of_ratings(num_of_ratings, driver):
    """
    Load all the professors with minimum number of ratings
    :param num_of_ratings: professors with less than this number of ratings will be ignored.
    :param driver: webdriver
    :return:
    """
    # Load all Computer Science Professors
    while True:
        side_panel = driver.find_element_by_class_name('left-panel')
        result_list = side_panel.find_element_by_class_name('result-list')
        wait.until(lambda result_list: result_list.find_element_by_class_name("progressbtnwrap"))
        load_btn = driver.find_element_by_class_name("progressbtnwrap")

        # scroll down to the load more button
        driver.execute_script("arguments[0].scrollIntoView();", load_btn)

        if len(load_btn.text) > 0:
            # if less than NUM_RATINGS, don't load anymore
            get_professors_so_far = result_list.find_elements_by_tag_name('a')
            last_prof_in_the_list = get_professors_so_far[-1]
            items = last_prof_in_the_list.text.split('\n')
            ratings = items[2].split()  # '174 RATINGS'
            num_ratings = ratings[0]
            if int(num_ratings) < num_of_ratings:
                break
            else:
                load_btn.click()
        else:
            break


def inspect_professors_with_minimum_average_rating(target_num_of_ratings, target_avg_rating, driver):
    """
    Opens professors in a new tab who has minimum num of ratings and average rating score
    :param target_num_of_ratings: number of student ratings
    :param target_avg_rating: overall average minimum rating
    :param driver: webdriver
    :return:
    """

    side_panel = driver.find_element_by_class_name('left-panel')
    result_list = side_panel.find_element_by_class_name('result-list')
    wait.until(lambda result_list: result_list.find_elements_by_tag_name('a'))
    all_prof_links = result_list.find_elements_by_tag_name('a')

    main_window = driver.current_window_handle
    for professor in all_prof_links:
        prof_summary = professor.text.split('\n')  # '1.6\nQuick, Susan\n277 RATINGS'
        received_avg_rating = prof_summary[0]
        received_num_of_ratings = (prof_summary[2].split())[0]

        # ignore N/A ratings
        if received_avg_rating.strip().lower() == 'n/a':
            continue

        if float(received_avg_rating) >= target_avg_rating and int(received_num_of_ratings) >= target_num_of_ratings:

            professor.send_keys(Keys.COMMAND + Keys.RETURN)
            driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + Keys.TAB)
            time.sleep(5)
            # Put focus on current window which will, in fact, put focus on the current visible tab
            driver.switch_to.window(driver.window_handles[1])

            #
            summary = parse_professor(UNIVERSITY, DEPARTMENT, prof_summary, driver)

            # add only valid summary
            if summary:
                popular_professors_json.append(summary)
                # print(summary)

            # Close current tab
            driver.close()

            # Put focus on current window which will be the window opener
            driver.switch_to.window(main_window)

    with open(LOG_FILE, 'a') as fObj:
        fObj.write('Total number of professors processed = ' + str(len(popular_professors_json)) + '\n')

    # print(popular_professors_json)


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
                temp = ", ".join(item)
                single_best_professor_plain.append(str(temp))
            else:
                single_best_professor_plain.append(str(item))
        popular_professors_plain_text.append('\t'.join(single_best_professor_plain))

    with open(filename, 'w') as fObj:
        fObj.write('\n'.join(popular_professors_plain_text))


"""Global variables"""
# University names should not have any '-'s in them


# Top Global and Graduate Universities for Computer Science in the US and Canada
# https://www.usnews.com/education/best-global-universities/search?region=&country=united-states&subject=computer-science&name=
'''
UNIVERSITY_NAMES = ['Massachusetts Institute of Technology',
                    'Stanford University',
                    'Carnegie Mellon University',
                    'University of California Berkeley',
                    'Harvard University',
                    'Georgia Institute of Technology',                    
                    'California Institute of Technology',
                    'University of California Los Angeles (UCLA)',
                    'University of Washington',
                    'University of Texas at Austin',
                    'University of Southern California',
                    'University of California San Diego'
                    'University of Waterloo',
                    'University of British Columbia',
                    'University of Toronto',
                    'University of Alberta',
                    'McGill University',
                    'University of Montreal',
                    'Carleton University',
                    'University of Ottawa',
                    'Simon Fraser University',
                    'Concordia University']
'''

'''
# Top Global Universities for English in the US and Canada
#https://www.usnews.com/education/best-global-universities/search?region=&country=canada&subject=arts-and-humanities&name=
UNIVERSITY_NAMES = ['University of California Berkeley',                    
                    'Columbia University',
                    'Stanford University',                    
                    'University of California Los Angeles (UCLA)',                                     
                    'Harvard University',
                    'Yale University',
                    'New York University',
                    'University of Michigan',
                    'Massachusetts Institute of Technology',                    
                    'Princeton University',
                    'University of Toronto',
                    'McGill University',
                    'University of British Columbia',
                    'University of Alberta',
                    'York University (all campuses)',
                    'Concordia University',
                    'Western University',
                    'University of Ottawa',
                    'University of Calgary',
                    'Universite de Montreal']
'''

UNIVERSITY_NAMES = ['University of Michigan']

TARGET_NUM_RATINGS = 10
AVERAGE_RATING = 3.5
DEPARTMENT = 'English'
JSON_FILE_NAME = 'english_michigan.json'
PLAIN_TEXT_FILE_NAME = 'english_michigan.txt'
popular_professors_json = []
popular_professors_plain_text = []

LOG_FILE = 'rmp.log'

with open(LOG_FILE, 'w') as fObj:
    fObj.write('Starting experiment for ' + DEPARTMENT + ' ... ...\n')

for UNIVERSITY in UNIVERSITY_NAMES:

    try:
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get("https://www.ratemyprofessors.com/")
        wait = ui.WebDriverWait(driver, 10)

        time.sleep(5)
        with open(LOG_FILE, 'a') as fObj:
            fObj.write(
                'Waiting 5 seconds for web page to load ...\nStarting experiment for ' + DEPARTMENT + ' of ' + UNIVERSITY + ' ... ...\n')

        remove_cookie_alert(driver)
        search_for_unversity_name(UNIVERSITY, driver)
        find_and_click_university_name_from_search_result(UNIVERSITY, driver)
        select_department_from_school_navigation_side_bar(DEPARTMENT, driver)
        load_all_professors_with_minimum_number_of_ratings(TARGET_NUM_RATINGS, driver)
        inspect_professors_with_minimum_average_rating(TARGET_NUM_RATINGS, AVERAGE_RATING, driver)

    except:
        with open(LOG_FILE, 'a') as fObj:
            fObj.write('Some error occurred, please check log for ' + DEPARTMENT + ' of ' + UNIVERSITY + ' ... ...\n')
        pass

    finally:
        driver.close()

with open(LOG_FILE, 'a') as fObj:
    fObj.write('Finalizing the result, writing to the json and txt files ... \n')

save_result_as_json(JSON_FILE_NAME)
save_result_as_plain_text(PLAIN_TEXT_FILE_NAME)
