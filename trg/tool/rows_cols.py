__author__ = 'Administrator'


def rows_cols_(cds):
    retrieved = []
    for row_ in cds:
        row = []
        for col_ in row_:
            row.append(col_)
        retrieved.append(row)
    return retrieved




