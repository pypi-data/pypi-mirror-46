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

from MD import md_var

# import MU -> not enabled

import Errors

import mistune


def run(mode):

	if mode == "MD" or "md":
		global md_var
		print(mistune.markdown(md_var))

	# elif mode == "MU" or "mu":
	#    global mu_var
	#    print(mu_var)		
	else: 
		raise Errors.ModeError()

__version__ = 0.5
__author__ = 'Amir Mohammad Joshaghani'
__author_email__ = 'amjoshaghani@gmail.com'


def test():
	filename = 'file:///'+os.getcwd()+'/' + 'helloworld.html'
	webbrowser.open_new_tab(filename)

if __name__ == "__main__":
	test()