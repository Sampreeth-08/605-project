# Hotel Booking Demand Prediction with MLOps

This project presents a complete end-to-end MLOps pipeline to predict hotel booking cancellations using the [Hotel Booking Demand Dataset](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand). The system integrates data ingestion, preprocessing, model training, experiment tracking, CI/CD automation, containerization, and cloud deployment.

## 🚀 Features

- Machine learning model to predict booking cancellations
- MLflow for experiment tracking and model versioning
- TensorBoard for performance visualization
- Jenkins-based CI/CD pipeline with Docker and Trivy
- Deployment on AWS ECS with Fargate
- Web interface built with Flask for real-time predictions

---

## 📁 Project Structure

```
605-project/
├── application.py        # Flask web application
├── main.py               # Model training and orchestration script
├── Dockerfile            # Dockerfile for the ML app
├── Jenkinsfile           # Jenkins CI/CD pipeline definition
├── requirements.txt      # Python dependencies
├── config/               # Config files (paths, params, AWS settings)
├── data/                 # Input dataset (ignored in repo)
├── models/               # Saved model artifacts
├── notebooks/            # EDA and experimentation notebooks
├── src/                  # Source code (preprocessing, training, utils)
│   ├── data_ingestion.py
│   ├── feature_engineering.py
│   ├── model_trainer.py
│   └── logger.py
└── README.md             # Project documentation
```

---

## ⚙️ How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/Sampreeth-08/605-project.git
cd 605-project
```

### 2. Set Up Virtual Environment

```bash
python -m venv 605venv
source 605venv/bin/activate  # or use `.ƅvenv\Scriptsctivate` on Windows
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Train the Model

```bash
python main.py
```

### 4. Run the Web App

```bash
python application.py
```

Visit `http://localhost:5000` in your browser.

---

## 🧪 MLOps Stack

| Component           | Tool                          |
|---------------------|-------------------------------|
| Experiment Tracking | MLflow, TensorBoard           |
| CI/CD Automation    | Jenkins (Declarative Pipeline)|
| Containerization    | Docker, DockerHub             |
| Security Scanning   | Trivy                         |
| Deployment          | AWS ECS (Fargate)             |
| Monitoring          | MLflow, CloudWatch (optional) |

---

## 📊 Model Performance

- **Best Model:** CatBoost Classifier  
- **Accuracy:** 99.5%  
- **Tracked Using:** MLflow and TensorBoard

---

## 🧑‍💻 Team Members

- **Sampreeth Jangala** – CI/CD Pipeline, Jenkins, Docker
- **Keshav Naram** – AWS ECS Deployment
- **Pranav Srinivasan** – ML Model Development, Flask API

---

## 📄 License

This project is part of an academic course submission and is intended for educational use.

---

## 📬 Contact

For questions or collaboration, feel free to reach out via [LinkedIn](https://www.linkedin.com/in/sampreethjangala).
