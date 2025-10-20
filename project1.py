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
    write_to_csv('project_1_output.csv', state_avg_price, state_most_freq_cat_percentage)
    #write to a new csv file with columns "state" "average sale price" "percentage of total sales from most frequent category", using state_avg_price and state_most_freq_cat_percentage dictionaries to get the data

#Write 4 simple test cases for each function above using the unit test framework. Each function should have two tests for general/usua cases, and two edge cases.
class TestSuperstoreCalculations(unittest.TestCase):
    header = [
        "Order ID", "Order Date", "Ship Date", "Ship Mode",
        "State", "Country", "City", "Category", "Sub-Category",
        "Sales", "Quantity"
    ]
    data = [header,
        ["CA-2016-152156", "11/08/16", "11/11/16", "Second Class", "California", "United States", "Los Angeles", "Furniture",        "Bookcases",      "261.96", "2"],
        ["CA-2016-152157", "11/08/16", "11/11/16", "Second Class", "California", "United States", "Los Angeles", "Office Supplies",  "Labels",         "14.62",  "3"],
        ["TX-2017-100001", "12/02/17", "12/05/17", "Standard Class","Texas",     "United States", "Houston",     "Technology",       "Phones",         "100.00", "1"],
        ["TX-2017-100002", "12/02/17", "12/05/17", "Standard Class","Texas",     "United States", "Houston",     "Office Supplies",  "Paper",          "50.00",  "4"],
        ["NY-2016-152158", "11/08/16", "11/11/16", "Second Class",  "New York",  "United States", "New York City","Technology",      "Phones",         "957.58", "5"],
    ]

    data_header_only = [header]

    data_all_zero = [header,
     ["NV-2018-200001", "03/14/18", "03/17/18", "First Class", "Nevada", "United States", "Reno", "Furniture",  "Tables",      "0", "0"],
     ["NV-2018-200002", "03/14/18", "03/17/18", "First Class", "Nevada", "United States", "Reno", "Technology", "Accessories", "0", "0"],
    ]

    data_tie = [header, 
        ["GA-2020-600001", "02/18/20", "02/21/20", "Second Class", "Georgia", "United States", "Atlanta", "Furniture",  "Tables", "60", "1"],
        ["GA-2020-600002", "02/18/20", "02/21/20", "Second Class", "Georgia", "United States", "Atlanta", "Technology", "Phones", "60", "1"],
    ]       

    # ---------------- get_num_sales_per_state ----------------
    # General 1: full base data
    def test_get_num_sales_per_state_general(self):
        result = get_num_sales_per_state(self.data)
        self.assertEqual(result, {"California": 5, "Texas": 5, "New York": 5})

    # General 2: subset using only CA + TX rows (reused data, no new rows)
    def test_get_num_sales_per_state_general_subset(self):
        subset = [self.header] + self.data[1:5]  # CA rows + TX rows
        result = get_num_sales_per_state(subset)
        self.assertEqual(result, {"California": 5, "Texas": 5})

    # Edge 1: header only
    def test_get_num_sales_per_state_header_only(self):
        self.assertEqual(get_num_sales_per_state(self.data_header_only), {})

    # Edge 2: all zero quantities
    def test_get_num_sales_per_state_all_zero(self):
        self.assertEqual(get_num_sales_per_state(self.data_all_zero), {"Nevada": 0})

    # ---------------- total_sales_per_state ----------------
    # General 1: full base data
    def test_total_sales_per_state_general(self):
        result = total_sales_per_state(self.data)
        self.assertEqual(result, {"California": 276.58, "Texas": 150.00, "New York": 957.58})

    # General 2: subset using only CA + TX rows (reused data)
    def test_total_sales_per_state_general_subset(self):
        subset = [self.header] + self.data[1:5]  # CA rows + TX rows
        result = total_sales_per_state(subset)
        self.assertEqual(result, {"California": 276.58, "Texas": 150.00})

    # Edge 1: header only
    def test_total_sales_per_state_header_only(self):
        self.assertEqual(total_sales_per_state(self.data_header_only), {})

    # Edge 2: all zero sales
    def test_total_sales_per_state_all_zero(self):
        self.assertEqual(total_sales_per_state(self.data_all_zero), {"Nevada": 0.0})

    # ---------------- calculate_average_sale_price_per_state ----------------
    # General 1: from full base data
    def test_calculate_average_sale_price_per_state_general(self):
        state_sales = total_sales_per_state(self.data)
        state_counts = get_num_sales_per_state(self.data)
        result = calculate_average_sale_price_per_state(state_sales, state_counts)
        self.assertEqual(result, {"California": 55.316, "Texas": 30.0, "New York": 191.516})

    # General 2: subset CA + TX (reused data)
    def test_calculate_average_sale_price_per_state_general_subset(self):
        subset = [self.header] + self.data[1:5]  # CA rows + TX rows
        sales = total_sales_per_state(subset)
        counts = get_num_sales_per_state(subset)
        result = calculate_average_sale_price_per_state(sales, counts)
        self.assertEqual(result, {"California": 55.316, "Texas": 30.0})

    # Edge 1: zero count for a state (force TX to 0)
    def test_calculate_average_sale_price_per_state_zero_count(self):
        sales = total_sales_per_state(self.data)
        counts = get_num_sales_per_state(self.data)
        counts["Texas"] = 0
        result = calculate_average_sale_price_per_state(sales, counts)
        self.assertEqual(result["Texas"], 0)

    # Edge 2: missing count key -> graceful default 0
    def test_calculate_average_sale_price_per_state_missing_key(self):
        sales = {"Oregon": 12.0}
        counts = {}  # missing key
        result = calculate_average_sale_price_per_state(sales, counts)
        self.assertEqual(result, {"Oregon": 0})

    # ---------------- state_freq_cat_sales ----------------
    # General 1: full base data
    def test_state_freq_cat_sales_general(self):
        result = state_freq_cat_sales(self.data)
        self.assertEqual(
            result,
            {"California": ("Furniture", 261.96), "Texas": ("Technology", 100.0), "New York": ("Technology", 957.58)}
        )

    # General 2: subset TX-only (reused rows)
    def test_state_freq_cat_sales_general_subset(self):
        subset_tx = [self.header] + self.data[3:5]  # the two TX rows only
        result = state_freq_cat_sales(subset_tx)
        self.assertEqual(result, {"Texas": ("Technology", 100.0)})

    # Edge 1: tie case (keeps first encountered)
    def test_state_freq_cat_sales_tie_first_encountered(self):
        self.assertEqual(state_freq_cat_sales(self.data_tie), {"Georgia": ("Furniture", 60.0)})

    # Edge 2: header only
    def test_state_freq_cat_sales_header_only(self):
        self.assertEqual(state_freq_cat_sales(self.data_header_only), {})

    # ---------------- calculate_percent_sales_from_most_frequent_category ----------------
    # General 1: from full base data
    def test_calculate_percent_sales_from_most_frequent_category_general(self):
        totals = total_sales_per_state(self.data)
        max_cat = state_freq_cat_sales(self.data)
        result = calculate_percent_sales_from_most_frequent_category(totals, max_cat)
        self.assertEqual(result["California"], ("Furniture", 261.96, 94.714))
        self.assertEqual(result["Texas"], ("Technology", 100.0, 66.667))
        self.assertEqual(result["New York"], ("Technology", 957.58, 100.0))

    # General 2: subset TX-only (reused rows)
    def test_calculate_percent_sales_from_most_frequent_category_general_subset(self):
        subset_tx = [self.header] + self.data[3:5]
        totals = total_sales_per_state(subset_tx)          # {"Texas": 150.0}
        max_cat = state_freq_cat_sales(subset_tx)          # {"Texas": ("Technology", 100.0)}
        result = calculate_percent_sales_from_most_frequent_category(totals, max_cat)
        self.assertEqual(result, {"Texas": ("Technology", 100.0, 66.667)})

    # Edge 1: zero total -> 0%
    def test_calculate_percent_sales_from_most_frequent_category_zero_total(self):
        totals = {"Nevada": 0.0}
        max_cat = {"Nevada": ("Technology", 0.0)}
        self.assertEqual(
            calculate_percent_sales_from_most_frequent_category(totals, max_cat),
            {"Nevada": ("Technology", 0.0, 0)}
        )

    # Edge 2: missing total key -> graceful 0%
    def test_calculate_percent_sales_from_most_frequent_category_missing_total(self):
        totals = {}
        max_cat = {"Oregon": ("Furniture", 10.0)}
        self.assertEqual(
            calculate_percent_sales_from_most_frequent_category(totals, max_cat),
            {"Oregon": ("Furniture", 10.0, 0)}
        )

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)