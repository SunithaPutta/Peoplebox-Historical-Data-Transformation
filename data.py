import csv
from datetime import datetime, timedelta

# Function to read input CSV file
def read_csv(file_path):
    data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            data.append(row)
    return data

# Function to write transformed data into a new CSV file
def write_csv(data, file_path):
    fieldnames = ['Employee Code', 'Manager Employee Code', 'Last Compensation', 'Compensation', 
                  'Last Pay Raise Date', 'Variable Pay', 'Tenure in Org', 'Performance Rating', 
                  'Engagement Score', 'Effective Date', 'End Date']
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Function to transform the data
def transform_data(input_data):
    transformed_data = []

    for employee in input_data:
        # Determine effective and end dates
        start_date = datetime.strptime(employee['Date of Joining'], '%Y-%m-%d')
        end_date = datetime.strptime(employee['Date of Exit'], '%Y-%m-%d') if employee['Date of Exit'] else datetime(2100, 1, 1)

        # Compensation
        compensation_dates = [datetime.strptime(employee['Compensation 1 date'], '%Y-%m-%d'), 
                              datetime.strptime(employee['Compensation 2 date'], '%Y-%m-%d')]
        compensation_values = [employee['Compensation 1'], employee['Compensation 2']]

        # Review
        review_dates = [datetime.strptime(employee['Review 1 date'], '%Y-%m-%d'), 
                        datetime.strptime(employee['Review 2 date'], '%Y-%m-%d')]
        review_values = [employee['Review 1'], employee['Review 2']]

        # Engagement
        engagement_dates = [datetime.strptime(employee['Engagement 1 date'], '%Y-%m-%d'), 
                            datetime.strptime(employee['Engagement 2 date'], '%Y-%m-%d')]
        engagement_values = [employee['Engagement 1'], employee['Engagement 2']]

        # Create historical records
        for i in range(len(compensation_dates)):
            record = {
                'Employee Code': employee['Employee Code'],
                'Manager Employee Code': employee['Manager Employee Code'],
                'Last Compensation': compensation_values[i - 1] if i > 0 else '',
                'Compensation': compensation_values[i],
                'Last Pay Raise Date': compensation_dates[i - 1].strftime('%Y-%m-%d') if i > 0 else '',
                'Variable Pay': '',
                'Tenure in Org': '',
                'Performance Rating': review_values[i],
                'Engagement Score': engagement_values[i],
                'Effective Date': compensation_dates[i].strftime('%Y-%m-%d'),
                'End Date': (compensation_dates[i + 1] - timedelta(days=1)).strftime('%Y-%m-%d') if i < len(compensation_dates) - 1 else end_date.strftime('%Y-%m-%d'),
            }
            transformed_data.append(record)

    return transformed_data

# Main function
if __name__ == "__main__":
    input_file = 'input_data.csv'
    output_file = 'output_data.csv'

    input_data = read_csv(input_file)
    transformed_data = transform_data(input_data)
    write_csv(transformed_data, output_file)

    print("Transformation complete. Output saved to:", output_file)
