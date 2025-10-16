import os
import csv
def read_in_superstore():
    """
    Reads in the 'superstore.csv' file and returns its contents as a list of lists.
    
    Returns:
        list: A list of lists, where each inner list represents a row from the CSV file.
    """
    base_path = os.path.dirname(__file__)
    filename = 'SampleSuperstore.csv'
    full_path = os.path.join(base_path, filename)
    
    with open(full_path, 'r') as file_obj:
        reader = csv.reader(file_obj)
        data = list(reader)
    
    return data

#average sale price per category



def total_sales_per_state(data):
    state_sales = {}
    for row in data[1:]:  # Skip header row
        state = row[4]
        sales = float(row[9])
        if state not in state_sales:
            state_sales[state] = 0
        state_sales[state] += sales
    return state_sales


def state_freq_cat_sales(data):
#most frequent category per state with total sales from that category for that state
    state_cat = {}
    for row in data[1:]:  # Skip header row
        state = row[4]
        category = row[7]
        sales = float(row[9])
        if state not in state_cat:
            state_cat[state] = {}
        if category not in state_cat[state]:
            state_cat[state][category] = 0
        state_cat[state][category] += sales

    state_cat_max = {}
    for state in state_cat:
        max_cat = None
        max_sales = 0
        for cat in state_cat[state]:
            if state_cat[state][cat] > max_sales:
                max_cat = cat
                max_sales = state_cat[state][cat]
        state_cat_max[state] = (max_cat, max_sales)
    
    return state_cat_max

def calculate_percent_sales_from_most_frequent_category(data):
    state_sales = total_sales_per_state(data)
    state_cat_max = state_freq_cat_sales(data)
    
    state_cat_percent = {}
    for state in state_cat_max:
        max_cat, max_sales = state_cat_max[state]
        total_sales = state_sales[state]
        percent = (max_sales / total_sales) * 100 if total_sales > 0 else 0
        state_cat_percent[state] = (max_cat, max_sales, percent)
    
    return state_cat_percent
 

def main():
    data = read_in_superstore()
    percent_sales_most_freq = calculate_percent_sales_from_most_frequent_category(data)
    print(percent_sales_most_freq)

if __name__ == '__main__':
    main()