# This script is for reading the xml output from the program SEMAFOR. 
# The view shows the annotated sentenceses include their frames. 

# The script is written in python 3.4.3 and uses for the view html and
# the bootstrap framework

import xml.etree.ElementTree as ET
from collections import namedtuple
from operator import attrgetter

# reading the xml-file from semafor
tree = ET.parse('output.xml')
root = tree.getroot()

outfile = open("output.html", "w") 
print("_________________________________")
print("Parsing Start")

# html structure 
html_str1 = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html>

<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <title>Semafor View</title>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">

    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
    
</head>

<body>
    <div class="container theme-showcase" role="main">
        <div class="jumbotron">
            <h1>Semafor View</h1>
            <p>This view shows a formated output from the xml output by the program SEMAFOR</p>
        </div>

        <div class="container">"""
outfile.write(html_str1)
tag = namedtuple('tag',['text','pos1','pos2']) # namedtuple for the annotations (includes the text and the start and end position)
tags = [] # list for all tags from a frame
counterSentence = 0 # counter for sentenceses

outfile.write('<div class="row">')
outfile.write('<div class="col-sm-12">')
outfile.write('<div class="row">')
outfile.write('<div class="col-sm-8">')
for sentence in root.iter('sentence'):
    text = sentence.find('text').text # text in a sentence

    id = sentence.attrib # get ID from the sentence

    # reading the sentence
    for value in id.values():
        i = int(value)
        if counterSentence == i:
            print('Satz',counterSentence,': ',text)  # print the sentence into console
            # print html structure in output

            outfile.write('<div class="panel panel-info">')
            outfile.write('<div class="panel-heading"><b>Sentence:</b> '+text+'</div>') # print sentence in html doc

            # reading the annotationsets
            for annotationSet in sentence.iter('annotationSet'):
                frameName = annotationSet.get('frameName') 
                outfile.write('<div class="panel-body"><b>Frame:</b> '+frameName+'</div>') # print frame name in html doc

                layers = annotationSet.find('layers')

                for layer in layers.findall('layer'):
                    name = layer.get('name')
                    labels = layer.find('labels')

                    for label in labels.findall('label'): 
                        labelname = label.get('name') # name of label of annotation for frame 
                        labelid = label.get('ID')   # id of label
                        start = int(label.get('start')) # start position of label
                        end = int(label.get('end')) # end position of label

                        # discrimination of labeltypes (Lexical Units or Targets and Frame Elements)
                        if labelname == 'Target':
                            target_start = start
                            target_end = end
                            # append lexical units in tag list
                            tags.append(tag(text='<span class="label label-info">'+text[start:end+1]+'</span>', pos1=start, pos2=end+1))
                        else:
                            if (target_start == start) or (target_end == end):
                                ignore = 1 
                            else:
                                # append frame elements in tag list
                                tags.append(tag(text='<span class="label label-warning">'+text[start:end+1]+'</span>', pos1=start, pos2=end+1))

                tags = sorted(tags, key=attrgetter('pos1'), reverse=True) # sorting the labels in the tag list for one frame name
                new_text = text
                outfile.write('<div class="panel-footer">')
                
                # print the sentence and annotations in one line
                for x in tags:
                    new_text = new_text[:x[1]] + x[0] + new_text[x[2]:]
                outfile.write('<p>'+new_text+'</p>') # print output in html doc

                outfile.write('</div>')
                
                tags = []
    outfile.write('</div>') # end_tag: <div class="panel panel-info">

    counterSentence = counterSentence + 1
outfile.write('</div>') # end_tag: <div class="col-sm-8">
outfile.write('<div class="col-sm-4">')
html_note = ("""<p>
        <b>Note for view:</b></b> <br/> <br/>
        <span class="label label-info">Lexical units</span> of sentenceses. <br/>
        <span class="label label-warning">Frame elements</span> of sentenceses. <br/><br/><br/>
		
		<b>Usefule Links:</b>
			<ul>
				<li><a href="http://www.cs.cmu.edu/~ark/SEMAFOR/">
				http://www.cs.cmu.edu/~ark/SEMAFOR/</a></li>
				<li><a href="https://github.com/Noahs-ARK/semafor-semantic-parser">
				https://github.com/Noahs-ARK/semafor-semantic-parser</a></li>
				<li><a href="https://github.com/kenoboss/Semafor_Output_Viewer">
				https://github.com/kenoboss/Semafor_Output_Viewer</a></li>
				<li><a href="https://framenet.icsi.berkeley.edu/fndrupal/">
				https://framenet.icsi.berkeley.edu/fndrupal/</a></li>
			</ul>
        </p>""")
outfile.write(html_note)
outfile.write('</div>') # end_tag: <div class="col-sm-8">
outfile.write('</div>') # end_tag: <div class="row"> 
outfile.write('</div>') # end_tag: <div class="col-sm-12">
outfile.write('</div>') # end_tag: <div class="row">
            
html_str2 = ("""
            </div> <!-- end_tag <div class="container"> -->
        </div> <!-- end_tag <div class="container theme-showcase" role="main"> -->
    </body>
</html>""")              
outfile.write(html_str2)
outfile.close()

print("Parsing End")
print("_________________________________")


