include "globals.mzn";

% Variables 
int: plate_width;
int: n_circuits;
int: max_height;
int: min_height;

set of int: circuits = 1..n_circuits;
array[circuits] of int: circuit_heights;
array[circuits] of int: circuit_widths;

var min_height..max_height: plate_height;

array[circuits] of var 0..max_height: y;
array[circuits] of var 0..plate_width: x;

array[circuits] of int : areas = [circuit_heights[c]*circuit_widths[c] | c in circuits];

% index array ordered by circuit areas, widths, to be used for variabl
array[circuits] of int : sorted_area = reverse(sort_by(circuits, [circuit_heights[c]*circuit_widths[c] | c in circuits]));
array[circuits] of int : sorted_width = reverse(sort_by(circuits, [circuit_widths[c] | c in circuits]));

% cumulative constraints
constraint cumulative(x, circuit_widths, circuit_heights, plate_height);
constraint cumulative(y, circuit_heights, circuit_widths, plate_width);

% make sure that circuits do not exceed the plate dimensions
constraint forall(c in circuits)(x[c] + circuit_widths[c] <= plate_width);
constraint forall(c in circuits)(y[c] + circuit_heights[c] <= plate_height);

% remove overlapping
constraint diffn(x, y, circuit_widths, circuit_heights);

% The biggest circuit is always placed at (0,0)
% DRAMATICALLY IMPROVED MODEL
constraint symmetry_breaking_constraint(x[sorted_area[1]] = 0 /\
                                        y[sorted_area[1]] = 0);

% solve :: seq_search([
%     int_search([plate_height], dom_w_deg, indomain_min),
%     int_search([x[i] | i in sorted_idx], input_order, indomain_min),
%     int_search([y[i] | i in sorted_idx], input_order, indomain_min), 
% ])
% minimize plate_height;

solve :: seq_search([
    int_search([plate_height], dom_w_deg, indomain_min),
    int_search(x, dom_w_deg, indomain_min),
    int_search(y, dom_w_deg, indomain_min), 
])
minimize plate_height;

% output ["\(areas)"++"\(ordered_c)"];