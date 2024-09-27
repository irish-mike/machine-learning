def print_rows(data):
    row_format = " ".join(["{}"] * data.shape[1])
    for row in data:
        print(row_format.format(*row))

def denormalize(normalized_value, max_value):
    return normalized_value * max_value

def normalize(value, max_value):
    return value / max_value