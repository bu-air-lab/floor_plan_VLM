## TODO
	- log all results
	- make figure
	- start paper (correct template, references)
	- plan demo
	- Evaluate based on planners understanding of door connections

Dataset names:

	fully labeled
	ablation 1 (one label per room)
	ablation 2 (original door symbols + multiple labels per room)
	ablation 3 (original door symbols + 1 label per room)
	ablation 4 (don't ask VLM to output door and room connections)



More difficult task:

1. Harder maps (more rooms)
2. Dotted lines (add GOTO)
3. More complex task (A->B->C->D)

		- every task contains 3 locations? Or some contains 2, and some contains 4?





No GOTO command, no dotted lines
1. crop, rename ablation 1
2. crop, add labels, rename ablation 2
3. Log results (manually label correctness and plan length)
4. Report results (avg accuracy and avg plan length)
5. make figures
6. Repeat steps 3-5 for ablations
7. write paper



Dashed rooms:

1. added dotted lines to complex maps
2. Add new "rooms" for complex maps
3. Make new prompt for complex maps
4. Add to room list for pre-defined plans


Comment:

	The VLM tells us how it understands the floor layout via room and door connections