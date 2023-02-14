__author__ = 'Administrator'
import logging
import re


class IdentifySQL:
    def __init__(self):
        i = 0

    def identify_sql_(self, stmt):
        pattern = re.compile('^(select|insert|with|update|delete).*')
        sql_type = []
        stmt = stmt.strip()
        stmt_match = pattern.match(stmt)  # obj or null
        if stmt_match:
            sql_type = [stmt, stmt_match.group(1)]
        return sql_type







