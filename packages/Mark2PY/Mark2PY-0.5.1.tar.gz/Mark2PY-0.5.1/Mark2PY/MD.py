md_var = ""

def H1(text):

    md_var.join('# {}\n'.format(str(text)))





def H2(text):

    md_var.join('## {}\n'.format(str(text)))





def H3(text):

    md_var.join('### {}\n'.format(str(text)))





def bold(text):

    md_var.join('**{}**\n'.format(str(text)))





def italic(text):

    md_var.join('*{}*\n'.format(str(text)))





def strikethrough(text):

    md_var.join('~~{}~~\n'.format(str(text)))





def block_quote(text):

    md_var.join('> {}\n'.format(str(text)))





def unordered_list(*arg):

    for i in arg:

        md_var.join('- {}\n'.format(str(arg)))





def ordered_list(*arg):

    for i in arg:

        x = 1

        md_var.join('{}. {}\n'.format(x, str(i)))

        x += 1





def horizontal_rule():

    md_var.join('------------')



def link(title=str, href=str):

	md_var.join("[{}]({})\n".format(title, str))

	

#TODO: other statements

