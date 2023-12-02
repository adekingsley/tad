# Tad

### Project Description

Tad test is a breif test AI machine learning work that can analyse, charatersize and predict loan creditworthiness 

### Table of Contents

- [Setup](#setup)
- [Endpoints](#endpoints)
- [Usage](#usage)
- [Dependencies](#dependencies)
- [Contributing](#contributing)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/adekingsley/Tad_test.git
   cd your-project
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   python app.py
   ```

   The application should be running at `http://localhost:5000/`.

### Endpoints

- **Calculate Loan**

  - **Endpoint:** `/calculate_loan`
  - **Method:** `GET`
  - **Description:** Calculate the eligible loan amount for a user based on their monthly income and salary consistency.
  - **Parameters:**
    - None
  - **Response:**
    - JSON Object:
      ```json
      {
        "loan_amount": 50000,
        "message": "User consistently receives a salary in at least 4 months.",
        "salary_consistent": true
      }
      ```
  - **Example Request:**
    ```bash
    curl http://localhost:5000/calculate_loan
    ```
  - **Example Response:**
    ```json
    {
      "loan_amount": 50000,
      "message": "User consistently receives a salary in at least 4 months.",
      "salary_consistent": true
    }
    ```

### Usage

Provide examples or instructions on how to use your API. Include sample requests and responses.

### Dependencies

List any external libraries or dependencies required to run your project.

### Contributing

If you'd like to contribute to this project, please follow these guidelines.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test your changes.
5. Submit a pull request.
