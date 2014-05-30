text = """
/*
	--------------------------------
	Infinite Scroll
	--------------------------------
	+ https://github.com/paulirish/infinitescroll
	+ version 2.0b2.110713
	+ Copyright 2011 Paul Irish & Luke Shumard
	+ Licensed under the MIT license
	
	+ Documentation: http://infinite-scroll.com/
	
*/(function (window, $, undefined) {
a=23;}"""

INDENT_CHAR = " "
DEPTH = 0
C = '<'

def between(a,b,c):
	return a >= b and b <= c

def lastChar(s,pos):
	for ind in range(1,pos):
		c = s[pos-ind]
		#print c
		#if between(ord('a'),ord(c.lower()),ord('z')) or between(ord('0'),ord(c.lower()),ord('9')):
		if not c in ("\n","\t","\r","\a","\b"," "):
			return c
	return None

"""
def indenta_js(text):
	text = text.strip("\r\n\t").split("\n")
	indent = 0
	output = []
	in_comment = False
	for i in range(len(text)):
		row = text[i].strip("\n\r\t\b")
		if not row:
			continue
		
		if in_comment:
			if "*/" in row:
				in_comment = False
				row = row.replace("*/","*/\n")
			else:
				row = " "+row
		elif row.startswith('/*') or row.startswith('//'):
			if row.startswith('/*'):
				in_comment = True
			row = "\t"*indent + row
		if "{" in row:
			indent = indent + 1
			if not row.endswith("{"):
				row = row.replace("{","{\n"+"\t"*indent)
		elif "}" in row:
			indent = indent - 1
			if indent < 0:
				indent = 0
			row = row.replace("}","\n}")
			if not row.endswith("}"):
				row = row.replace("}","}\n"+"\t"*indent)
		row = "\t"*indent + row
		output.append(row)
	
	return ("\n".join(output)).replace("\n\n","\n")
"""

def indenta_js(text):
	indent = 0
	output = []
	in_comment = False
	in_string  = False
	row_started= False
	row = ""
	prec = ''
	next = ''
	c = False
	while len(text):
		
		if c and not c in ("\r","\t","\n","\b"," "):
			prec = c
		
		c = text[0]
		text = text[1:]
		
		i = 0
		next = ''
		while i+1 < len(text) and next in ("","\r","\t","\n","\b"," "):
			next = text[i]
			i += 1
		
		if not row_started and c in ('\n','\r','\t','\b',' '):
				continue
		else:
			row_started = True
		
		if row_started:
			if not in_comment and not in_string and c in ';':
				row += c
				output.append( "\t" * indent + row )
				row = ""
				row_started = False
			elif not in_comment and not in_string and ( c+next == "//" or c+next == "/*" ):
				row += c
				in_comment = True
			elif in_comment and ( c == "\n" or c == "\r" or c+next == "*/" ):
				if not c == "\n":
					row += c
				in_comment = False
				output.append( "\t" * indent + row )
				row = ""
				row_started = False
			elif not in_comment and not in_string and prec+c != "\'" and prec+c != '\"' and c in ("'",'"'):
				in_string = c
				row += c
			elif in_string and prec+next != "\'" and prec+next != '\"' and c == in_string:
				row += c
				in_string = False
			elif not in_comment and not in_string and c == "{":
				if prec+c == "){":
					row += " "
				row += c
				output.append( "\t" * indent + row )
				indent += 1
				row = ""
				row_started = False
			elif not in_comment and not in_string and c == "}" and not next in (",",")"):
				row += c
				output.append( "\t" * indent + row )
				indent -= 1
				row = ""
				row_started = False
			elif not in_comment and not in_string and c == "}":
				output.append( "\t" * indent + row )
				indent -= 1
				row = c
				row_started = False
			elif not in_comment and not in_string and c == ",":
				row += c
				if next != "{":
					output.append( "\t" * indent + row )
					row = ""
					row_started = False
			elif not in_string and not in_comment and not c in ("\r","\t","\n","\b"," "):
				row += c
			else:
				row += c
	if row:
		output.append("\t" * indent + row)
	return ("\r\n".join(output))

if __name__ == '__main__':
	if len(sys.argv) == 2 and os.path.exists(sys.argv[1]):
		fp = open(sys.argv[1],'r')
		text = fp.read()
		print text
		fp.close()
	
	tags = indenta_js(text)
	print "\r\n".join(tags)
