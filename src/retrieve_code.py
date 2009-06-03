#!/usr/bin/env python

"""
A trivial utility to retrieve the Utah Code, Annotated
"""

import httplib
import os
import re
import subprocess
import sys
import tempfile
import zipfile

import wrap_text

title_pattern = re.compile("(\d{2})(.)(\d{2})(.)(\d{4})(\d{2})")
const_pattern = re.compile("00i(\d{2})_(\d{4})00")
def parse_title_name(name):
    """
    Parse out title, chapter and section
    """
    m = title_pattern.match(name)

    if m:
        title, subtitle, chapter, subchapter, section, subsection = m.groups()

        if subtitle != '_':
            title = title + subtitle

        if subchapter != '_':
            chapter = chapter + subchapter

        if subsection != '00':
            section = section + '.' + subsection

        return title, chapter, section

    m = const_pattern.match(name)

    if m:
        article, section = m.groups()
        return "", article, section

    print m
    assert False

def ensure_dir_exists(dirname):
    """
    Make sure dirname exists.
    """
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def extract_title(conn, title_name, code_dir):
    """
    Download one title, unzip it, convert the WordPerfect files to
    wrapped text and write them into title_dir.
    """
    conn.request('GET', '/~code/%s.zip' % (title_name))
    rsp = conn.getresponse()
    assert rsp.status == 200

    zip_file = tempfile.TemporaryFile()
    zip_file.write(rsp.read())

    # Retrieved data should be a zip file.  Process each entry.
    zip_obj = zipfile.ZipFile(zip_file)
    pattern = re.compile('(.*)\.wpd')

    wp_files = [ e for e in zip_obj.infolist() if pattern.match(e.filename) ]
    for entry in wp_files:
        print "Processing", entry.filename

        # Extract entry content into temporary file
        wp_file = tempfile.NamedTemporaryFile()
        wp_file.write(zip_obj.read(entry.filename))
        wp_file.flush()

        # Convert WP data in file to text
        txt_file = tempfile.NamedTemporaryFile()
        ret_code = subprocess.call(['wpd2text', wp_file.name], stdout=txt_file)
        assert ret_code == 0

        # Line-wrap text and write to destination
        out_path = get_out_path(code_dir,
                                pattern.match(entry.filename).group(1))
        wrap_text.wrap_file(txt_file.name, out_path)

        wp_file.close()                 # Temp file also disappears
        txt_file.close()                # Temp file also disappears

    zip_file.close()                    # Temp file also disappears

def get_out_path(code_dir, titlename):
    """
    Construct output path name
    """
    title, chapter, section = parse_title_name(titlename)
    ensure_dir_exists(os.path.join(code_dir, title, chapter))
    return os.path.join(code_dir, title, chapter, section + '.txt')

title_list = [ '03',
               '04',
               '06',
               '07',
               '08',
               '09',
               '10',
               '11',
               '12',
               '13',
               '14',
               '15',
               '16',
               '17',
               '17B',
               '17C',
               '17D',
               '18',
               '19',
               '20A',
               '22',
               '23',
               '24',
               '25',
               '26',
               '26A',
               '29',
               '30',
               '31A',
               '32A',
               '34',
               '34A',
               '35A',
               '36',
               '38',
               '39',
               '40',
               '41',
               '42',
               '43',
               '45',
               '46',
               '47',
               '48',
               '49',
               '50',
               '51',
               '52',
               '53',
               '53A',
               '53B',
               '53C',
               '54',
               '55',
               '56',
               '57',
               '58',
               '59',
               '61',
               '62A',
               '63A',
               '63B',
               '63C',
               '63D',
               '63E',
               '63F',
               '63G',
               '63H',
               '63I',
               '63J',
               '63K',
               '63L',
               '63M',
               '64',
               '65A',
               '67',
               '68',
               '69',
               '70',
               '70A',
               '70C',
               '70D',
               '71',
               '72',
               '73',
               '75',
               '76',
               '77',
               '78A',
               '78B',
               '79',
               ]

def extract_titles(dest_dir):
    """
    Extract all titles of Utah Code
    """
    conn = httplib.HTTPConnection('le.utah.gov')

    extract_title(conn, "const", "constitution")

    for title in title_list:
        extract_title(conn, "TITLE"+title, 'code')

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print "Usage: retrive_code <dest_path>"
        sys.exit(1)

    extract_titles(sys.argv[1])
        
