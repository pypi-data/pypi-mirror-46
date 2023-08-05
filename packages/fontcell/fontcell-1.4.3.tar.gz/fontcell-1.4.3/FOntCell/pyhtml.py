#
# Document with tools for write a html using python


def html(corpus):
    return '<!DOCTYPE html>' + '<html>' + corpus + '</html>'


def tittle(tittle_string):
    return '<head>' + tittle_string + '</head>'


def body(corpus):
    return '<body>' + corpus + '</body>'


def heading(text, number=None):
    if number is None:
        return '<h>' + text + '</h>'
    else:
        return '<h' + str(number) + '>' + text + '</h' + str(number) + '>'


def paragraph(text, number=None):
    if number is None:
        return '<p>' + text + '</p>'
    else:
        return '<p' + str(number) + '>' + text + '</p' + str(number) + '>'


def htmllist(list_of_strings):
    text = list(map(lambda a: '<li>' + a + '</li>', list_of_strings))
    result = ''.join(text)
    return '<ul>' + result + '</ul>'


def insert_link(link, mask_string):
    return '<a href="' + link + '">' + mask_string + '</a>'


def insert_image(image_name, width=200, height=200, align=None):
    if align is None:
        return '<img src="' + image_name + '" width="' + str(width) + '" height="' + str(height) + '">'
    else:
        return '<img src="' + image_name + '" width="' + str(width) + '" height="' + str(height) + '"align="' \
               + align + '">'

def blankspace():
    return '<br>'


def align(corpus, side):
    return '<div align="' + side + '">' + corpus + '</div>'


def add_box(corpus, type):
    return '<div class ="' + type + '" >' + corpus + '</div>'


def add_style(list_styles, type=None, number=None, style=None):
    if list_styles == '':
        return tittle('<style>' + type + str(number) + '{' + style + '}' + '</style> ')
    else:
        old = list_styles.split('<head><style>')[1]
        new = '<head><style>' + type + str(number) + '{' + style + '}'
        return new + old
