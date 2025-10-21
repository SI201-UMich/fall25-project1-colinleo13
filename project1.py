# author Colin Leonard
# umid 2262 5134
# colinleo@umich.edu
#assignment: Project 1
#All functions below written by Colin Leonard
#AI use: Used ChatGPT to help debug an error with the file writing location, used ChatGPT for ideas for different test cases.


import os
import csv
import unittest
def read_in_superstore(filename='SampleSuperstore.csv'):
    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, filename)
    
    with open(full_path, 'r') as file_obj:
        reader = csv.reader(file_obj)
        data = list(reader)
    
    return data

def get_num_sales_per_state(data):
    state_counts = {}
    for row in data[1:]:  
        state = row[4]
        quantity = int(row[10])
        if state not in state_counts:
            state_counts[state] = 0
        state_counts[state] += quantity
    return state_counts


def total_sales_per_state(data):
    state_sales = {}
    for row in data[1:]:  
        state = row[4]
        sales = float(row[9])
        if state not in state_sales:
            state_sales[state] = 0
        state_sales[state] += sales
    return state_sales

def calculate_average_sale_price_per_state(state_sales_in, state_counts_in):
    state_sales = state_sales_in
    state_counts = state_counts_in
    state_avg_price = {}
    for state in state_sales:
        avg_price = state_sales[state] / state_counts.get(state, 0) if state_counts.get(state, 0) > 0 else 0
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
        total_sales = state_sales.get(state, 0.0)
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
    base_path = os.path.dirname(__file__)
    output_path = os.path.join(base_path, 'project_1_output.csv')
    write_to_csv(output_path, state_avg_price, state_most_freq_cat_percentage)
    print(data[0])
    
class TestSuperstoreCalculations(unittest.TestCase):
    header = [
        "Ship Mode", "Segment", "Country", "City", "State", "Postal Code", "Region",
        "Category", "Sub-Category", "Sales", "Quantity", "Discount", "Profit"
    ]

    data = [header,
        ["Second Class", "Consumer",  "United States", "Los Angeles",   "California", "90036", "West",    "Furniture",       "Bookcases",  "261.96", "2", "0.00", "41.913"],
        ["Second Class", "Consumer",  "United States", "Los Angeles",   "California", "90036", "West",    "Office Supplies", "Labels",     "14.62",  "3", "0.00", "6.871"],
        ["Standard Class","Corporate","United States", "Houston",       "Texas",      "77041", "Central", "Technology",      "Phones",     "100.00", "1", "0.10", "9.000"],
        ["Standard Class","Corporate","United States", "Houston",       "Texas",      "77041", "Central", "Office Supplies", "Paper",      "50.00",  "4", "0.20", "3.000"],
        ["Second Class", "Consumer",  "United States", "New York City", "New York",   "10024", "East",    "Technology",      "Phones",     "957.58", "5", "0.00", "200.00"],
    ]

    data_header_only = [header]

    data_all_zero = [header,
        ["First Class", "Consumer",  "United States", "Reno",      "Nevada",  "89501", "West", "Furniture",  "Tables",      "0", "0", "0.00", "0.00"],
        ["First Class", "Consumer",  "United States", "Reno",      "Nevada",  "89501", "West", "Technology", "Accessories", "0", "0", "0.00", "0.00"],
    ]

    data_tie = [header,
        ["Second Class", "Consumer",  "United States", "Atlanta", "Georgia", "30303", "South", "Furniture",  "Tables", "60", "1", "0.00", "5.00"],
        ["Second Class", "Consumer",  "United States", "Atlanta", "Georgia", "30303", "South", "Technology", "Phones",  "60", "1", "0.00", "8.00"],
    ]

    def test_get_num_sales_per_state_general(self):
        result = get_num_sales_per_state(self.data)
        self.assertEqual(result, {"California": 5, "Texas": 5, "New York": 5})

    def test_get_num_sales_per_state_general_subset(self):
        subset = [self.header] + self.data[1:5]  
        result = get_num_sales_per_state(subset)
        self.assertEqual(result, {"California": 5, "Texas": 5})

    def test_get_num_sales_per_state_header_only(self):
        self.assertEqual(get_num_sales_per_state(self.data_header_only), {})

    def test_get_num_sales_per_state_all_zero(self):
        self.assertEqual(get_num_sales_per_state(self.data_all_zero), {"Nevada": 0})

    def test_total_sales_per_state_general(self):
        result = total_sales_per_state(self.data)

        self.assertEqual(result, {"California": 276.58, "Texas": 150.00, "New York": 957.58})

    def test_total_sales_per_state_general_subset(self):
        subset = [self.header] + self.data[1:5]
        result = total_sales_per_state(subset)
        self.assertEqual(result, {"California": 276.58, "Texas": 150.00})

    def test_total_sales_per_state_header_only(self):
        self.assertEqual(total_sales_per_state(self.data_header_only), {})

    def test_total_sales_per_state_all_zero(self):
        self.assertEqual(total_sales_per_state(self.data_all_zero), {"Nevada": 0.0})

    def test_calculate_average_sale_price_per_state_general(self):
        state_sales = total_sales_per_state(self.data)
        state_counts = get_num_sales_per_state(self.data)
        result = calculate_average_sale_price_per_state(state_sales, state_counts)
        self.assertEqual(result, {"California": 55.316, "Texas": 30.0, "New York": 191.516})

    def test_calculate_average_sale_price_per_state_general_subset(self):
        subset = [self.header] + self.data[1:5]
        sales = total_sales_per_state(subset)
        counts = get_num_sales_per_state(subset)
        result = calculate_average_sale_price_per_state(sales, counts)
        self.assertEqual(result, {"California": 55.316, "Texas": 30.0})

    def test_calculate_average_sale_price_per_state_zero_count(self):
        sales = total_sales_per_state(self.data)
        counts = get_num_sales_per_state(self.data)
        counts["Texas"] = 0
        result = calculate_average_sale_price_per_state(sales, counts)
        self.assertEqual(result["Texas"], 0)

    def test_calculate_average_sale_price_per_state_missing_key(self):
        sales = {"Oregon": 12.0}
        counts = {}  
        result = calculate_average_sale_price_per_state(sales, counts)
        self.assertEqual(result, {"Oregon": 0})

    def test_state_freq_cat_sales_general(self):
        result = state_freq_cat_sales(self.data)
        self.assertEqual(
            result,
            {"California": ("Furniture", 261.96), "Texas": ("Technology", 100.0), "New York": ("Technology", 957.58)}
        )

    def test_state_freq_cat_sales_general_subset(self):
        subset_tx = [self.header] + self.data[3:5]  
        result = state_freq_cat_sales(subset_tx)
        self.assertEqual(result, {"Texas": ("Technology", 100.0)})

    def test_state_freq_cat_sales_tie_first_encountered(self):
        self.assertEqual(state_freq_cat_sales(self.data_tie), {"Georgia": ("Furniture", 60.0)})

    def test_state_freq_cat_sales_header_only(self):
        self.assertEqual(state_freq_cat_sales(self.data_header_only), {})

    def test_calculate_percent_sales_from_most_frequent_category_general(self):
        totals = total_sales_per_state(self.data)
        max_cat = state_freq_cat_sales(self.data)
        result = calculate_percent_sales_from_most_frequent_category(totals, max_cat)
        self.assertEqual(result["California"], ("Furniture", 261.96, 94.714))
        self.assertEqual(result["Texas"], ("Technology", 100.0, 66.667))
        self.assertEqual(result["New York"], ("Technology", 957.58, 100.0))

    def test_calculate_percent_sales_from_most_frequent_category_general_subset(self):
        subset_tx = [self.header] + self.data[3:5]
        totals = total_sales_per_state(subset_tx)
        max_cat = state_freq_cat_sales(subset_tx)
        result = calculate_percent_sales_from_most_frequent_category(totals, max_cat)
        self.assertEqual(result, {"Texas": ("Technology", 100.0, 66.667)})

    def test_calculate_percent_sales_from_most_frequent_category_zero_total(self):
        totals = {"Nevada": 0.0}
        max_cat = {"Nevada": ("Technology", 0.0)}
        self.assertEqual(
            calculate_percent_sales_from_most_frequent_category(totals, max_cat),
            {"Nevada": ("Technology", 0.0, 0)}
        )

    def test_calculate_percent_sales_from_most_frequent_category_missing_total(self):
        totals = {}
        max_cat = {"Oregon": ("Furniture", 10.0)}
        self.assertEqual(
            calculate_percent_sales_from_most_frequent_category(totals, max_cat),
            {"Oregon": ("Furniture", 10.0, 0)}
        )

    def test_read_in_superstore_file_exists(self): 
        data = read_in_superstore() 
        self.assertGreater(len(data), 0) 
    def test_read_in_superstore_header(self): 
        data = read_in_superstore() 
        expected_header = [ "Ship Mode", "Segment", "Country", "City", "State", "Postal Code", "Region",
        "Category", "Sub-Category", "Sales", "Quantity", "Discount", "Profit"] 
        self.assertEqual(data[0], expected_header)

    def test_read_in_superstore_empty_file(self):
        data = read_in_superstore("testfile.csv")
        self.assertEqual(data, [])
    
    def test_read_in_superstore_whitespace_only(self):
        data = read_in_superstore("testfile.csv")
        self.assertEqual(data, [])

    def test_write_to_csv_general_single(self):
        filename = "test_output.csv"
        state_avg = {"California": 55.316}
        state_freq = {"California": ("Furniture", 261.96, 94.714)}
        write_to_csv(filename, state_avg, state_freq)
        with open(filename, newline="") as f:
            rows = list(csv.reader(f))
        self.assertEqual(rows[0], [
            "State", "Average Sale Price", "Most Frequent Category",
            "Sales from Most Frequent Category", "Percentage of Total Sales from Most Frequent Category"
        ])
        self.assertEqual(rows[1], ["California", "55.316", "Furniture", "261.96", "94.714"])
        os.remove(filename)

    def test_write_to_csv_general_multiple(self):
        filename = "test_output.csv"
        state_avg = {"California": 55.316, "Texas": 30.0}
        state_freq = {"California": ("Furniture", 261.96, 94.714), "Texas": ("Technology", 100.0, 66.667)}
        write_to_csv(filename, state_avg, state_freq)
        with open(filename, newline="") as f:
            body = {r[0]: r for r in list(csv.reader(f))[1:]}
        self.assertEqual(body["California"], ["California", "55.316", "Furniture", "261.96", "94.714"])
        self.assertEqual(body["Texas"],      ["Texas",      "30.0",   "Technology","100.0",  "66.667"])
        os.remove(filename)

    def test_write_to_csv_edge_empty_averages(self):
        filename = "test_output.csv"
        write_to_csv(filename, {}, {})
        with open(filename, newline="") as f:
            rows = list(csv.reader(f))
        self.assertEqual(len(rows), 1)  
        os.remove(filename)

    def test_write_to_csv_edge_missing_freq_defaults(self):
        filename = "test_output.csv"
        state_avg = {"California": 10.0, "Texas": 20.0}  
        state_freq = {"California": ("Tech", 5.0, 50.0)}
        write_to_csv(filename, state_avg, state_freq)
        with open(filename, newline="") as f:
            body = {r[0]: r for r in list(csv.reader(f))[1:]}
        self.assertEqual(body["California"], ["California", "10.0", "Tech", "5.0", "50.0"])
        self.assertEqual(body["Texas"],      ["Texas",      "20.0", "N/A",  "0",   "0"])
        os.remove(filename)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)