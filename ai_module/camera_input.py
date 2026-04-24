import cv2
import subprocess
import os

print("Starting Camera + FPGA System")

# Compile FPGA module once
subprocess.run(["iverilog", "-o", "nav_sim", "navigation_logic.v", "navigation_tb.v"])

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera could not be opened")
    exit()

gtkwave_opened = False

while True:

    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    # Example navigation logic from camera position
    height, width, _ = frame.shape

    left = 0
    center = 1
    right = 0

    # Write FPGA inputs
    with open("fpga_input.txt", "w") as f:
        f.write(f"{left} {center} {right}")

    # Run FPGA simulation
    subprocess.run(["vvp", "nav_sim"])

    # Open GTKWave once
    if os.path.exists("navigation_wave.vcd") and not gtkwave_opened:
        subprocess.Popen([r"C:\iverilog\gtkwave\bin\gtkwave.exe", "navigation_wave.vcd"])
        gtkwave_opened = True

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()