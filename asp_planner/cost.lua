#script (lua)
-- clingo = require("clingo")
-- N = clingo.Number
-- F = clingo.Function

stairs = {15.3963861465, -4.60112667084}
elevator = {18.1897678375, 15.777630806}
water_fountain = {8.17935752869, 30.2605838776}
waiting_room = {-6.25724887848, 38.9669075012}
kitchen = {-8.15394687653, 64.0944595337}

lab1 = {-0.760191917419, 7.65376281738}
lab2 = {0.753301620483, -3.95647525787}
a1 = {-1.17305183411, 8.99259757996}
a2 = {9.86956119537, 15.9883003235}
a3 = {3.3401260376, 40.6803817749}
b1 = {-0.202418327332, -5.40789985657}
b2 = {20.1075153351, -11.3619117737}
c1 = {19.6808776855, -9.35009288788}
c2 = {11.4531002045, 16.33893013}
c3 = {6.71399879456, 40.8018875122}

door_cost = 15

--Compute distances from each reachable location pair
function distanceFrom(l1,l2) 
	distance = math.sqrt((l1[1] - l2[1]) ^ 2 + (l1[2] - l2[2]) ^ 2) 
	return math.floor(distance)
end


lab1_a1 = distanceFrom(lab1, a1) + door_cost
lab1_lab2 = distanceFrom(lab1, lab2)

lab2_b1 = distanceFrom(lab2, b1) + door_cost

a1_a2 = distanceFrom(a1, a2)
a1_a3 = math.floor(distanceFrom(a1, a3) * 1.5) --this path is not a straight line
a1_b1 = math.floor(distanceFrom(a1, b1) * 1.5) --this path is not a straight line
a1_waiting_room = math.floor(distanceFrom(a1, waiting_room) * 1.25)
a1_kitchen = math.floor(distanceFrom(a1, kitchen) * 1.5)

a2_a3 = math.floor(distanceFrom(a2, a3) * 1.5) --this path is not a straight line
a2_c2 = distanceFrom(a2, c2) + door_cost
a2_waiting_room = math.floor(distanceFrom(a2, waiting_room) *1.5)
a2_kitchen = math.floor(distanceFrom(a2, kitchen) * 1.5)

a3_c3 = distanceFrom(a3, c3) + door_cost
a3_waiting_room = distanceFrom(a3, waiting_room)
a3_kitchen = math.floor(distanceFrom(a3, kitchen) * 2.5)

b1_b2 = distanceFrom(b1, b2)

b2_c1 = distanceFrom(b2, c1) + door_cost

c1_c2 = distanceFrom(c1, c2)
c1_stairs = distanceFrom(c1, stairs)
c1_elevator = math.floor(distanceFrom(c1, elevator)*1.25)

c2_stairs = distanceFrom(c2, stairs)
c2_elevator = distanceFrom(c2, elevator)
c2_water_fountain = distanceFrom(c2, water_fountain)
c2_c3 = distanceFrom(c2, c3)

c3_water_fountain = distanceFrom(c3, water_fountain)


function dis(a,b)

	x_location = a.name
	y_location = b.name

	ret = 1
	if x_location==y_location then
	    ret = 1
	end

	if x_location == 'lab1' then
	    if y_location == 'a1' then ret = lab1_a1 end
	    if y_location == 'lab2' then ret = lab1_lab2 end
	end

	if x_location == 'lab2' then
		if y_location == 'lab1' then ret = lab1_lab2 end
	    if y_location == 'b1' then ret = lab2_b1 end
	end

	if x_location == 'a1' then
		if y_location == 'lab1' then ret = lab1_a1 end
	    if y_location == 'a2' then ret = a1_a2 end
	    if y_location == 'a3' then ret = a1_a3 end
	    if y_location == 'b1' then ret = a1_b1 end
		if y_location == 'waiting_room' then ret = a1_waiting_room end
		if y_location == 'kitchen' then ret = a1_kitchen end
	end

	if x_location == 'a2' then
		if y_location == 'a1' then ret = a1_a2 end
	    if y_location == 'a3' then ret = a2_a3 end
	    if y_location == 'c2' then ret = a2_c2 end
		if y_location == 'waiting_room' then ret = a2_waiting_room end
		if y_location == 'kitchen' then ret = a2_kitchen end
	end

	if x_location == 'a3' then
		if y_location == 'a2' then ret = a2_a3 end
		if y_location == 'a1' then ret = a1_a3 end
	    if y_location == 'c3' then ret = a3_c3 end
		if y_location == 'waiting_room' then ret = a3_waiting_room end
		if y_location == 'kitchen' then ret = a3_kitchen end
	end

	if x_location == 'b1' then
		if y_location == 'a1' then ret = a1_b1 end
		if y_location == 'lab2' then ret = lab2_b1 end
	    if y_location == 'b2' then ret = b1_b2 end
	end

	if x_location == 'b2' then
		if y_location == 'b1' then ret = b1_b2 end
	    if y_location == 'c1' then ret = b2_c1 end
	end

	if x_location == 'c1' then
		if y_location == 'b2' then ret = b2_c1 end
	    if y_location == 'c2' then ret = c1_c2 end
	    if y_location == 'staircase' then ret = c1_stairs end
		if y_location == 'elevator' then ret = c1_elevator end
	end

	if x_location == 'c2' then
		if y_location == 'c1' then ret = c1_c2 end
		if y_location == 'a2' then ret = a2_c2 end
	    if y_location == 'staircase' then ret = c2_stairs end
	    if y_location == 'elevator' then ret = c2_elevator end
	    if y_location == 'water_fountain' then ret = c2_water_fountain end
		if y_location == 'c3' then ret = c2_c3 end
	end

	if x_location == 'c3' then
		if y_location == 'a3' then ret = a3_c3 end
		if y_location == 'c2' then ret = c2_c3 end
	    if y_location == 'water_fountain' then ret = c3_water_fountain end
	end

	if x_location == 'water_fountain' then
		if y_location == 'c3' then ret = c3_water_fountain end
		if y_location == 'c2' then ret = c2_water_fountain end
	end

	if x_location == 'staircase' then
		if y_location == 'c1' then ret = c1_stairs end
		if y_location == 'c2' then ret = c2_stairs end
	end

	if x_location == 'elevator' then
		if y_location == 'c1' then ret = c1_elevator end
		if y_location == 'c2' then ret = c2_elevator end
	end

	if x_location == 'waiting_room' then
		if y_location == 'a1' then ret = a1_waiting_room end
		if y_location == 'a2' then ret = a2_waiting_room end
		if y_location == 'a3' then ret = a3_waiting_room end
	end

	if x_location == 'kitchen' then
		if y_location == 'a1' then ret = a1_kitchen end
		if y_location == 'a2' then ret = a2_kitchen end
		if y_location == 'a3' then ret = a3_kitchen end
	end
	--print(ret)
	return ret
end

#end.