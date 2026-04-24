import cv2
from ultralytics import YOLO
from distance_estimation import estimate_distance, estimate_position
from voice_alert import speak
import subprocess
import os


def run_system():
    print("Starting Blind Assist Navigation System...")

    # Clear history file at start
    with open("navigation_history.txt", "w") as f:
        f.write("")

    # Compile FPGA module once
    try:
        subprocess.run(
            ["iverilog", "-o", "nav_sim", "navigation_logic.v", "navigation_tb.v"],
            check=True
        )
        print("FPGA module compiled")
    except Exception as e:
        print("FPGA compilation failed", e)

    # Track if GTKWave is already opened
    gtkwave_opened = False

    # Load YOLO model
    model = YOLO("yolov8m.pt")

    # Open camera
    cap = cv2.VideoCapture(0)

    last_message = ""
    last_fpga_input = ""

    cv2.namedWindow("AI Navigation Vision", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("AI Navigation Vision", 800, 600)

    while True:

        ret, frame = cap.read()

        if not ret:
            print("Camera not detected")
            break

        # Run detection
        results = model(frame, imgsz=480, verbose=False)

        annotated_frame = results[0].plot()

        frame_width = frame.shape[1]
        frame_height = frame.shape[0]

        # Draw navigation zones
        left_line = frame_width // 3
        right_line = 2 * frame_width // 3

        cv2.line(annotated_frame,(left_line,0),(left_line,frame_height),(255,255,0),2)
        cv2.line(annotated_frame,(right_line,0),(right_line,frame_height),(255,255,0),2)

        closest_object = None
        closest_position = None
        closest_distance = float('inf')

        for box in results[0].boxes:

            x1, y1, x2, y2 = box.xyxy[0]

            box_width = x2 - x1
            x_center = (x1 + x2) / 2

            distance = float(estimate_distance(box_width))
            position = estimate_position(x_center, frame_width)

            label = model.names[int(box.cls[0])]

            if label not in ["person","chair","cell phone","laptop","bottle","cup"]:
                label = "object"

            if distance < closest_distance:
                closest_distance = distance
                closest_object = label
                closest_position = position

        # FPGA inputs
        left = 0
        center = 0
        right = 0

        if closest_position == "left":
            left = 1
        elif closest_position == "center":
            center = 1
        elif closest_position == "right":
            right = 1

        # Append to navigation history
        current_fpga_input = f"{left} {center} {right}"
        with open("navigation_history.txt", "a") as f:
            f.write(current_fpga_input + "\n")
        
        # Run FPGA simulation to update the .vcd with all history
        subprocess.run(["vvp", "nav_sim"])

        # Open GTKWave once
        if os.path.exists("navigation_wave.vcd") and not gtkwave_opened:
            subprocess.Popen([
                r"C:\iverilog\gtkwave\bin\gtkwave.exe",
                "navigation_wave.vcd"
            ])
            gtkwave_opened = True

        # Navigation decision
        if closest_object is None:
            message = "Path clear"
            arrow = "↑"

        elif closest_object == "person":
            message = "Get out of my way"
            arrow = "⚠"

        elif closest_position == "center":
            message = f"{closest_object} ahead"
            arrow = "⚠"

        elif closest_position == "left":
            message = f"{closest_object} on the left"
            arrow = "→"

        elif closest_position == "right":
            message = f"{closest_object} on the right"
            arrow = "←"

        else:
            message = "Obstacle nearby"
            arrow = "⚠"

        display_text = f"{arrow} {message.upper()}"

        cv2.putText(
            annotated_frame,
            display_text,
            (40,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            3
        )

        if message != last_message:
            speak(message)
            last_message = message

        cv2.imshow("AI Navigation Vision", annotated_frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_system()