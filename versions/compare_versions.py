def compose_output(first_version, second_version, comparism):
    """
    This function construct the human readable string comparism between two versions

    Parameters:
        first_version (string): A string-format app version
        second_version (string): A string-format app version
        comparism (int): A number indicating the relationship between the two versions

    Returns:
        comparism (string): A string showing how first_version compares to second_version
    """
    compare_values = {
        1: 'is greater than',
        0: 'is equal to',
        -1: 'is less than'
    }
    return f'"{first_version}" {compare_values[comparism]} "{second_version}"'


def compare_versions(first_version, second_version):
    """
    This function compare two string-format app versions and returns their comparism

    Parameters:
        first_version (string): A string-format app version
        second_version (string): A string-format app version

    Returns:
        comparism (string): A string showing how first_version compares to second_version
    """
    first_version_num_list = first_version.split('.')
    second_version_num_list = second_version.split('.')

    first_version_subversion_len = len(first_version_num_list)
    second_version_subversion_len = len(second_version_num_list)

    loop_len = first_version_subversion_len if (
        first_version_subversion_len > second_version_subversion_len
    ) else second_version_subversion_len
    state = 0
    for i in range(loop_len):
        try:
            fv_value = int(first_version_num_list[i])
        except ValueError:
            return f'Invalid version supplied: {first_version}'
        except IndexError:
            overflow = ''.join(second_version_num_list[i:])
            if not overflow.isdigit():
                return f'Invalid version supplied: {second_version}'
            elif int(overflow) != 0:
                state = -1
                break
            else:
                break

        try:
            sv_value = int(second_version_num_list[i])
        except ValueError:
            return f'Invalid version supplied: {second_version}'
        except IndexError:
            overflow = ''.join(first_version_num_list[i:])
            if not overflow.isdigit():
                return f'Invalid version supplied: {first_version}'
            elif int(overflow) != 0:
                state = 1
                break
            else:
                break

        if (fv_value != sv_value):
            state = 1 if fv_value > sv_value else -1
            break

    return compose_output(first_version, second_version, state)
