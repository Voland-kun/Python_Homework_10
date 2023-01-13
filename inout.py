from fractions import Fraction
import sys

def get_number(user_number):
    try:
        user_number = Fraction(user_number)
        return user_number

    except ValueError:
        try: 
            isinstance(complex(user_number), complex)
            return complex(user_number)
        except ValueError:
            print('Неверные данные, завершение работы')
            sys.exit(0)


def manual_input(text):
    last_name, phone_number, comment = text.split(maxsplit=2)
    res_line = '; '.join([last_name, phone_number, comment])
    return res_line


def output_rows(text):
    temptxt = text.split('\n')
    result = ''
    for i in temptxt:
        res = i.split('; ')
        if res[0] != '':
            res_txt = '\n'.join(res)
            res_txt += '\n'+'\n'
        
            result += res_txt
        fix_result = result
        while fix_result[-1] == '\n':
            fix_result=fix_result[:-1]
    return fix_result
