from flask import jsonify
import base64
from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import csv
import re
import PyPDF2
import pandas as pd
from io import BytesIO

app = Flask(__name__)


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text


@app.route('/upload', methods=['POST'])
def upload_pdf():
    try:
        # Check if the 'file' key is in the request files
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        pdf_file = request.files['file']

        # Check if the file has a PDF extension
        if not pdf_file.filename.lower().endswith('.pdf'):
            return jsonify({'error': 'Invalid file format, only PDF files are accepted'}), 400

        # Save the PDF file temporarily
        pdf_path = 'temp.pdf'
        pdf_file.save(pdf_path)

        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_path)

        # Implement logic to parse and extract relevant data from the text
        data = []
        matches = re.finditer(
            r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).*?(\w+).*?([+-]?\d+\.\d{2})\s+(\S+)', pdf_text)
        for match in matches:
            date, debit_type, amount, counter_party = match.groups()
            data.append({'Date': date, 'Debit Type': debit_type,
                        'Amount': amount, 'Counter Party': counter_party})

        # Creating a DataFrame from the extracted data
        df = pd.DataFrame(data)

        # Save the extracted data to a CSV file
        csv_path = 'output.csv'
        df.to_csv(csv_path, index=False)

        return jsonify({'success': 'File processed successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/analyze')
def analyze_data():
    try:
        # Read CSV data
        df = pd.read_csv('output.csv')

        df['Date'] = pd.to_datetime(df['Date'])

        # Separating 'Amount' into 'Credit' and 'Debit' columns
        df['Credit'] = df['Amount'].apply(lambda x: x if x > 0 else 0)
        df['Debit'] = df['Amount'].apply(lambda x: -x if x < 0 else 0)

        # Extract the month from the 'Date' column
        df['Month'] = df['Date'].dt.to_period('M')

        # Grouping the data by month and calculate monthly income and expenditure
        monthly_income = df.groupby('Month')['Credit'].sum()
        monthly_expenditure = df.groupby('Month')['Debit'].sum()

        monthly_income.plot(kind='bar', xlabel='Month',
                            ylabel='Total Income', title='Monthly Income Analysis')
        plt.show()

        monthly_expenditure.plot(kind='bar', xlabel='Month', ylabel='Total Expenditure',
                                 title='Monthly Expenditure Analysis', color='red')
        plt.show()

        # Calculate the total debit for each debit type
        total_debits = df[df['Debit'] != 0].groupby('Debit Type')[
            'Debit'].sum()

        # Pie chart for total debits
        plt.figure(figsize=(8, 8))
        total_debits.plot.pie(autopct='%1.1f%%', startangle=90)
        plt.title("Total Debits Across All Months")
        plt.show()

        # calculate for credit
        total_credit = df[df['Credit'] != 0].groupby('Debit Type')[
            'Credit'].sum()

        # Pie chart for total debits
        plt.figure(figsize=(8, 8))
        total_credit.plot.pie(autopct='%1.1f%%', startangle=90)
        plt.title("Total Cresits Across All Months")
        plt.show()

        # Grouping entire debit into most common debits and others
        common_debits = df['Debit Type'].value_counts().nlargest(
            3).index.tolist()
        df['DebitType'] = df['Debit Type'].apply(
            lambda x: x if x in common_debits else 'Others')

        # Calculate the total debit for each debit type
        total_debits = df[df['Debit'] != 0].groupby('Debit Type')[
            'Debit'].sum()
        total_credit = df[df['Credit'] != 0].groupby('Debit Type')[
            'Credit'].sum()

        # Save plots to BytesIO object
        income_plot = BytesIO()
        monthly_income.plot(kind='bar', xlabel='Month',
                            ylabel='Total Income', title='Monthly Income Analysis')
        plt.savefig(income_plot, format='png')
        income_plot.seek(0)
        income_plot_encoded = base64.b64encode(
            income_plot.getvalue()).decode('utf-8')

        expenditure_plot = BytesIO()
        monthly_expenditure.plot(kind='bar', xlabel='Month', ylabel='Total Expenditure',
                                 title='Monthly Expenditure Analysis', color='red')
        plt.savefig(expenditure_plot, format='png')
        expenditure_plot.seek(0)
        expenditure_plot_encoded = base64.b64encode(
            expenditure_plot.getvalue()).decode('utf-8')

        debits_plot = BytesIO()
        total_debits.plot.pie(autopct='%1.1f%%', startangle=90)
        plt.title("Total Debits Across All Months")
        plt.savefig(debits_plot, format='png')
        debits_plot.seek(0)
        debits_plot_encoded = base64.b64encode(
            debits_plot.getvalue()).decode('utf-8')

        credit_plot = BytesIO()
        total_credit.plot.pie(autopct='%1.1f%%', startangle=90)
        plt.title("Total Credit Across All Months")
        plt.savefig(credit_plot, format='png')
        credit_plot.seek(0)
        credit_plot_encoded = base64.b64encode(
            credit_plot.getvalue()).decode('utf-8')

        # Close the figure objects
        plt.clf()
        plt.close('all')

        return render_template('analysis.html', income_plot=income_plot_encoded,
                               expenditure_plot=expenditure_plot_encoded,
                               debits_plot=debits_plot_encoded,
                               credit_plot=credit_plot_encoded)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/calculate_loan')
def calculate_loan():
    try:
        df = pd.read_csv('output.csv')
        # to filter the credit from the debit
        df['Credit'] = df['Amount'].apply(lambda x: x if x > 0 else 0)
        df['Debit'] = df['Amount'].apply(lambda x: -x if x < 0 else 0)

        # Filtering rows with "MobileData" and "Bouns" out
        filtered_df = df[(df['Debit Type'] != 'MobileData')
                         & (df['Debit Type'] != 'Bouns')]
        filtered_df = filtered_df.drop(['Debit Type'], axis=1)

        # Assuming 'Date' is a datetime column
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

        # Calculate the total number of months
        total_months = (filtered_df['Date'].dt.to_period(
            "M").max() - filtered_df['Date'].dt.to_period("M").min()).n + 1

        # Assuming 'Credit' is the transaction amount
        salary_threshold = 50000
        consistency_threshold = total_months - 1

        # Group by month and count the number of months with transactions greater than or equal to the threshold
        consistent_salary_months = filtered_df.groupby(filtered_df['Date'].dt.to_period("M")).apply(
            lambda x: (x['Credit'] >= salary_threshold).any())

        # Count the number of consistent months
        consistent_months_count = consistent_salary_months.sum()

        if consistent_months_count >= consistency_threshold:
            response_message = f"User consistently receives a salary in at least {consistency_threshold} months."
            salary_consistent = True
        else:
            response_message = "User does not consistently receive a salary."
            salary_consistent = False

        def calculate_loan_amount(monthly_income, salary_consistent):
            loan_percentage = 0.2  # 30% of monthly income
            loan_term_months = 11  # Loan term in months

            # Adjust loan percentage for users who consistently receive a salary
            if salary_consistent:
                loan_percentage = 0.5

            loan_amount = loan_percentage * monthly_income * loan_term_months
            return loan_amount

        # Extract the month from the 'Date' column
        filtered_df['Month'] = filtered_df['Date'].dt.to_period('M')
        monthly_income = filtered_df.groupby('Month')['Credit'].sum()

        # Find the month with the lowest monthly income
        lowest_month = monthly_income.idxmin()
        lowest_month_income = monthly_income[lowest_month]

        print(
            f"The month with the lowest monthly income is: {lowest_month}, with income: {lowest_month_income:.2f}")

        # Using the identified lowest month for the loan calculation
        loan_amount_for_lowest_month = calculate_loan_amount(
            lowest_month_income, salary_consistent)

        # Round the loan amount to the nearest thousand
        rounded_loan_amount = round(loan_amount_for_lowest_month, -3)

        # Return loan amount as a JSON response along with other information
        json_response = {'loan_amount': rounded_loan_amount,
                         'message': response_message, 'salary_consistent': salary_consistent}

        return jsonify(json_response)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
