def import_row(file):
    with open(str(file), 'r') as input_data:
        txt = input_data.read()
    raw_txt = txt.split('\n')
    for i in raw_txt:
        result = '; '.join(raw_txt)
    while result[-1] in '; \n':
            result = result[:-1]
    result = result.replace('; ; ', '\n')
    return result

def add_strings(txt):
    with open ('book.csv', 'a') as output_file:
        output_file.writelines(f'{txt}\n')
