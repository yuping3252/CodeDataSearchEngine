import logging

from   trg.cmd.cmdprocess  import cmdprocess_

def travel_(cmd, path_, travel_type, glo):
    logging.basicConfig(
        level    =logging.DEBUG,
        format   ='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt  ='%a, %d %b %Y %H:%M:%S',
        filename ='project_system.log',
        filemode ='a'
    )
    travel_result = cmdprocess_(cmd, path_, travel_type, glo)
    return travel_result


if __name__ == "__main__":
    travel_('t', 'D:/tr7/tr103')

