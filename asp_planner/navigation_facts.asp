location(staircase).
location(elevator).
location(lab1).
location(lab2).
location(water_fountain).
location(waiting_room).
location(kitchen).
location(a1).
location(a2).
location(a3).
location(b1).
location(b2).
location(c1).
location(c2).
location(c3).

door(d1).
door(d2).
door(d3).
door(d4).
door(d5).

hasdoor(a1, d1).
hasdoor(a2, d4).
hasdoor(a3, d5).
hasdoor(b1, d2).
hasdoor(b2, d3).
hasdoor(c1, d3).
hasdoor(c2, d4).
hasdoor(c3, d5).
hasdoor(lab1, d1).
hasdoor(lab2, d2).

%Accessibility
acc(a1, a2).
acc(a1, a3).
acc(a1, b1).
acc(a1, waiting_room).
acc(a1, kitchen).
acc(a2, a3).
acc(a2, waiting_room).
acc(a2, kitchen).
acc(a3, waiting_room).
acc(a3, kitchen).
acc(b1, b2).
acc(c1, staircase).
acc(c1, c2).
acc(c1, elevator).
acc(c2, elevator).
acc(c2, staircase).
acc(c2, water_fountain).
acc(c2, c3).
acc(c3, water_fountain).
acc(lab1, lab2).

dooracc(P1,D,P2) :- hasdoor(P1,D), hasdoor(P2,D), P1 != P2, door(D), location(P1), location(P2).
dooracc(P1,D,P2) :- dooracc(P2,D,P1).

acc(L,L) :- location(L).
acc(L1,L2) :- acc(L2,L1), location(L1), location(L2).
% acc(L1,L2) :- acc(L1,_L), acc(L2,_L), location(L1), location(L2), location(_L).

% acc(R,R) :- room(R).
% acc(R1,R2) :- acc(R2,R1), room(R1), room(R2).
% acc(R1,R2) :- acc(R1,_R), acc(R2,_R), room(R1), room(R2), room(_R).

% acc(R,L) :- acc(L,R), room(R), location(L).
% acc(L,R) :- acc(R,L), room(R), location(L).
% acc(R,L) :- acc(R,_R), acc(L,_R), room(R), location(L), room(_R).
% acc(L,R) :- acc(L,_L), acc(R,_L), room(R), location(L), location(_L).

pos(X) :- location(X).
% pos(X) :- room(X).
cost(X, Y, L) :- L=@dis(X, Y), pos(X), pos(Y).
path(X, Y, I+1) :- at(X, I), at(Y, I+1), I=0..n-2.