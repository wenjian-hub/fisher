
txt = "12253453246786"
part = "5321"


def subTex(text, pattern):
    txt_len = len(text)
    part_len = len(pattern)

    text_index = 0
    part_index = 0

    while text_index < txt_len and part_index < part_len:
        if text[text_index] == pattern[part_index]:
            text_index += 1
            part_index += 1

        else:
            text_index -= part_index - 1
            part_index = 0

    # if part_index == part_len:
    #     return True
    #
    # else:
    #     return False

    return part_index == part_len


print(subTex(txt, part))




