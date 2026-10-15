\# 🎯 MLOps Churn — API FastAPI conteneurisée



Prédiction du \*\*churn client\*\* (attrition) via un modèle scikit-learn, exposé avec \*\*FastAPI\*\*, conteneurisé avec \*\*Docker\*\* et déployé en production sur \*\*Heroku\*\*.



!\[Python](https://img.shields.io/badge/Python-3.12-blue)

!\[FastAPI](https://img.shields.io/badge/FastAPI-0.142-009688)

!\[Docker](https://img.shields.io/badge/Docker-container-2496ED)

!\[Heroku](https://img.shields.io/badge/Heroku-deployed-430098)



\---



\## 🔗 Application en ligne



| Service | URL |

|---|---|

| Interface web | https://ouahmane-churn-mlops.herokuapp.com/ui |

| Swagger (docs) | https://ouahmane-churn-mlops.herokuapp.com/docs |

| Health check | https://ouahmane-churn-mlops.herokuapp.com/health |



> ⏱️ Le plan gratuit Heroku met le conteneur en veille après 30 min d'inactivité. Le premier accès peut prendre \~15 s (cold start).



\---



\## 🏗️ Architecture



```

&#x20; Client (navigateur)

&#x20;       │

&#x20;       ▼

&#x20; ┌─────────────────┐

&#x20; │  Heroku dyno    │

&#x20; │  ┌───────────┐  │

&#x20; │  │  Docker   │  │

&#x20; │  │  FastAPI  │──┼──►  /ui       (interface)

&#x20; │  │  Uvicorn  │  │     /docs     (Swagger)

&#x20; │  │           │  │     /health   (santé)

&#x20; │  │  model.pkl│  │     /predict  (inférence)

&#x20; │  └───────────┘  │

&#x20; └─────────────────┘

```



\---



\## 📂 Structure du projet



```

MLOps\_Churn\_Docker/

├── api/                    # Code FastAPI (routes, modèles Pydantic)

│   └── main.py

├── model/                  # Pipeline scikit-learn sérialisé (.pkl)

├── flask\_app/              # Templates et assets servis sur /ui

│   ├── templates/

│   └── static/

├── Dockerfile              # Image Docker de l'API

├── heroku.yml              # Config de déploiement Heroku (stack container)

├── .dockerignore           # Exclusions du contexte Docker

├── requirements.txt        # Dépendances Python

├── DEPLOY.md               # Guide de déploiement détaillé

└── README.md               # Ce fichier

```



\---



\## 🚀 Endpoints de l'API



| Route | Méthode | Description |

|---|---|---|

| `/` | GET | Page d'accueil / redirection |

| `/ui` | GET | Interface web de prédiction |

| `/docs` | GET | Documentation Swagger auto-générée |

| `/health` | GET | Vérification d'état (health check) |

| `/predict` | POST | Prédiction de churn (JSON) |



\### Exemple de requête



```bash

curl -X POST https://ouahmane-churn-mlops.herokuapp.com/predict \\

&#x20; -H "Content-Type: application/json" \\

&#x20; -d '{"tenure":12,"MonthlyCharges":70.5,"TotalCharges":850}'

```



\---



\## 🛠️ Stack technique



\- \*\*Modèle\*\* : scikit-learn (classification binaire)

\- \*\*API\*\* : FastAPI + Uvicorn (ASGI)

\- \*\*Interface\*\* : HTML / CSS / JS servis sur `/ui`

\- \*\*Conteneur\*\* : Docker (`python:3.12-slim`)

\- \*\*Déploiement\*\* : Heroku Container Registry + `heroku.yml`



\---



\## 💻 Lancer en local



\### Option 1 — Avec Docker (recommandé)



```bash

\# Construire l'image (amd64 pour compat Heroku / Mac M1)

docker build --platform linux/amd64 -t churn-api .



\# Lancer le conteneur

docker run --rm -p 8000:8000 -e PORT=8000 churn-api

```



→ API sur http://localhost:8000 · Interface sur http://localhost:8000/ui



\### Option 2 — Sans Docker (Python local)



```bash

python -m venv .venv

.venv\\Scripts\\activate          # Windows

pip install -r requirements.txt

uvicorn api.main:app --host 0.0.0.0 --port 8000

```



\---



\## ☁️ Déploiement sur Heroku



```bash

\# 1. Définir la stack container

heroku stack:set container --app ouahmane-churn-mlops



\# 2. Connecter le remote Heroku (une seule fois)

heroku git:remote --app ouahmane-churn-mlops



\# 3. Pousser (Heroku rebuild l'image automatiquement)

git push heroku HEAD:master



\# 4. Suivre les logs

heroku logs --tail --app ouahmane-churn-mlops

```



Voir \[`DEPLOY.md`](./DEPLOY.md) pour le détail complet.



\---



\## 👤 Auteur



\*\*K. Ouahmane\*\* — Projet MLOps

📧 khadijaouahmane13@gmail.com



\---



\## 📄 Licence



Projet académique — usage pédagogique.

