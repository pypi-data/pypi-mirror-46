import Mark2PY
var = Mark2PY.M2P.md_var

def H1(text):
    var.join('# {}\n'.format(str(text)))
    return None


def H2(text):
    var.join('## {}\n'.format(str(text)))
    return None


def H3(text):
    var.join('### {}\n'.format(str(text)))
    return None


def H4(text):
    var.join('#### {}\n'.format(str(text)))
    return None


def H5(text):
    var.join('##### {}\n'.format(str(text)))
    return None


def H6(text):
    var.join('###### {}\n'.format(str(text)))
    return None


def bold(text):
    var.join('**{}**\n'.format(str(text)))
    return None


def italic(text):
    var.join('*{}*\n'.format(str(text)))
    return None


def strikethrough(text):
    var.join('~~{}~~\n'.format(str(text)))
    return None


def block_quote(text):
    var.join('> {}\n'.format(str(text)))
    return None


def unordered_list(*arg):
    for i in arg:
        var.join('- {}\n'.format(str(arg)))
        return None


def ordered_list(*arg):
    for i in arg:
        x = 1
        var.join('{}. {}\n'.format(x, str(i)))
        x += 1
        return None


def horizontal_rule():
    var.join('------------')
    return None

def link():
    pass
    # TODO: link

#TODO: other statements
