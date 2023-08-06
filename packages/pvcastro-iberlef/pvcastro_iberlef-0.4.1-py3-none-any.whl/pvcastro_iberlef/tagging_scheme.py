def convert_tag_scheme(predictions):
    for prediction in predictions:
        tags = []
        for tag in prediction['tags']:
            tags.append(tag)

        iob2(tags)

        for index, tag in enumerate(tags):
            prediction['tags'][index] = tag


def iob2(tags):
    """
    Check that tags have a valid IOB format.
    Tags in IOB1 format are converted to IOB2.
    """
    for i, tag in enumerate(tags):
        if tag == 'O':
            continue
        if '-' not in tag:
            tag = 'I-' + tag
            tags[i] = tag
        split = tag.split('-')
        # if len(split) != 2 or split[0] not in ['I', 'B']:
        #     return False
        if split[0] == 'B':
            continue
        elif i == 0 or tags[i - 1] == 'O':  # conversion IOB1 to IOB2
            tags[i] = 'B' + tag[1:]
        elif tags[i - 1][1:] == tag[1:]:
            if split[0] != 'I':
                tags[i] = 'I' + tag[1:]
            else:
                continue
        else:  # conversion IOB1 to IOB2
            tags[i] = 'B' + tag[1:]
    return True
