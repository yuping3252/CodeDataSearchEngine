def special_ch_convert_(content):
    #handle the file content special char.

    invalid_char = ["'",'"','\n','\t','\r']
    for ichr in invalid_char:
        if ichr == '"' or ichr == "'":
            content = content.replace(ichr,'#####')
        elif ichr == '\t' or ichr == '\n' or ichr == '\r':
            content = content.replace(ichr,' ')
        
    return content


def special_ch_rconvert_(content):
    #handle the file content special char back.

    content = content.replace("#####",'"')
    return content