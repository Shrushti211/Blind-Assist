`timescale 1ns / 1ps

module navigation_tb;

reg left, center, right;
wire warn_left, warn_center, warn_right;

// Instantiate the logic module
navigation_logic uut (
    .left(left),
    .center(center),
    .right(right),
    .warn_left(warn_left),
    .warn_center(warn_center),
    .warn_right(warn_right)
);

integer f;
integer status;
initial begin
    // Create the waveform file
    $dumpfile("navigation_wave.vcd");
    $dumpvars(0, navigation_tb);

    // Initial state
    left = 0; center = 0; right = 0;
    #10;

    // Read signals from the growing history file
    f = $fopen("navigation_history.txt", "r");
    if (f) begin
        while (!$feof(f)) begin
            status = $fscanf(f, "%d %d %d\n", left, center, right);
            if (status == 3) begin
                #100; // Simulate 100ns for each captured frame
            end
        end
        $fclose(f);
    end

    #10;
    $finish;
end

endmodule