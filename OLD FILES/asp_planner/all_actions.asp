%LIST HERE ANY ACTION YOU ADD!!!

1{	approach(D,I) : door(D);
	gothrough(D,I) : door(D);
	opendoor(D,I) : door(D);
	goto(L,I) : location(L)
	}1 :- not noop(I), I=0..n-2.

%removes the warning about noop not being defined, shouldn't have any consequences
noop(n).

%#hide noop/1.
