import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the mapped dataset from the JSON file
with open('./modules/module_0/mapped_explorations_dataset_corrected.json', 'r') as f:
    mapped_dataset = json.load(f)

# Convert the mapped dataset into a flat list of explorers
explorers_data = np.array([explorer for excursion in mapped_dataset for explorer in excursion])

# Characteristics mapped to their respective index positions
characteristics = [
    "Untraveled paths",
    "Physical challenge",
    "Flora diversity",
    "Fauna diversity",
    "Historical sites",
    "Water sites"
]

# Analyzing the statistical properties for each characteristic
for i, characteristic in enumerate(characteristics):
    characteristic_values = explorers_data[:, i]
    
    print(f"Characteristic: {characteristic}")
    print(f"Count: {np.count_nonzero(characteristic_values)}")
    print(f"Mean: {np.mean(characteristic_values):.2f}")
    print(f"Standard Deviation: {np.std(characteristic_values):.2f}")
    print(f"25th Percentile: {np.percentile(characteristic_values, 25):.2f}")
    print(f"50th Percentile (Median): {np.percentile(characteristic_values, 50):.2f}")
    print(f"75th Percentile: {np.percentile(characteristic_values, 75):.2f}")
    print(f"Minimum Value: {np.min(characteristic_values):.2f}")
    print(f"Maximum Value: {np.max(characteristic_values):.2f}")
    print("\n")
    
    # # Plotting the distribution of the characteristic
    # sns.histplot(characteristic_values, bins=20, kde=True)
    # plt.title(f'Distribution of {characteristic}')
    # plt.xlabel('Score')
    # plt.ylabel('Frequency')
    # plt.show()

# # Relationship between characteristics - Correlation matrix
# correlation_matrix = np.corrcoef(explorers_data.T)

# # Plotting the correlation matrix
# sns.heatmap(correlation_matrix, annot=True, xticklabels=characteristics, yticklabels=characteristics, cmap='coolwarm')
# plt.title('Correlation Matrix Between Characteristics')
# plt.show()
print("######################################First hike#################################\n\n")

for i, characteristic in enumerate(characteristics):

    characteristic_values = explorers_data[0, i]
        
    print(f"Characteristic: {characteristic}")
    print(f"Count: {np.count_nonzero(characteristic_values)}")
    print(f"Mean: {np.mean(characteristic_values):.2f}")
    print(f"Standard Deviation: {np.std(characteristic_values):.2f}")
    print(f"25th Percentile: {np.percentile(characteristic_values, 25):.2f}")
    print(f"50th Percentile (Median): {np.percentile(characteristic_values, 50):.2f}")
    print(f"75th Percentile: {np.percentile(characteristic_values, 75):.2f}")
    print(f"Minimum Value: {np.min(characteristic_values):.2f}")
    print(f"Maximum Value: {np.max(characteristic_values):.2f}")
    print("\n")