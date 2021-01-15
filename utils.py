import locale
locale.setlocale(locale.LC_NUMERIC, '')

def format_number(number):
    _num = locale.format_string('%d', number, grouping=True)

    return _num
