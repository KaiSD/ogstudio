#!/usr/bin/python
# -*- coding: utf-8 -*-

from sys import argv, exit, path
from os.path import join
import UnicodeCSV

def Main(fname, tname):
	
	try:
		print 'Loading template'
		template = level = __import__('templates.'+tname, globals(), locals(), [tname], -1)
		print 'OK'
	except:
		print 'Loading template failed'
		exit(0)
	
	# CSV open
	print 'Opening %s' % (fname)
	csvfile = UnicodeCSV.UnicodeReader(open(fname), delimiter=';', quotechar='"')
	sourceHeaders = None
	sourceData = []
		
	for i in csvfile:
		if sourceHeaders is None:
			sourceHeaders = i
		else:
			for k in xrange(0, len(i)):
					try:
						i[k] = int(i[k])
					except:
						try:
							i[k] = float(i[k])
						except:
							i[k] = i[k]
			sourceData.append(i)
	
	def get_by_name(name):
		col = []
		if name in sourceHeaders:
			index = sourceHeaders.index(name)
			for i in sourceData:
				col.append(i[index])
		return col
	
	def replacement(string):
		for i in template.replacement.keys():
			string = string.replace(i, template.replacement[i])
		return string
	
	print 'OK'
	
	#Keywords list creation
	print 'Creating keywords list'
	keywords = []
	multiWords = {}
	numbs = ('1','2','3','4','5','6','7','8','9','0')
	allOut = template.header
	
	for i in sourceHeaders:
		multi = False
		while i[-1] in numbs:
			i = i[:-1]
			multi = True
		if multi:
			if i in multiWords:
				multiWords[i] += 1
			else:
				multiWords[i] = 1
				keywords.append(i)
				print '    ' + i
		else:
			keywords.append(i)
			print '    ' + i
	keywords = tuple(keywords)
	
	if not template.keyField in keywords:
		print 'No key field found in CSV'
		exit(3)
	else:
		print 'OK'
	
	# Text compilation
	print 'Generating text'
	idx=0
	for element in get_by_name(template.keyField):
	    text = template.text
	    for i in keywords:
	        if i in multiWords.keys():
	            mystr = ""
	            oldval = None
	            for j in xrange(1, multiWords[i]+1):
	                val = str(get_by_name(i+str(j))[idx])
	                if not val == oldval and not val == '':
	                    if i in template.parts.keys():
	                        addstr = template.parts[i].replace(unicode(template.marker+'_val_'+template.marker), val)
	                        for k in keywords:
	                            if k in multiWords.keys():
	                                if multiWords[k] >= j:
	                                    if k in template.parts.keys():
	                                        val2s = replacement(str(get_by_name(k+str(j))[idx]))
	                                        val2 = template.parts[k].replace(unicode(template.marker+k+template.marker), val2s)
	                                        addstr = addstr.replace(unicode(template.marker+k+template.marker), val2)
	                                    else:
	                                        val2 = replacement(str(get_by_name(k+str(j))[idx]))
	                                        addstr = addstr.replace(unicode(template.marker+k+template.marker), val2)
	                        mystr += addstr
	                    else:
	                        mystr += str(val) + '\n'
	                        oldval = val
	            if i in template.cutLastSymb:
	                mystr = mystr[:-1]
	            text = text.replace(unicode(template.marker+i+template.marker), mystr)
	        else:
	            mystr = replacement(unicode(get_by_name(i)[idx]))
	            text = text.replace(unicode(template.marker+i+template.marker), mystr)
	    
	    if template.oneFile:
	    	allOut += text
	    else:
		    filename = template.prefix + element + '.' + template.extension
		    print filename 
		    f = open(filename, 'w')
		    f.write(text.encode('utf-8'))
		    f.close()
	    
	    idx += 1
	
	if template.oneFile:
		allOut += template.footer
		filename = template.prefix + fname + '.' + template.extension
		print filename 
		f = open(filename, 'w')
		f.write(allOut.encode('utf-8'))
		f.close()
	
	print 'All done!'

if __name__ == "__main__":
	# Arguments check
	if len(argv) != 3:
	    Main('translate.csv', 'ru')
	    Main('translate.csv', 'de')
	else:
		Main(argv[1], argv[2])