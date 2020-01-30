def get_max(num_one, num_two):
    return num_one if num_one > num_two else num_two


def get_min(num_one, num_two):
    return num_one if num_one < num_two else num_two


def extract_values(line_values_str):
    arr_line_values = line_values_str.split()
    first_value = int(arr_line_values[0])
    second_value = int(arr_line_values[1])
    return first_value, second_value


def check_line_overlap(first_line, second_line):
    first_line_max = get_max(first_line[0], first_line[1])
    second_line_min = get_min(second_line[0], second_line[1])
    return second_line_min < first_line_max


if __name__ == "__main__":
    first_line = input(
        "Enter x1 and x2 values of first line separated by space: ")
    second_line = input(
        "Enter x3 and x4 values of second line separated by space: ")
    x1, x2 = extract_values(first_line)
    x3, x4 = extract_values(second_line)

    print(check_line_overlap((x1, x2), (x3, x4)))