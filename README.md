🎓 FindMyStress – Student Stress Predictor

FindMyStress is a machine learning–powered web application built with Django, HTML, and CSS that helps students identify their stress levels — whether they’re experiencing Eustress (Positive Stress), Distress (Negative Stress), or No Stress.
The project aims to promote mental health awareness and help students take early steps toward managing stress effectively.

Features

🧠 ML Model Integration – Predicts stress type using a trained Support Vector Machine (SVM) model.

🎨 Interactive Frontend – Beautifully designed using HTML, CSS, and responsive styling.

💬 AI Chat Assistant – Gemini-powered chatbot offering motivational tips and coping strategies.

📊 Comprehensive Survey – Collects psychological and lifestyle data from students (1–5 scale).

⚙️ Django Backend – Handles ML inference, form submissions, and chat integration.

🧾 Dynamic Results Display – Shows prediction result, confidence score, and stress-specific advice.

 Tech Stack
Category	Technologies Used
Frontend	HTML, CSS
Backend	Django (Python)
Machine Learning	scikit-learn, joblib, numpy, pandas
AI Assistant	Google Gemini API
Deployment (optional)	Render / Heroku / PythonAnywhere

Project Structure
```bash
student_stress_predictor/
│
├── predictor/
│   ├── templates/predictor/
│   │   ├── landing.html
│   │   ├── survey.html
│   │   └── chat.html
│   ├── static/css/style.css
│   ├── ml_model/trained_model.joblib
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── manage.py
└── requirements.txt
```
Installation & Setup

Clone this repository
```bash
git clone https://github.com/<your-username>/student-stress-predictor.git
cd student-stress-predictor
```
Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate     # on Windows
source venv/bin/activate  # on macOS/Linux
```

Install dependencies

```bash
pip install -r requirements.txt
```

Add your Gemini API key
Create a .env file in the root folder:

```bash
GEMINI_API_KEY=your_api_key_here
```

Run the server

```bash
python manage.py runserver
```

Open in browser

http://127.0.0.1:8000/

📊 Machine Learning Model

Trained on a student stress dataset (Kaggle).

Target variable encoded as:

0 → Distress

1 → Eustress

2 → No Stress

Preprocessing: Standard Scaling + Label Encoding + PCA (if applied).

Algorithm used: Support Vector Machine (SVM).

Model stored as trained_model.joblib and loaded dynamically in Django views.

🧠 Example Output
| Input                              | Predicted Stress Type | Confidence |
| ---------------------------------- | --------------------- | ---------- |
| Age: 20, Male, High workload       | Distress              | 89.3%      |
| Age: 19, Female, Moderate workload | Eustress              | 78.5%      |
| Age: 21, Male, Balanced life       | No Stress             | 92.1%      |

💬 Chat Assistant (Bonus)

After prediction, students can chat with StressLess an AI stress assistant that provides:

Motivational quotes

Relaxation and time management tips

Stress reduction techniques

Powered by Gemini Generative AI API.

📸 Screenshots



<img width="1366" height="641" alt="landing page" src="https://github.com/user-attachments/assets/eb00ebee-eac4-42d7-8d7c-e79aec728ccc" />

<img width="1343" height="614" alt="Predict!" src="https://github.com/user-attachments/assets/45d5d1ec-92f6-4c05-aa28-448be181e303" />

<img width="1356" height="622" alt="Chatbot StressLess" src="https://github.com/user-attachments/assets/6abc9e95-c62f-4720-832f-df428045882d" />

<img width="1341" height="641" alt="Survey page" src="https://github.com/user-attachments/assets/bc66fb29-d4cd-4527-99c5-a08bec23fa45" />


📜 License


This project is open-source and available under the MIT License
.

👩‍💻 Author

Reshma Thomas
💼 PG Diploma Project – Machine Learning Based Web Application
📫 Feel free to reach out for collaboration or feedback!
