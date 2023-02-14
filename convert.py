import argparse
import datetime
import xml.etree.ElementTree as ET

try:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', help='file to be processed', required=True, type=str)
    args = parser.parse_args()
except:
    exit()

tree = ET.parse(args.file)
root = tree.getroot()

# Create the base XML elements
ET.Element('?xml version="1.0" encoding="ISO-8859-1"?')
ET.Element('!DOCTYPE tv SYSTEM "xmltv.dtd"')
tv = ET.Element('tv')

# Loop over 
for programData in root.findall('program_data'):
    for channel in programData.findall('channel'):
        tv_channel = ET.SubElement(tv, 'channel', id=channel.get('id'))
        displayName = ET.SubElement(tv_channel, 'display-name')
        displayName.text = channel.find('program').get('id')[:12]
    for channel in programData.findall('channel'):
        for program in channel.findall('program'):
            start = datetime.datetime.fromtimestamp(int(program.get('start'))).strftime("%Y%m%d%H%M%S") + ' -0600'
            stop = datetime.datetime.fromtimestamp(int(program.get('start')) + int(program.get('duration'))).strftime("%Y%m%d%H%M%S") + ' -0600'
            tv_programme = ET.SubElement(tv, 'programme', start=start, stop=stop, channel=program.get('id')[:11])
            tv_programme_title = ET.SubElement(tv_programme, 'title')
            tv_programme_title.text = program.get('title')
            tv_programme_desc = ET.SubElement(tv_programme, "desc")
            tv_programme_desc.text = program.get('synopsis')


f = open("xmltv.xml", "w")
f.write(ET.tostring(tv, encoding='utf-8', method='xml', xml_declaration=True))
f.close()

assert tv.tag == 'tv'
assert tv.attrib == {}
for child in tv:
    assert child.tag == 'channel' or child.tag == 'programme'