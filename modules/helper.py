



def replace_all(string, old, new=''):
	for char in old:
		string = string.replace(char, new)
	return string
