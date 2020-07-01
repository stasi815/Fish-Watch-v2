import re

def remove_line_break():
    string = "Hello, WOrld\nHuzzah"

    edit_string = re.sub('\n', " ", string)
    return edit_string


print(remove_line_break())