from Mark2PY import M2P

def H1(text):
    M2P.md_var.join('# {}\n'.format(str(text)))


def H2(text):
    M2P.md_var.join('## {}\n'.format(str(text)))


def H3(text):
    M2P.md_var.join('### {}\n'.format(str(text)))


def bold(text):
    M2P.md_var.join('**{}**\n'.format(str(text)))


def italic(text):
    M2P.md_var.join('*{}*\n'.format(str(text)))


def strikethrough(text):
    M2P.md_var.join('~~{}~~\n'.format(str(text)))


def block_quote(text):
    M2P.md_var.join('> {}\n'.format(str(text)))


def unordered_list(*arg):
    for i in arg:
        M2P.md_var.join('- {}\n'.format(str(arg)))


def ordered_list(*arg):
    for i in arg:
        x = 1
        M2P.md_var.join('{}. {}\n'.format(x, str(i)))
        x += 1


def horizontal_rule():
    M2P.md_var.join('------------')

def link(title=str, href=str):
	M2P.md_var.join("[{}]({})\n".format(title, str))
	
#TODO: other statements
