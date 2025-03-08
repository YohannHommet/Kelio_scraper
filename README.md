<div align="center">
  <a href="https://www.docker.com/">
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  </a>
  <a href="https://www.selenium.dev/">
    <img src="https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white" alt="Selenium">
  </a>
  <a href="https://flask.palletsprojects.com/">
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  </a>
</div>

# Scraper d'offres d'emploi Kelio

Ce projet est une application web Flask intégrant un scraper conçu pour extraire les offres d'emploi liées au développement web de la société Kelio. Il utilise des bibliothèques Python telles que `requests`, `BeautifulSoup`, et `Selenium` pour récupérer et analyser les données, et Flask pour présenter les résultats via une interface web.

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Interface Web](#interface-web)
- [Déploiement](#déploiement)
- [Contributions](#contributions)
- [License](#license)

## Fonctionnalités

- Scraping adaptatif (Requests + Selenium)
- Filtrage des offres d'emploi en fonction de mots-clés
- Sauvegarde des résultats dans un fichier CSV
- Notification par email (optionnel)
- Interface web pour consulter les offres d'emploi
- Journalisation détaillée des opérations

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- Python 3.7 ou supérieur
- Chrome et ChromeDriver (pour Selenium)

## Installation

1. **Cloner le dépôt** :
```bash
git clone https://github.com/YohannHommet/scraper.git
cd scraper
```

2. **Créer un environnement virtuel** :
```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
.\venv\Scripts\activate # Windows
```

3. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

## Configuration

1. **Configurer votre fichier `.env`** :
   Créez un fichier `.env` à la racine du projet (si ce n'est pas déjà fait) avec par exemple :

   ```env
   SCRAPER_URL=https://www.bodet.com/fr/nos-offres-d-emploi.html?list%5Bcompany%5D=kelio
   SEND_EMAIL=true
   RESEND_API_KEY=your_resend_api_key
   EMAIL_SENDER=your_verified_sender@yourdomain.com
   EMAIL_RECEIVER=receiver@example.com
   GROQ_API_KEY=your_groq_api_key
   ```

## Utilisation

### Exécution locale

- Pour exécuter le scraper, utilisez la commande suivante :
```bash
python src/core/scraper.py
```

- Pour voir les résultats, ouvrez le fichier `data/jobs.csv`
```bash
cat data/jobs.csv | column -t -s ','
```

- Pour voir les logs, ouvrez le fichier `scraper.log` dans le dossier `logs/scraper.log`
```bash
cat logs/scraper.log | tail -n 10
```

### Exécution avec Docker Compose

- Pour construire et démarrer les conteneurs :
```bash
docker-compose up -d
```

- Pour voir les logs du conteneur scraper :
```bash
docker-compose logs -f scraper
```

- Pour voir les logs du conteneur web :
```bash
docker-compose logs -f web
```

- Pour arrêter les conteneurs :
```bash
docker-compose down
```

## Interface Web

Le projet inclut une interface web pour visualiser les offres d'emploi récupérées.

- Pour démarrer l'interface web en local :
```bash
python src/app.py
```

- Avec Docker Compose, l'interface web est automatiquement disponible à l'adresse : http://localhost:5000

L'interface affiche toutes les offres d'emploi stockées dans le fichier CSV sous forme de cartes avec les informations pertinentes et des liens vers les annonces complètes.

## Déploiement

### Déploiement local avec Docker

Pour déployer l'application localement avec Docker, suivez ces étapes :

1. Construisez l'image Docker :
```bash
docker build -t kelio-app .
```

2. Démarrez le conteneur Docker :
```bash
docker run -d -p 5000:5000 --name kelio-app kelio-app
```

Ou utilisez Docker Compose :
```bash
docker-compose up -d
```

### Déploiement sur Render

L'application est configurée pour être facilement déployée sur [Render](https://render.com) :

1. Créez un compte sur Render si vous n'en avez pas déjà un.

2. Connectez votre dépôt GitHub à Render.

3. Créez un nouveau service Web et sélectionnez votre dépôt.

4. Render détectera automatiquement le fichier `render.yaml` et configurera le service.

5. Configurez les variables d'environnement nécessaires dans l'interface Render :
   - `RESEND_API_KEY` (si vous utilisez les notifications par email)
   - `EMAIL_SENDER` (adresse email d'expédition)
   - `FLASK_SECRET_KEY` (clé secrète pour Flask)
   - `APP_DEBUG` (true/false)

6. Déployez l'application.

Le service déployé sur Render exécutera l'application Flask qui permet d'afficher les offres d'emploi et d'exécuter le scraper à la demande via l'interface web.

## Contributions

Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet, veuillez suivre ces étapes :

1. Forkez le projet.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalite`).
3. Commitez vos modifications (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`).
4. Poussez vers la branche (`git push origin feature/ma-fonctionnalite`).
5. Ouvrez une Pull Request.

## License

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
