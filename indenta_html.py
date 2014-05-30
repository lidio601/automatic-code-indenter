# coding=UTF-8

from pprint import pprint
import sys, os
from indenta_js import indenta_js

text="""
<body id="page" class="yoopage column-left column-contentright ">

		<div id="absolute">prova
		ciao
			</div>
	
	<div id="page-body" />
		<div class="page-body-2">
			<div class="page-body-3">
				<div class="wrapper">
				</div>
			</div>
		</div>
	</div>
"""

finale="""
<body id="page" class="yoopage column-left column-contentright ">
	<div id="absolute">prova
		ciao</div>
	<div id="page-body" />
	<div class="page-body-2">
		<div class="page-body-3">
			<div class="wrapper">
			</div>
		</div>
	</div>
</div>
"""

text = """
<div class="box-1 deepest">
	
				<h3 class="header"><span class="header-2"><span class="header-3"><span class="title"><span class="color">Top</span> Block </span><span class="subtitle"> Sub Title</span></span></span></h3>
				
		Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Used Module Class Suffix: <em class="box">style-block</em>		
	</div>
"""


text = """
				<div class="panel-container" style="width: 1048px;">
					<div class="panel-container-bl">
						<div class="panel-container-br" style="height: 1048px;">
							
							<div class="panel" style="width: 1048px;">
								<div style="width: 2403px;">
<div class="slide" style="width: 1048px; position: absolute;"><div class="article"><img height="300" src="images/slide_1.jpg" alt="" /></div></div>
<div class="slide" style="width: 1048px; position: absolute;"><div class="article"><img height="300" src="images/slide_2.jpg" alt="" /></div></div>
<div class="slide" style="width: 1048px; position: absolute;"><div class="article"><img height="300" src="images/slide_3.jpg" alt="" /></div></div>
<div class="slide" style="width: 1048px; position: absolute;"><div class="article"><img height="300" src="images/slide_4.jpg" alt="" /></div></div>
<div class="slide" style="width: 1048px; position: absolute;"><div class="article"><img height="300" src="images/slide_5.jpg" alt="" /></div></div>
<div class="slide" style="width: 1048px; position: absolute;"><div class="article"><img height="300" src="images/slide_6.jpg" alt="" /></div></div>
<div class="slide" style="width: 1048px; position: absolute;"><div class="article"><img height="300" src="images/slide_7.jpg" alt="" /></div></div>
<div class="slide" style="width: 1048px; position: absolute;"><div class="article"><img height="300" src="images/slide_8.jpg" alt="" /></div></div>
								</div>
							</div>
						</div>
					</div>
				</div>
"""

text = """
<body id="page" class="yoopage column-left column-contentright ">

		<div id="absolute">
			</div>
	
	<div id="page-body">
		<div class="page-body-2">
			<div class="page-body-3">
				<div class="wrapper">
		
							<script type="text/javascript">
// <!--
window.addEvent('domready', function(){ 
	
	new YOOcarousel('yoo-carousel-1', { transitionEffect: 'crossfade', transitionDuration: 300, rotateAction: 'mouseover', rotateActionDuration: 300, rotateActionEffect: 'crossfade', slideInterval: 10000, autoplay: 'on' }); });
// -->
</script>
										<div id="footer">
		abi
						<a class="anchor" href="#page">bone</a>
													
					</div>
					
					<div class="footer-box-b1">
						<div class="footer-box-b2">
							<div class="footer-box-b3"></div>
						</div>
					</div>
					<!-- footer end -->
							
				</div>
			</div>
		</div>
	</div>

</body>
"""

#text = """YOUR_HTML_TEXT"""

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

def chopTag(s):
	if not s:
		return False, s
	ind = -1
	base_ind = 0
	while ind < 0:
		ind = str(s).find('<',base_ind)
		if ind >= 0:
			if ind+4 >= len(s):
				break
			elif s[ind:ind+4] == '<!--':
				#print s[ind:ind+4]
				base_ind = ind+4
				ind = -1
		else:
			break
	#print ind
	if ind < 0:
		return False, s, None
	ris = str(s)
	chopped = None
	if ind > 0:
		chopped = str(ris[:ind]).strip("\n\r\t\a\b")
	ris = ris[ind:]
	ind = ris.find('>')
	if ind < 0:
		return False, ris, chopped
	tag = ris[:ind+1]
	#print tag
	ris = ris[ind+1:]
	return tag,ris, chopped

def isCloseTag(tag):
	pos = tag.find('<')
	if pos < 0 or pos+1 < len(tag) and tag[pos+1] == '/':
		return True
	return False

def isClosedTag(tag):
	return tag.find("/>") >= 0 or tag.find("</") >= 0

def indenta(text):
	INDENT_CHAR = " "
	DEPTH = 0
	C = '<'
	#print lastChar(text,text.find('>'))
	tags = []
	while True:
		(tag,text,chopped) = chopTag(text)
		#print tag, text
		#print chopped
		if tag and not tag.startswith('</script') and not tag.startswith('</pre') and not tag.startswith('</style'):
			if chopped:
				chopped = chopped.replace("\n","").replace("\t","").replace("\r","")
		if not tag:
			if chopped:
				tags.append(INDENT_CHAR*DEPTH + chopped + "\r\n")
			break
		if len(tags)>0 and isCloseTag(tag) and not isClosedTag(tags[len(tags)-1]):
			DEPTH -= 1
			if tag.startswith('</script'):
				if chopped:	tags[len(tags)-1] += "\r\n"+indenta_js(chopped)+"\r\n"+INDENT_CHAR*DEPTH
			elif tag.startswith('</style'):
				if chopped:	tags[len(tags)-1] += "\r\n"+chopped+"\r\n"+INDENT_CHAR*DEPTH
			else:
				if chopped:	tags[len(tags)-1] += chopped
			if tag: tags[len(tags)-1] += tag
		else:
			if chopped:
				tags.append(INDENT_CHAR*DEPTH + chopped)
			if isCloseTag(tag):
				DEPTH -= 1
			tags.append(INDENT_CHAR*DEPTH + tag)
			#str(DEPTH)+
			if not isClosedTag(tag):
				DEPTH += 1
		if DEPTH < 0:
			DEPTH = 0
	
	#pprint(tags)
	#print text
	#for tag in tags:
	#	print tag, isClosedTag(tag)
	return tags

if __name__ == '__main__':
	if len(sys.argv) == 2 and os.path.exists(sys.argv[1]):
		fp = open(sys.argv[1],'r')
		text = fp.read()
		print text
		fp.close()
	
	tags = indenta(text)
	print "\r\n".join(tags)
