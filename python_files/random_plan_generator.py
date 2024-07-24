import random

# Read the room lists from the provided data
room_lists = {
    'simple1': ['CH.3', 'CH.2', 'CH.1', 'SEJOUR', 'CUISINE'],
    'medium1': ['CELLIER', 'SEJOUR', 'CUISINE', 'DEGT.', 'WC', 'BAINS', 'CH.1', 'CH.2', 'PORCHE'],
    'complex1': ['GARAGE', 'CELLIER', 'CHAMBRE 2', 'BAINS', 'WC', 'CHAMBRE 1', 'PORCHE', 'HALL', 'CUISINE', 'TERRASSE COUVERTE'],
    'complex2': ['GARAGE', 'CELLIER', 'CHAMBRE 2', 'BAINS', 'WC', 'PORCHE', 'HALL', 'CHAMBRE 1', 'CUISINE', 'TERRASSE COUVERTE'],
    'complex3': ['PORCHE', 'LINGERIE', 'BUREAU', 'BAINS', 'CHAMBRE PARENTS', 'GARAGE', 'CELLIER', 'HALL', 'WC', 'CHAMBRE ENFANT 1', 'CHAMBRE ENFANT 2'],
    'simple2': ['CH.1', 'BAINS', 'GARAGE', 'CH.2', 'HALL', 'CUISINE'],
    'medium2': ['GARAGE', 'CHAMBRE 1', 'CELLIER', 'BAINS', 'WC', 'HALL', 'CHAMBRE 3', 'CHAMBRE 2', 'PORCHE'],
    'medium3': ['GARAGES', 'DOUCHE', 'CELLIER', 'WC', 'CHAMBRE 1', 'CUISINE', 'HALL'],
    'simple3': ['CUISINE', 'CELLIER', 'TERRASSE COUVERTE', 'DOUCHE', 'CH. PARENTS']
}

# Generate 5 random plans for each room list
random_plans = {}
for key, rooms in room_lists.items():
    plans = []
    for _ in range(5):
        start, intermediate, end = random.sample(rooms, 3)
        plans.append((start, intermediate, end))
    random_plans[key] = plans

# Print the random plans
for key, plan_list in random_plans.items():
    print(f"{key}: {plan_list}")