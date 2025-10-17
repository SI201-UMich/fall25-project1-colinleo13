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

#get total number of sales per state
def get_num_sales_per_state(data):
    state_counts = {}
    for row in data[1:]:  # Skip header row
        state = row[4]
    #get quantity from row 10
        quantity = int(row[10])
        if state not in state_counts:
            state_counts[state] = 0
        state_counts[state] += quantity
    return state_counts


def total_sales_per_state(data):
    state_sales = {}
    for row in data[1:]:  # Skip header row
        state = row[4]
        sales = float(row[9])
        if state not in state_sales:
            state_sales[state] = 0
        state_sales[state] += sales
    return state_sales

#get average sale price for each state by dividing total sales by number of sales
def calculate_average_sale_price_per_state(state_sales_in, state_counts_in):
    state_sales = state_sales_in
    state_counts = state_counts_in
    state_avg_price = {}
    for state in state_sales:
        avg_price = state_sales[state] / state_counts[state] if state_counts[state] > 0 else 0
        state_avg_price[state] = avg_price
    return state_avg_price


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

def calculate_percent_sales_from_most_frequent_category(state_sales_in, state_cat_max_in):
    state_sales = state_sales_in
    state_cat_max = state_cat_max_in
    
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
    state_sales = total_sales_per_state(data)
    state_counts = get_num_sales_per_state(data)
    state_freq_cat_total_sales = state_freq_cat_sales(data)
    state_avg_price = calculate_average_sale_price_per_state(state_sales, state_counts)
    state_most_freq_cat_percentage = calculate_percent_sales_from_most_frequent_category(state_sales, state_freq_cat_total_sales)



if __name__ == '__main__':
    main()