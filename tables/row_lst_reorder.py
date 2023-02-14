import sys



class RowListReOrder:
    def __init__(self):
        i = 1

    def row_lst_reorder(self, row_lst):
        for rows_ in row_lst:
            for row_ in rows_: 
                print("tableview.py,   row_lst_reorder_rows(),   row_lst,   row_=", row_)
            print("")
        print("")

        print("tableview.py,   row_lst_reorder_rows(),   len row_lst=", len(row_lst))
        print("")

        row_order     = []
        row_order_1st = []
        rows_ordered  = []
        grp = 0

        for rows_ in row_lst:
            new_rows  = []

            # ---------------------------- reordering, outer loop
            if grp > 0:

                # print("tableview.py,   row_lst_reorder_rows(),   chain=", chain)

                # ---------------------------- start a new chain
                if not chain == rows_[0][1][len(rows_[0][1])-1]:       # same chain
                    chain     = rows_[0][1][len(rows_[0][1])-1]        # get next chain num
                    row_order = [i for i in row_order_1st]
                    # print("tableview.py,   row_lst_reorder_rows(),   changed chain=", chain)
                    # print("tableview.py,   row_lst_reorder_rows(),   changed row_order=", row_order)

                # ---------------------------- reordering, inner loop
                for order in row_order:
                    # print("tableview.py,   row_lst_reorder_rows(),   order=", order)
                    for row_ in rows_:
                        len_ = len(row_[1])
                        if row_[1][len_-3] == order:
                            # print("tableview.py,   row_lst_reorder_rows(),                     found,  row_=", row_)
                            new_rows.append(row_)
                            break
            if not new_rows == []: 
                rows_ordered.append(new_rows)

            # ---------------------------- next level order
            row_order.clear()
            if grp == 0:
                for row_ in rows_:
                    len_ = len(row_[1])
                    row_order.append(row_[1][len_-2]) 
                    # print("tableview.py,   row_lst_reorder_rows(),   next level row_order,   row_[1][len_-2]=", row_[1][len_-2])
            else:
                for row_ in new_rows:
                    len_ = len(row_[1])
                    row_order.append(row_[1][len_-2]) 
                    # print("tableview.py,   row_lst_reorder_rows(),   next level row_order,   row_[1][len_-2]=", row_[1][len_-2])
            # print("")

            # ---------------------------- preserve the 1st level order
            if grp == 0:
                for row_ in rows_:
                    len_ = len(row_[1])
                    row_order_1st.append(row_[1][len_-3]) 
                chain = rows_[0][1][len(rows_[0][1])-1]                # get next chain num

            grp += 1

        print("")


        rows_ordered.reverse()
        rows_ordered.append(row_lst[0])
        rows_ordered.reverse()
        for rows in rows_ordered:
            r = 0
            for row in rows: 
                row[0] = r
                r += 1

        for rows in rows_ordered:
            for row in rows: 
                print("tableview.py,   row_lst_reorder_rows(),   rows_ordered,   row=", row)
            print("")
        print("")

        print("tableview.py,   row_lst_reorder_rows(),   len rows_ordered=", len(rows_ordered))
        print("")
        return rows_ordered

