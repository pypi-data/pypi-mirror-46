import re


def remove_md_titles(line, file):
    line = re.sub(
        r'((#\s)|(##\s)|(###\s)|(####\s)|(#####\s)|(######\s))',
        '',
        line
    )
    return line


def md_table_row_to_array(line):
    line = re.sub(r'(\ \|\ )', '-', line)
    line = re.sub(r'(\|\ )|(\ \|)', '', line)
    line = line.replace("\\n", '')
    line = line.split('-')
    return line


def add_md_checkbox(items):
    items = items.split(';')
    a = ""
    for item in items:
        a += str('- [ ] ' + item + '\n')
    return a


def format_description(description):
    return str('**Issue description:**\n' + description + '\n')


def add_prefix_to_title(title, number, prefix, subid, numerate):
    subid = subid.upper()
    prefix = prefix.upper()
    title = title.capitalize()

    if numerate:
        return str(prefix + subid + str(number) + " " + title)
    return str(prefix + subid + " " + title)


def get_all_lines(file):
    line = file.readline()
    lines = []
    while line:
        lines.append(line)
        line = file.readline()
    return lines
