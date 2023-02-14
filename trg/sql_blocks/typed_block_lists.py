__author__ = 'Administrator'

from trg.sql_blocks.typed_nest import TypedNest

class TypedBlocks:
    def __init__(self):
        self.tnst = TypedNest()

    def typed_block_lists_(self,tree, query):
        query_list  = []
        select_list = []
        column_list = []
        from_list   = []
        from_alias_table_list = []
        from_alias_alias_list = []
        from_only_table_list  = []
        join_list   = []
        join_table_list = []
        join_alias_table_list = []
        join_alias_alias_list = []
        join_only_table_list  = []
        where_list = []
        join_on_list = []
        condition_list = []
        topb = self.top_block_(tree, query)
        for b in tree:
            if not self.is_sub_block_(tree, b, topb):
                continue
            if b[5]=="complex query" or b[5]=="query":
                # union or not, is decided in union_blocks.py. For processing convenience,
                # even union is one query, b[6] is still "union"
                # therefore, b[8] is used (not used before) to indicate some "union" is not
                # truly a "union" (if only unioned one query). So, this is a make up action.
                if b[6] == "union" and not b[8]:
                    b[6] = "query"
                query_list.append(b)

            if b[5]=="select":
                select_list.append(b)
            if b[6]=="column":
                column_list.append(b)
            if b[5]=="from":
                from_list.append(b)
            if b[5]=="from table alias" and b[6]=="table":
                from_alias_table_list.append(b)
            if b[5]=="from table alias" and b[6]=="alias":
                from_alias_alias_list.append(b)
            if b[5]=="from table only"  and b[6]=="table":
                from_only_table_list.append(b)
            if b[5]=="join":
                join_list.append(b)
            if b[5]=="join table":
                join_table_list.append(b)
            if b[5]=="join table alias" and b[6]=="table":
                join_alias_table_list.append(b)
            if b[5]=="join table alias" and b[6]=="alias":
                join_alias_alias_list.append(b)
            if b[5]=="join table only"  and b[6]=="table":
                join_only_table_list.append(b)
            if b[5]=="where":
                where_list.append(b)
            if b[5]=="join on":
                join_on_list.append(b)
            if b[5]=="condition":
                condition_list.append(b)
        query_nest_list = self.tnst.typed_nest_(query_list,"query", "complex query", tree)
        return query_list, query_nest_list, select_list, column_list, from_list, from_alias_table_list, \
               from_alias_alias_list, from_only_table_list, join_list, join_table_list, join_alias_table_list,\
               join_alias_alias_list, join_only_table_list, where_list, join_on_list, condition_list

    def top_block_(self, tree, query):
        topb = []
        for b in tree:
            if b[7] == query:
                topb = b
        return topb

    # check whether thisb is a subblock of topb
    def is_sub_block_(self, tree, thisb, topb):
        if thisb == topb:
            return True
        currentb = thisb
        for b in tree:
            for b1 in tree:
                if currentb[1] == b1[0]:
                    currentb = b1
                    if b1 == topb:
                        return True
        return False






