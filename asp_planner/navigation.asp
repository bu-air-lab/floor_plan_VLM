%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  Actions
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
at(R2,I+1) :- approach(D,I), at(R1,I), hasdoor(R2,D), acc(R1,R2), I=0..n-2.
facing(D,I+1) :- approach(D,I), door(D), I=0..n-2.
:- approach(D,I), facing(D,I), door(D), I=0..n-1.
:- approach(D,I), at(R1,I), door(D), dooracc(R3,D,R2), not acc(R1,R3), not acc(R1,R2), I=0..n-1.

at(L,I+1) :- goto(L,I), at(R,I), acc(L,R), I=0..n-2.
:- goto(L,I), at(L,I), I=0..n-1.
:- goto(L2,I), at(L1,I), not acc(L1,L2), I=0..n-1.
:- goto(L2,I), at(L1,I), acc(R1,L2), not acc(L1,L2), not acc(L1,R1), I=0..n-1.

at(R2,I+1) :- gothrough(D,I), at(R1,I), dooracc(R1,D,R2), location(R1), location(R2), I=0..n-2.
-facing(D,I+1) :- gothrough(D,I), I=0..n-2.
:- gothrough(D,I), not facing(D,I), door(D), I=0..n-1.
:- gothrough(D,I), not open(D,I), door(D), I=0..n-1.
:- gothrough(D,I), at(R,I), not hasdoor(R,D), door(D), location(R), I=0..n-1.


open(D,I+1) :- opendoor(D,I), door(D), I=0..n-2.
:- opendoor(D,I), not facing(D,I), door(D), I=0..n-1.
:- opendoor(D,I), open(D,I), door(D), I=0..n-1.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  Static laws
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%you can't be at two places at the some time
% -at(R1,I):- at(L1,I), room(R1),     location(L1), R1 != L1, I=0..n-1.
% -at(R1,I):- at(R2,I), room(R1),     room(R2),     R1 != R2, I=0..n-1.
-at(L1,I):- at(L2,I), location(L1), location(L2), L1 != L2, I=0..n-1.
% -at(L1,I):- at(R1,I), location(L1), room(R1),     L1 != R1, I=0..n-1.

%you can be facing only one door at a time
-facing(D2,I):- facing(D1,I), door(D2), D1 != D2, I=0..n-1.

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  Inertia
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%at is inertial
at(R,I+1) :- at(R,I), not -at(R,I+1), I=0..n-2.

%facing is inertial
facing(D,I+1) :- facing(D,I), not -facing(D,I+1), I=0..n-2.
-facing(D,I+1) :- -facing(D,I), not facing(D,I+1), I=0..n-2.

% open is inertial
open(D,I+1) :- open(D,I), not -open(D,I+1), I=0..n-2.
-open(D,I+1) :- -open(D,I), not open(D,I+1), I=0..n-2.
