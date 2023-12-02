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
   git clone https://github.com/adekingsley/tad.git
   cd your-project
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**

   ```bash
   flask run --port=5001
   ```

4. **Run the API from postman or curl: by sending a post request to the url below containing the opay bank statement in pdf with a key file**
   
- **Endpoint:** `/upload`
  - **Method:** `POST`
   ```bash
   flask run --port=5001/upload
   ```

   The application should be running at `http://localhost:5001/`.

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
- **Analyse your account**

  - **Endpoint:** `/analyse`
  - **Method:** `GET`
  - **Description:** analyse your account using chats this can enable you to have a clear picture of your income/expenditure and salary consistency.
  - **Parameters:**
    - None
  - **Response:**
    - **Example Request:**
    ```bash
    curl http://localhost:5000/analyse
    ```

### Usage

f the code breaks during analysis please exit the server and restart your local server again.

### Dependencies

here are the used dependencies 
Flask==3.0.0
PyPDF2==3.0.1
python-dateutil==2.8.2
matplotlib==3.8.2
numpy==1.26.2
etc. please do open the requirements for more details

### Contributing

If you'd like to contribute to this project, please follow these guidelines.

1. Fork the repository.
2. Create a new branch.
3. Make your changes.
4. Test your changes.
5. Submit a pull request.
