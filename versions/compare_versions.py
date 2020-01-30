def compose_output(first_version, second_version, comparism):
    compare_values = {
        1: 'is greater than',
        0: 'is equal to',
        -1: 'is less than'
    }
    return f'"{first_version}" {compare_values[comparism]} "{second_version}"'


def compare_versions(first_version, second_version):
    first_version_num_list = first_version.split('.')
    second_version_num_list = second_version.split('.')

    first_version_subversion_len = len(first_version_num_list)
    second_version_subversion_len = len(second_version_num_list)

    loop_len = first_version_subversion_len if first_version_subversion_len > second_version_subversion_len else second_version_subversion_len
    state = 0
    for i in range(loop_len):
        try:
            fv_value = int(first_version_num_list[i])
        except ValueError:
            return f'Invalid version supplied: {first_version}'
        except IndexError:
            if second_version_num_list[i].isdigit():
                state = -1
                break
            else:
                return f'Invalid version supplied: {second_version}'

        try:
            sv_value = int(second_version_num_list[i])
        except ValueError:
            return f'Invalid version supplied: {second_version}'
        except IndexError:
            state = 1
            break

        if (fv_value != sv_value):
            state = 1 if fv_value > sv_value else -1
            break

    return compose_output(first_version, second_version, state)
