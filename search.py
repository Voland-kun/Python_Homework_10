def surename_search(surename):
    with open('book.csv', 'r') as data:
        result = ''
        temp_search = data.read()
        temp_list = temp_search.split('\n')
        for line in temp_list:
            li = line.split('; ')
            if li[0].lower() == surename.lower():
                result += '; '.join(li) + '\n'
        if result == '':
            result = 'Совпадений не обнаружено'
    return result

