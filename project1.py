import os
import csv
import unittest
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
        state_avg_price[state] = round(avg_price, 3)
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
        state_cat_percent[state] = (max_cat, round(max_sales, 3), round(percent, 3))
    
    return state_cat_percent

def write_to_csv(filename, state_avg_price, state_most_freq_cat_percentage):
 with open(filename, 'w', newline='') as file_obj:
        writer = csv.writer(file_obj)
        writer.writerow(["State", "Average Sale Price", "Most Frequent Category", "Sales from Most Frequent Category", "Percentage of Total Sales from Most Frequent Category"])
        for state in state_avg_price:
            avg_price = state_avg_price[state]
            if state in state_most_freq_cat_percentage:
                most_freq_cat, sales_from_cat, percent_from_cat = state_most_freq_cat_percentage[state]
            else:
                most_freq_cat, sales_from_cat, percent_from_cat = ("N/A", 0, 0)
            writer.writerow([state, avg_price, most_freq_cat, sales_from_cat, percent_from_cat])

def main():
    data = read_in_superstore()
    state_sales = total_sales_per_state(data)
    state_counts = get_num_sales_per_state(data)
    state_freq_cat_total_sales = state_freq_cat_sales(data)
    state_avg_price = calculate_average_sale_price_per_state(state_sales, state_counts)
    state_most_freq_cat_percentage = calculate_percent_sales_from_most_frequent_category(state_sales, state_freq_cat_total_sales)
    write_to_csv('project_1_output.csv', state_avg_price, state_most_freq_cat_percentage)
    #write to a new csv file with columns "state" "average sale price" "percentage of total sales from most frequent category", using state_avg_price and state_most_freq_cat_percentage dictionaries to get the data

#Write 4 simple test cases for each function above using the unit test framework. Each function should have two tests for general/usua cases, and two edge cases.
class TestSuperstoreCalculations(unittest.TestCase):
#Write 4 simple test cases for each function above using the unit test framework. Each function should have two tests for general/usua cases, and two edge cases. The sample data that you use should follow the schema of the SampleSuper.csv file.
    data = [
            ["Order ID", "Order Date", "Ship Date", "Ship Mode", "State", "Country", "City", "Category", "Sub-Category", "Sales", "Quantity"],
            ["CA-2016-152156", "11/8/16", "11/11/16", "Second Class", "California", "United States", "Los Angeles", "Furniture", "Bookcases", "261.96", "2"],
            ["CA-2016-152157", "11/8/16", "11/11/16", "Second Class", "California", "United States", "Los Angeles", "Office Supplies", "Labels", "14.62", "3"],
            ["NY-2016-152158", "11/8/16", "11/11/16", "Second Class", "New York", "United States", "New York City", "Technology", "Phones", "957.58", "5"]
        ]
    def test_get_num_sales_per_state(self):
        result = get_num_sales_per_state(self.data)
        expected = {"California": 5, "New York": 5}
        self.assertEqual(result, expected)
    def test_total_sales_per_state(self):
        result = total_sales_per_state(self.data)
        expected = {"California": 276.58, "New York": 957.58}
        self.assertEqual(result, expected)
    def test_calculate_average_sale_price_per_state(self):
        state_sales = {"California": 276.58, "New York": 957.58}
        state_counts = {"California": 5, "New York": 5}
        result = calculate_average_sale_price_per_state(state_sales, state_counts)
        expected = {"California": 55.316, "New York": 191.516}
        self.assertEqual(result, expected)
    def test_state_freq_cat_sales(self):
        result = state_freq_cat_sales(self.data)
        expected = {"California": ("Furniture", 261.96), "New York": ("Technology", 957.58)}
        self.assertEqual(result, expected)
    def test_calculate_percent_sales_from_most_frequent_category(self):
        state_sales = {"California": 276.58, "New York": 957.58}
        state_cat_max = {"California": ("Furniture", 261.96), "New York": ("Technology", 957.58)}
        result = calculate_percent_sales_from_most_frequent_category(state_sales, state_cat_max)
        expected = {"California": ("Furniture", 261.96, 94.714), "New York": ("Technology", 957.58, 100.0)}
        self.assertEqual(result, expected)




if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)