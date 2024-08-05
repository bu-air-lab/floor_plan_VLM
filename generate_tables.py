import pandas as pd
import matplotlib.pyplot as plt

# Create the data for the table
# data = {
#     'Map 1': [0.93, 3.2],
#     'Map 2': [0.8, 3.6],
#     'Map 3': [0.67, 3.6],
#     'Map 4 (augmented Map 1)': [0.6, 4.2],
#     'Map 5 (augmented Map 2)': [0.67, 4.8],
#     'Map 6 (augmented Map 3)': [0.33, 4]
# }

data = {
    'Map 1': [1.0, 9.0],
    'Map 2': [0.86, 9.0],
    'Map 3': [0.8, 9.4],
    'Map 4 (augmented Map 1)': [0.66, 9.2],
    'Map 5 (augmented Map 2)': [0.4, 9.2],
    'Map 6 (augmented Map 3)': [0.13, 7.2]
}

# Create the DataFrame
df = pd.DataFrame(data, index=['Avg success rate', 'Avg plan length'])

# Plotting the table
fig, ax = plt.subplots(figsize=(10, 2))  # Adjust figsize for better clarity
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, cellLoc='center', loc='center')

# Add title
plt.title('4-room navigation with GPT-4o', pad=20)

# Adjust column widths
table.auto_set_column_width(col=list(range(len(df.columns))))

# Save the plot with higher resolution
plt.savefig('table.png', dpi=300, bbox_inches='tight', pad_inches=0.1)


# import pandas as pd
# import matplotlib.pyplot as plt

# # Create the data for the table
# data = {
#     'Map 1': [0.93, 3.2],
#     'Map 2': [0.8, 3.6],
#     'Map 3': [0.67, 3.6],
#     'Map 4 (augmented Map 1)': [0.6, 4.2],
#     'Map 5 (augmented Map 2)': [0.67, 4.8],
#     'Map 6 (augmented Map 3)': [0.33, 4]
# }

# # Create the DataFrame
# df = pd.DataFrame(data, index=['Avg success rate', 'Avg plan length'])

# # Plotting the table
# fig, ax = plt.subplots()
# ax.axis('tight')
# ax.axis('off')
# ax.table(cellText=df.values, colLabels=df.columns, rowLabels=df.index, cellLoc='center', loc='center')

# # Add title
# plt.title('2-room navigation with GPT-4o')

# # Show the plot
# plt.savefig('table.png', dpi=300)