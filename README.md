# 🏡 AI-Powered Smart House Recommendation System — Production ML Project

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Status](https://img.shields.io/badge/Status-Production-brightgreen)
![ML](https://img.shields.io/badge/ML-Hybrid%20Recommendation-orange)
![Backend](https://img.shields.io/badge/Backend-FastAPI-green)
![AI](https://img.shields.io/badge/AI-Explainable-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Project Overview

The **AI-Powered Smart House Recommendation System** is a production-level machine learning application that recommends houses based on user preferences such as price range, location, and bedroom requirements.

The system uses a **Hybrid Recommendation Engine (Content-Based + Collaborative Filtering)** combined with strict filtering, ranking, and explainable AI to deliver personalized recommendations.

This project demonstrates real-world ML system design, backend architecture, and intelligent decision systems.

---

## ⭐ Key Features

✅ Hybrid recommendation system (Content + Collaborative filtering)
✅ Strict preference-based filtering (price, location, bedrooms)
✅ Explainable AI (why each house is recommended)
✅ Real-time recommendation ranking
✅ Model training and retraining pipeline
✅ REST API backend (FastAPI)
✅ Database integration for houses and users
✅ Performance monitoring and logging
✅ Production-ready architecture

---

## 🏗 System Architecture

```
User → FastAPI Backend → Recommendation Engine → Database → Ranked Results
```

### Components

* **User Layer** — provides preferences and requests
* **Backend API** — processes requests and manages data
* **ML Engine** — filters and ranks houses
* **Database** — stores houses, users, and interactions
* **Recommendation Output** — returns ranked results

---

## 🧠 Machine Learning Pipeline

1. Data collection and preprocessing
2. Feature extraction (price, location, bedrooms, behavior)
3. Content-based similarity calculation
4. Collaborative filtering from user interactions
5. Hybrid score computation and ranking
6. Explainable AI output generation

---

## 🔄 System Workflow

```
User Request → Filter Houses → ML Ranking → Score Calculation → Top Recommendations
```

Steps:

* User provides preferences
* System filters matching houses
* Hybrid model ranks houses
* Top results returned with explanation

---

## 📊 Performance Metrics

* Average API response time: ~100–200 ms
* Model training time: ~few seconds (depends on dataset)
* Recommendation ranking complexity: O(n log n)
* Scalable architecture for large datasets

---

## 🧪 Testing & Validation

* Unit testing for API endpoints
* Input validation and error handling
* Data validation checks
* Secure request handling

---

## ⚙️ Tech Stack

* Python
* FastAPI
* Scikit-learn
* Pandas / NumPy
* SQLite / SQL Database
* REST API
* Docker (optional deployment)

---

## 🚀 How to Run

### Clone Repository

```
git clone <your-repo-url>
cd AI-Powered-Smart-House-Recommendation-System
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Run Backend Server

```
uvicorn apps.backend_api.main:app --reload
```

Open API documentation:

```
http://localhost:8000/docs
```

# 📸 Demo

## Recommendation API

![AI-Powered-Smart-House-Recommendation-System](assets/p1-project.png)
![AI-Powered-Smart-House-Recommendation-System](assets/p2-project.png)
* Returns ranked house recommendations
* Shows explanation for each result
* Provides hybrid recommendation score

## User Preference Filtering
![AI-Powered-Smart-House-Recommendation-System](assets/p3-project.png)
![AI-Powered-Smart-House-Recommendation-System](assets/p4-project.png)
* Filter by price range
* Filter by location
* Filter by bedrooms

## Explainable AI Output
![AI-Powered-Smart-House-Recommendation-System](assets/p5-project.png)
![AI-Powered-Smart-House-Recommendation-System](assets/p6-project.png)
![AI-Powered-Smart-House-Recommendation-System](assets/p7-project.png)
* Shows matching features
* Displays recommendation reason


---

## 📂 Project Structure

```
apps/
 ├── backend_api/        # FastAPI backend and routes
 ├── ml_engine/          # Recommendation engine and training
 └── mobile_app/         # Frontend client (optional)

docs/                    # Documentation
infra/                   # Deployment configuration
models/                  # Saved ML models
```

---

## 🎯 Applications

* Real estate recommendation platforms
* Personalized search systems
* E-commerce recommendation engines
* Intelligent decision support systems

---

## ⚠️ Limitations

* Performance depends on available data
* Cold-start problem for new users
* Recommendation quality improves with user interactions

---

## 🚀 Future Improvements

* Cloud deployment (AWS / GCP)
* Deep learning recommendation models
* Real-time analytics dashboard
* Large-scale distributed training

---

## 👨‍💻 Author

**Hemanth Gudi**
Computer Science Student | Full Stack Developer | Machine Learning Enthusiast
