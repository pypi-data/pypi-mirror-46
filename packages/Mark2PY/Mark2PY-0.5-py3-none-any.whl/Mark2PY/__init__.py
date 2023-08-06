# -*- coding: utf-8 -*-

""" this script is created by *AMJoshaghani* for helping web

    developers for using markup and markdown on python script

    :param MD: help you for showing markdown(md) on your script.

    for example:

        Mark2PY.MD.bold('AMJoshaghani')



    :param MU: help you for showing markup(html) on your script.

    for  example:

        Mark2PY.MU.center('AMJoshaghani')



    :copyright : © 2019 by Amir Mohammad Joshaghani --> AMJoshaghani @ https://amjoshaghani.ir

    :license : MIT

"""

import os

import webbrowser

from Mark2PY import M2P

from Mark2PY import MD

from Mark2PY import MU

from Mark2PY import Errors

import mistune


def run(mode=str):

	if mode == "MD" or "md":

		print(mistune.markdown(M2P.md_var))

	elif mode == "MU" or "mu":

		print(M2P.mu_var)

	else:

		raise ModeError

		

__version__ = 0.5
__author__ = 'Amir Mohammad Joshaghani'
__author_email__ = 'amjoshaghani@gmail.com'

if __name__ == "__main__":

	f = open("helloworld.html", "r")

	filename = 'file:///'+os.getcwd()+'/' + 'helloworld.html'

webbrowser.open_new_tab(filename)

