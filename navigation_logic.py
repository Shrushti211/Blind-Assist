from vision_module.voice_alert import speak

def navigation_warning(object_name, distance, position):

    position = position.lower()

    if position == "left":
        direction = "on the left"
    elif position == "right":
        direction = "on the right"
    else:
        direction = "ahead"

    if distance == "Very Close":
        message = f"Warning! {object_name} very close {direction}"
    elif distance == "Nearby":
        message = f"{object_name} {direction}"
    else:
        message = f"{object_name} detected {direction}"

    speak(message)

    return message

def safe_path(objects_detected):

    if len(objects_detected) == 0:

        return "Path clear"

    for obj in objects_detected:

        if obj["position"] == "center":

            return "Obstacle ahead move left or right"

    return "Path partially clear"