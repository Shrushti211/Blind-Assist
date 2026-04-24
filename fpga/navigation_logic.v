module navigation_logic(

input left,
input center,
input right,

output reg warn_left,
output reg warn_center,
output reg warn_right

);

always @(*) begin

warn_left = 0;
warn_center = 0;
warn_right = 0;

if(center)
    warn_center = 1;

else if(left)
    warn_left = 1;

else if(right)
    warn_right = 1;

end

endmodule