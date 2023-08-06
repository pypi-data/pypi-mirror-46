# *- coding: utf-8 -*-
"""
text colorisation functions  due to extendet use of the python3 print
function this is for python3 only
"""
from os import name as osname
from sys import stdout, stderr
__echo = stdout.write
__puke = stderr.write

# get color escape sequence from string
if osname == 'nt':
	# color faker function for windows compatibility
	def colortext(_, text): return text
else:
	def colortext(color, text):
		"""colortag prepending and end-tag appending function"""
		if osname == 'nt':
			return text
		string = '\033['
		__c = color
		if len(color) == 4:
			__c = color[1:]
			string = '%s01;'%(string)
		if __c == 'gre':
			string = '%s30m'%(string)
		if __c == 'red':
			string = '%s31m'%(string)
		if __c == 'grn':
			string = '%s32m'%(string)
		if __c == 'yel':
			string = '%s33m'%(string)
		if __c == 'blu':
			string = '%s34m'%(string)
		if __c == 'vio':
			string = '%s35m'%(string)
		if __c == 'cya':
			string = '%s36m'%(string)
		if __c == 'whi':
			string = '%s37m'%(string)
		__coloredtext = '%s%s\033[0m'%(string, text)
		return __coloredtext

# define 2 functions for each color
# one for normal and one for bold text
# blu, bblu, cya, bcya, gre, bgre, grn, bgrn, red, bred, vio, bvio, whi, bwhi, yel, byel
def blu(text):
	"""function for color blue"""
	return colortext('blu', text)
def bblu(text):
	"""function for color boldblue"""
	return colortext('bblu', text)

def cya(text):
	"""function for color cyan"""
	return colortext('cya', text)
def bcya(text):
	"""function for color boldcyan"""
	return colortext('bcya', text)

def gre(text):
	"""function for color grey"""
	return colortext('gre', text)
def bgre(text):
	"""function for color boldgrey"""
	return colortext('bgre', text)

def grn(text):
	"""function for color green"""
	return colortext('grn', text)
def bgrn(text):
	"""function for color boldgreen"""
	return colortext('bgrn', text)

def red(text):
	"""function for color red"""
	return colortext('red', text)
def bred(text):
	"""function for color boldred"""
	return colortext('bred', text)

def vio(text):
	"""function for color violet"""
	return colortext('vio', text)
def bvio(text):
	"""function for color boldviolet"""
	return colortext('bvio', text)

def whi(text):
	"""function for color white"""
	return colortext('whi', text)
def bwhi(text):
	"""function for color boldwhite"""
	return colortext('bwhi', text)

def yel(text):
	"""function for color guess what?  yellow ;)"""
	return colortext('yel', text)
def byel(text):
	"""function for color and you already guessed it... boldyellow"""
	return colortext('byel', text)

# functions for some high frequent use cases:
def abort(*messages):
	"""
	prints all text in blu by using STDOUT but also kills its
	parent processes and returns 0 (OK) instead of 1 (ERROR)
	by default used for aborting on STRG+C (see message,
	for "KeyboardInterrupt" exceptions)
	"""
	if not messages:
		messages = ('\naborted by keystroke', )
	msgs = []
	for msg in messages:
		if (messages.index(msg) % 2) == 0:
			msgs.append(blu(msg))
		else:
			msgs.append(yel(msg))
	__echo('%s\n'%' '.join(msg for msg in msgs))
	exit(1)

def anquest(*args, yesno=True, **kwargs):
	"""
	while i most often want to display error texts which heave
	one or more primary causes i want the text parts printed
	in red and the causes printed in yellow as follows
	"""
	if osname == 'nt':
		return input(' '.join(args))
	if 'sep' in kwargs.keys():
		delim = kwargs['sep']
	prefno = False
	if 'prefno' in kwargs.keys():
		prefno = kwargs['prefno']
	color = 'grn'
	if 'color' in kwargs.keys():
		color = kwargs['color']
	keycolor = 'yel'
	if 'keycolor' in kwargs.keys():
		keycolor = kwargs['keycolor']
	valcolor = 'vio'
	if 'valcolor' in kwargs.keys():
		valcolor = kwargs['valcolor']
	msgs = []
	for arg in args:
		if (args.index(arg) % 2) == 0:
			msgs.append(colortext(color, arg))
		else:
			msgs.append(colortext(keycolor, arg))
	if yesno:
		ynq = '[Y/n]'%colortext(color, '?')
		if prefno:
			ynq = '[y/N]'%colortext(color, '?')
		msgs.append(ynq)
	__echo('%s\n'%str(delim).join(msg for msg in msgs))
	answer = input()
	if yesno:
		if answer.lower() not in ('y', ''):
			return False
		return True
	return answer

def error(*args, **kwargs):
	"""
	while i most often want to display error texts which heave
	one or more primary causes i want the text parts printed
	in red and the causes printed in yellow as follows
	"""
	if osname == 'nt':
		return __puke(' '.join(args))
	delim = ' '
	if 'sep' in kwargs.keys():
		delim = kwargs['sep']
	errfile = ''
	errline = ''
	end = '\n' if not 'end' in kwargs.keys() else kwargs['end']
	buzzword = 'ERROR:'
	if 'file' in kwargs.keys():
		errfile = '%s:'%(kwargs['file'])
	if 'line' in kwargs.keys():
		errline = '%s:'%(kwargs['line'])
	if 'warn' in kwargs.keys():
		buzzword = 'WARNING:'
	elif 'buzzword' in kwargs.keys():
		buzzword = kwargs['buzzword']
	if 'sep' in kwargs.keys():
		delim = kwargs['sep']
	msgs = [errfile+errline+red(buzzword)]
	for arg in args:
		if (args.index(arg) % 2) == 0:
			if not arg:
				continue
			msgs.append(red(arg))
		else:
			msgs.append(yel(arg))
	__puke('%s%s'%(str(delim).join(msg for msg in msgs), end))
	stderr.flush()

def fatal(*args, **kwargs):
	"""
	does exactly the same as "error" except it prints texts
	in bold and kills its parent processes
	"""
	if osname == 'nt':
		return __puke(''.join(args))
	delim = ' '
	if 'sep' in kwargs.keys():
		delim = kwargs['sep']
	errfile = ''
	errline = ''
	end = '\n' if not 'end' in kwargs.keys() else kwargs['end']
	if 'file' in kwargs.keys():
		errfile = '%s:'%(kwargs['file'])
	if 'line' in kwargs.keys():
		errline = '%s: '%(kwargs['line'])
	if 'sep' in kwargs.keys():
		delim = kwargs['sep']
	msgs = ['%s%s%s'%(errfile, errline, bred('FATAL:'))]
	for arg in args:
		if (args.index(arg) % 2) == 0:
			if not arg:
				continue
			msgs.append(bred(arg))
		else:
			msgs.append(yel(arg))
	__puke('%s%s'%(str(delim).join(msg for msg in msgs), end))
	stderr.flush()
	exit(1)

def tabs(dat, ind=0, ll=80):
	"""string indentations on newline"""
	return '\n'.join(
        '%s%s'%(' '*ind, dat[i:int(i+ll)]) for i in range(0, len(dat), ll))

def tabl(dats, ind=0, iind=0):
	"""list to string with indentations"""
	tabbl = ''
	for i in dats:
		if isinstance(i, (tuple, list)):
			tabbl = '%s\n%s'%(tabbl, tabl(
                i, ind+iind if iind else 2, iind if iind else 2))
			continue
		elif isinstance(i, dict):
			tabbl = '%s\n%s'%(tabbl, tabd(i, ind, iind))
			continue
		tabbl = '%s\n%s%s'%(tabbl, ' '*ind, i)
	return tabbl #.lstrip('\n')

def tabd(dats, ind=0, iind=0):
	"""
	this is a function where i try to guess the best indentation for text
	representation of keyvalue paires with best matching indentation
	e.g:
	foo         = bar
	a           = b
	blibablubb  = bla
	^^indent "bar" and "b" as much as needed ("add" is added to each length)
	"""
	try:
		lim = int(max(len(str(k)) for k in dats if k)+int(ind))
	except (ValueError, TypeError):
		return dats
	tabbd = ''
	try:
		for (key, val) in sorted(dats.items()):
			if val and isinstance(val, dict):
				spc = ' '*int(lim-len(str(key))-ind-1)
				tabbd = '%s\n%s%s:\n%s'%(tabbd, ' '*ind, key, tabd(
                    val, ind+int(iind if iind else 2), iind if iind else 2))
			elif val and type(val) in (tuple, set, list):
				spc = ' '*int(lim-len(str(key))-ind+1)
				tabbd = str('%s\n%s%s%s= %s'%(
                    tabbd, ' '*ind, key, spc, val)).strip('\n')
			else:
				spc = ' '*int(lim-len(str(key))-ind+1)
				tabbd = str('%s\n%s%s%s= %s'%(
                    tabbd, ' '*ind, key, spc, val)).strip('\n')
	except AttributeError:
		return tabl(dats, ind)
	return tabbd.strip('\n')
