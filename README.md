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
</div>

# Scraper d'offres d'emploi Kelio

Ce projet est un scraper simple et efficace conçu pour extraire les offres d'emploi liées au développement web de la société Kelio. Il utilise des bibliothèques Python telles que `requests`, `BeautifulSoup`, et `Selenium` pour récupérer et analyser les données.

## Table des matières

- [Fonctionnalités](#fonctionnalités)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Interface Web](#interface-web)
- [Automatisation](#automatisation)
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

Plusieurs options gratuites sont disponibles pour déployer ce projet :

### Option 1 : Render (Recommandé)

1. Créez un compte sur [Render](https://render.com)
2. Connectez votre dépôt GitHub
3. Deployer en utilisant le fichier `render.yaml` inclus :
   - Un service web pour l'interface
   - Un service worker pour le scraper

### Option 2 : Railway

1. Créez un compte sur [Railway](https://railway.app)
2. Connectez votre dépôt GitHub
3. Configurez les variables d'environnement
4. Utilisez le fichier `docker-compose.yml` pour déployer les deux services

### Option 3 : PythonAnywhere

1. Créez un compte sur [PythonAnywhere](https://www.pythonanywhere.com)
2. Uploadez votre code
3. Configurez une application web Flask
4. Créez une tâche planifiée pour le scraper

Pour chaque option, assurez-vous de configurer les variables d'environnement nécessaires selon votre fichier `.env`.


## Automatisation

Pour automatiser l'exécution du scraper, vous pouvez utiliser `cron` sur Linux/Mac :

1. Ouvrez le crontab :
```bash
crontab -e
```

2. Ajoutez la ligne suivante pour exécuter le scraper toutes les 6 heures :
```bash
0 */6 * * * /usr/bin/python3 /path/to/scraper.py
```

## Contributions

Les contributions sont les bienvenues ! Si vous souhaitez améliorer ce projet, veuillez suivre ces étapes :

1. Forkez le projet.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/ma-fonctionnalite`).
3. Commitez vos modifications (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`).
4. Poussez vers la branche (`git push origin feature/ma-fonctionnalite`).
5. Ouvrez une Pull Request.

## License

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.
