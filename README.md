# MEDITRACK-INTERACTIVE-PATIENT-CARE-DASHBOARD
Build an interactive Streamlit dashboard. Provide real-time insights on patient demographics, prescriptions, lab results, and chronic disease burden. Support data-driven decision making to improve patient care, adherence, and diagnostic efficiency.
_______________________________________
🚀 Features
🔹 Home Page
•	Displays a summary of key metrics:
o	Total patients
o	Average age
o	Average BMI
o	Average adherence %
•	Includes a Patient Lookup tool for quick patient-specific details.
•	Footer with contact information.
🔹 Dashboard Page
•	Interactive visualizations with filters for city, state, and gender.
•	Includes:
o	Age & Drug Analysis (bar charts showing patient demographics vs. prescribed drug categories)
o	Patient Distribution & Demographics (state vs. city heatmap and gender ratio donut chart)
•	Customizable visualization themes (Plotly, Seaborn, Simple White).
🔹 Prescription Insights
•	Insights into prescribing trends with:
o	Top 10 prescribed drug categories
o	Branded vs Generic distribution (donut chart)
o	Doctor vs Prescription volume (heatmap)
o	Adherence percentage trend over time
o	Refill completion vs missed statistics
•	Filter options for Doctor and Drug Category.
🔹 Lab & Chronic Insights
•	Focused view on chronic disease and lab metrics:
o	Chronic disease prevalence (stacked bar)
o	Average HbA1c trends (for diabetic monitoring)
o	Hypertension control rate (% controlled vs uncontrolled)
o	Lab turnaround time (gauge meter)
o	Pareto chart for most frequently ordered tests
o	Key performance indicators (e.g., HbA1c > 7%, LDL > 130 mg/dL)
🔹 About Me
•	Displays developer details:
o	Name: A. Sirisha
o	Reg No: 321002
o	College: Shri Vishnu College of Pharmacy
o	Contact: 321002@svcp.edu.in
•	Brief overview of the MediTrack project purpose and functionality.
________________________________________
🧰 Tech Stack
Component	Technology
Frontend	Streamlit
Backend	Python
Data Visualization	Plotly, Matplotlib, Seaborn
Data Handling	Pandas
Environment	Jupyter / Streamlit Cloud / Localhost
________________________________________
⚙️ Installation & Setup
🪜 Prerequisites
•	Python 3.8+
•	pip (Python package manager)
📦 Required Libraries
Install all dependencies:
pip install streamlit pandas matplotlib plotly seaborn
create the folder structure by downloading the files
FOLDER STRUCTURE:
MediTrackApp/
│
├── app.py                        # Main entry point for the Streamlit app
├── utils.py                      # Helper functions and configurations
│
├── pages/                        # Contains different dashboard modules
│   ├── home.py                   # Home page with overview and patient search
│   ├── dashboard_page.py         # Visual analytics dashboard
│   ├── prescription_insights.py  # Prescription analytics and trends
│   ├── lab_chronic_insights.py   # Lab and chronic disease data visualization
│   └── about.py                  # Developer and project information page
│
├── assets/                       # Folder for static files and media
│   └── my_pics.jpg               # Copy your profile image here
│
└── README.md                     # Project documentation file

▶️ Run the Application 
streamlit run app.py
🌐 Access
After launching, open your browser at:
http://localhost:8501
________________________________________
📊 Data Inputs
MediTrack uses de-identified patient data for:
•	Demographics (Age, Gender, City, State)
•	Prescription records (Drug category, Branded/Generic type)
•	Lab results (HbA1c, LDL, BP readings)
•	Chronic condition tracking
(Sample datasets can be integrated in CSV format for demonstration or research use.)
________________________________________
🧩 Dashboard Modules Summary
Page	Key Visuals	Purpose
Home	KPI cards, Patient search	Overview & quick lookup
Dashboard	Age vs Drug, Demographics heatmap	Population-level analysis
Prescription Insights	Drug trends, Branded vs Generic, Adherence	Prescribing behavior insights
Lab & Chronic Insights	Lab KPIs, Control rates, Pareto chart	Disease monitoring & operational efficiency
About Me	Profile and project info	Project background
________________________________________
🧠 Insights Generated
•	Identify most prescribed drug categories.
•	Compare Branded vs Generic usage patterns.
•	Monitor chronic disease control metrics (e.g., BP, HbA1c).
•	Evaluate doctor performance via prescription heatmaps.
•	Track patient adherence trends and lab efficiency.
________________________________________
🧑‍💻 Author
A. Sirisha
Doctor of pharmacy Student
Shri Vishnu College of Pharmacy
📧 Contact: 321002@svcp.edu.in
