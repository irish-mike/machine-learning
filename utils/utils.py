def print_rows(data):
    row_format = " ".join(["{}"] * data.shape[1])
    for row in data:
        print(row_format.format(*row))