import csv
from datetime import datetime
from Interface.models import Data,User

def process_csv_file(file_path='static/csv_files/data.csv', name='TerrData', label_index=0, data_index=1):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data_rows = list(reader)

            date_list = []
            balance_list = []

            for row in data_rows:
                # Removing currency sign and ',' from numbers, handling empty values
                cleaned_balance = row[data_index].replace('€', '').replace(',', '').strip()
                if cleaned_balance:
                    try:
                        balance_list.append(float(cleaned_balance))
                    except ValueError:
                        pass  # Skip if conversion fails

                if len(row) > max(label_index, data_index):
                    # Extracting and converting date to the required format
                    cleaned_date = row[label_index].strip()
                    if cleaned_date:
                        try:
                            date_list.append(datetime.strptime(cleaned_date, '%Y-%m-%d').date())
                        except ValueError:
                            pass  # Skip if conversion fails

            # Create or get the user
            user = User.objects.get(username='Jayesh')

            # Create the Data entry
            data_instance = Data.objects.create(
                is_active=True,
                file_field=file_path,
                user=user,
                date_list=date_list,
                balance_list=balance_list,
                name=name
            )
            return f"Data entry created for '{name}' successfully!"

    except Exception as e:
        return f"Error processing file: {e}"
    
process_csv_file()