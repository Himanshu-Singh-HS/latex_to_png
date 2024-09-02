import csv
import json
import pandas as pd 
def sort_and_output_classifications(json_data,csvfile):
    with open(json_data, 'r') as file:
        data = json.load(file)
    
    classification_patent_counts = {key: value for key, value in data.items()}
    sorted_classifications = sorted(classification_patent_counts.items(), key=lambda item: len(item[1]))
 
    # for classification, patents in sorted_classifications:
    #     print(f"Classification: {classification}")
    #     print(f"Number of Patents: {len(patents)}")
    #     print(f"List of Patents: {patents}")
    #     print()

    with open(csvfile, 'w', newline='') as csvfile:
        fieldnames = ['Classification', 'Patents count', 'Patent numbers']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for classification, patents in sorted_classifications:
            writer.writerow({
                'Classification': classification,
                'Patents count': len(patents),
                'Patent numbers': ', '.join(patents)  
            })
   

json_data = "leaf_classifications.json"  
csvfile="sorted_patent.csv"
sort_and_output_classifications(json_data,csvfile)


# Load the CSV file into a DataFrame
df = pd.read_csv('sorted_patent.csv')

# Display the first 15 rows in the required text format
for index, row in df.head(3344).iterrows():
    with open('sorted_till_15counts.txt','a') as f:
        f.write(f"{row['Classification']},{row['Patents count']}\n")
    print(f"{row['Classification']},{row['Patents count']}")
