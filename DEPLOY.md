# Déployer l’API FastAPI conteneurisée sur Heroku

Le conteneur embarque l’API FastAPI, l’interface servie sur `/ui` et le pipeline scikit-learn sérialisé. Heroku construit l’image à partir du `Dockerfile` grâce à `heroku.yml`.

## Déploiement sur l’application existante

Depuis la racine du dépôt, avec Heroku CLI connecté :

```bash
heroku stack:set container --app ouahmane-churn-mlops
git add Dockerfile .dockerignore heroku.yml DEPLOY.md
git commit -m "Deploy FastAPI as a Docker image"
git push heroku HEAD:master
```

L’application écoute le port fourni par Heroku (`PORT`). Une fois le déploiement terminé, l’interface est disponible sur `/ui`, la documentation Swagger sur `/docs` et l’état de santé sur `/health`.

## Construction et lancement locaux (Docker installé)

```bash
docker build --platform linux/amd64 -t churn-api .
docker run --rm -p 8000:8000 -e PORT=8000 churn-api
```

L’API locale répond sur `http://localhost:8000`; l’interface est sur `/ui`.
