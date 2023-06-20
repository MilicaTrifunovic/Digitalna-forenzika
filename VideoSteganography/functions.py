def _int_to_bin(rgb):
    """Convert an integer tuple to a binary (string) tuple.
    :param rgb: An integer tuple like (220, 110, 96)
    :return: A string tuple like ("00101010", "11101011", "00010110")
    """
    r, g, b = rgb
    return f'{r:08b}', f'{g:08b}', f'{b:08b}'


def _bin_to_int(rgb):
    """Convert a binary (string) tuple to an integer tuple.
    :param rgb: A string tuple like ("00101010", "11101011", "00010110")
    :return: Return an int tuple like (220, 110, 96)
    """
    r, g, b = rgb
    return int(r, 2), int(g, 2), int(b, 2)


def _merge_rgb(rgb1, rgb2):
    """Merge two RGB tuples.
    :param rgb1: An integer tuple like (220, 110, 96)
    :param rgb2: An integer tuple like (240, 95, 105)
    :return: An integer tuple with the two RGB values merged.
    """
    r1, g1, b1 = _int_to_bin(rgb1)
    r2, g2, b2 = _int_to_bin(rgb2)
    rgb = r1[:4] + r2[:4], g1[:4] + g2[:4], b1[:4] + b2[:4]
    return _bin_to_int(rgb)


def _unmerge_rgb(rgb):
    """Unmerge RGB.
    :param rgb: An integer tuple like (220, 110, 96)
    :return: An integer tuple with the two RGB values merged.
    """
    r, g, b = _int_to_bin(rgb)
    # Extract the last 4 bits (corresponding to the hidden image)
    # Concatenate 4 zero bits because we are working with 8 bit
    new_rgb = r[4:] + '0000', g[4:] + '0000', b[4:] + '0000'
    return _bin_to_int(new_rgb)
