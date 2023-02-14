#!/usr/bin/python

import zipfile


def get_word_xml(docx_filename):
    with open(docx_filename) as f:
        zip = zipfile.ZipFile(f)
        xml_content = zip.read('word/document.xml')
    return xml_content


if __name__=='__main__':
    get_word_xml("pad.docx")