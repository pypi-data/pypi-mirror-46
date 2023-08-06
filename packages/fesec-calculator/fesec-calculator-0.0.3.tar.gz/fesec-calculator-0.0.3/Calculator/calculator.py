import ctypes

def add(n1, n2):
	return n1+n2

def minus(n1, n2):
	return n1-n2

def multiply(n1, n2):
	return n1*n2

def divind(n1, n2):
	return n1/n2

def mod(n1, n2):
	return n1%n2

def pow(n1, n2):
	return n1**n2

def getContact():
	text = 'My name is Fesec, the owner of this package\nIf you have any questions, please contact: aod03562@gmail.com'
	title = 'Message'
	style = 1
	return ctypes.windll.user32.MessageBoxW(0, text, title, style)
