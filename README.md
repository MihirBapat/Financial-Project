Gig Cashflow Index (GCI) - AI Credit Scoring MVP
This project is a full-stack Machine Learning application designed to evaluate the creditworthiness of gig workers. 
It replaces traditional credit scores with behavioral finance patterns like income stability, liquidity buffers, and fraud detection.

🛠 Tech Stack
Backend: Python (FastAPI, SQLAlchemy)

AI/ML: Scikit-learn (Isolation Forest & Gradient Boosting)

Database: SQLite

Frontend: React + Vite

💻 Installation & Setup
Follow these steps to get the project running on your local machine:

1. Clone the Project
Bash
git clone <your-repository-link>
cd "Project Based Learning"
2. Set Up the Python Environment
Bash
# Create a virtual environment
python -m venv .venv

# Activate it (Windows)
source .venv/Scripts/activate

# Install required libraries
pip install fastapi uvicorn sqlalchemy pandas numpy scikit-learn faker joblib
3. Initialize the Data & AI Models
You must run these scripts in order to generate the database and train the AI "brain":

Bash
# Generate 200k+ transactions
python scripts/generate_transactions.py

# Clean the data
python scripts/clean_dataset.py

# Build financial features
python ml/features/feature_engineering.py

# Run Fraud/Anomaly Detection
python ml/anomaly/manipulation_detector.py

# Train the Default Prediction Model
python ml/training/train_pd_model.py

# Calculate the final 300-900 GCI scores
python ml/training/gci_score.py
4. Start the Backend (Waiter)
Bash
uvicorn backend.api.main:app --reload
Your API is now live at http://localhost:8000/docs

5. Start the Frontend (Dashboard)
Open a new terminal window, then:

Bash
cd frontend
npm install
npm run dev
Open your browser to the link shown (usually http://localhost:5173)

🔍 How to Use the Dashboard
Once the React app opens, you will see a search box.

Enter a Borrower ID (e.g., B_0001, B_0042, or B_0150).

Click Fetch Score to see the AI's real-time evaluation of that gig worker's creditworthiness.

📁 Project Structure
backend/: FastAPI server and Database logic.

ml/: The Machine Learning "brains" (Anomaly detection & Risk modeling).

data/: Where the transaction and score CSVs are stored.

frontend/: The React code for the user interface.

Important Note for Collaborators
If you run into "Module Not Found" errors, ensure your .venv is activated.
If the Dashboard shows an error, make sure the Uvicorn server is running in a separate terminal!
