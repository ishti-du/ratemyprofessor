# write a function that checks for valid PSU email address
import re


def isValidPSUEmail(testStr):
    x = re.search(r'^[a-zA-Z0-9]+@psu.edu${1}', testStr)
    if x:
        return True
    else:
        return False

    # test cases


examples = ['iuh129@psu.edu', 'ishti_abc@yahoo.com', '`', 'ihussain@uta.edu', 'ihussain@psu.edu',
            'ihussain@psu', 'iuh@psu.edu@psu.edu']

for item in examples:
    print(item + ' isValid? = ' + str(isValidPSUEmail(item)))
