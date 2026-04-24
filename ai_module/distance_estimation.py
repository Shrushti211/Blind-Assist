def estimate_distance(box_width):

    if box_width > 300:
        return 0.5  # Very Close

    elif box_width > 150:
        return 1.0  # Nearby

    else:
        return 5.0  # Far


def estimate_position(x_center, frame_width):

    if x_center < frame_width / 3:
        return "left"

    elif x_center > 2 * frame_width / 3:
        return "right"

    else:
        return "center"