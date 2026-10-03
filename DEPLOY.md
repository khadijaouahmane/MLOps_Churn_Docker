# Déploiement Heroku (2 apps, 1 dépôt)

Architecture : **Navigateur → Flask (front) → FastAPI (API) → modèle `.pkl`**

```bash
git init && git add . && git commit -m "ChurnGuard"
heroku login

# 1) L'API (seule à charger le modèle)
heroku create churn-api-<votre-nom>
heroku config:set APP_ROLE=api -a churn-api-<votre-nom>
git push heroku main

# 2) L'interface
heroku create churn-front-<votre-nom>
heroku config:set APP_ROLE=front API_URL=https://churn-api-<votre-nom>.herokuapp.com -a churn-front-<votre-nom>
git remote add front https://git.heroku.com/churn-front-<votre-nom>.git
git push front main
```

Notes : `heroku open -a churn-front-<votre-nom>` ouvre l'interface ; la doc Swagger de l'API est sur `/docs`.
Après `git push heroku main`, vérifiez que `heroku` pointe bien vers l'API (`git remote -v`).
Test local : `uvicorn api.main:app --port 8000` puis `python -m flask_app.app`.
