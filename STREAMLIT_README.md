# Interface Streamlit - Prédiction d'Âge des Abalones

## 🌐 Vue d'ensemble

Cette interface Streamlit permet d'interagir avec l'API FastAPI pour prédire l'âge des abalones en utilisant leurs caractéristiques physiques.

## 🚀 Fonctionnalités

### 📊 Saisie Interactive des Données
- **Interface utilisateur intuitive** avec sliders et sélecteurs
- **Validation en temps réel** des données saisies
- **Aide contextuelle** pour chaque caractéristique

### 🔮 Prédiction en Temps Réel
- **Appel API** vers le backend FastAPI
- **Affichage des résultats** avec métriques de confiance
- **Visualisation comparative** avec les données d'entraînement

### 📈 Analyse des Données
- **Statistiques descriptives** des données d'exemple
- **Matrice de corrélation** entre les caractéristiques
- **Graphiques interactifs** avec Plotly

## 🛠️ Installation et Utilisation

### Prérequis
```bash
# Installer les dépendances Streamlit
pip install streamlit plotly requests pandas numpy
```

### Lancement
```bash
# Option 1: Script de lancement
./run_streamlit.sh

# Option 2: Commande directe
streamlit run streamlit_app.py
```

### Accès
- **Interface**: http://localhost:8501
- **API Backend**: http://localhost:8000 (doit être démarrée)

## 📋 Structure des Données

### Input (API)
```json
{
    "sex": "M|F|I",
    "length": 0.455,
    "diameter": 0.365,
    "height": 0.095,
    "whole_weight": 0.514,
    "shucked_weight": 0.2245,
    "viscera_weight": 0.101,
    "shell_weight": 0.15
}
```

### Output (API)
```json
{
    "predicted_age": 15.2,
    "confidence": 0.85,
    "model_version": "v1.0"
}
```

## 🎨 Personnalisation

### Configuration Streamlit
Le fichier `.streamlit/config.toml` contient :
- Configuration du serveur
- Thème personnalisé
- Paramètres de sécurité

### Thème
- **Couleur primaire**: Rouge corail (#FF6B6B)
- **Arrière-plan**: Blanc (#FFFFFF)
- **Style**: Moderne et épuré

## 🔧 Intégration avec l'API

### Vérification de Santé
```python
def check_api_health() -> bool:
    response = requests.get("http://localhost:8000/")
    return response.status_code == 200
```

### Prédiction
```python
def make_prediction(data: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post("http://localhost:8000/predict", json=data)
    return response.json()
```

## 📊 Visualisations

### Graphiques Disponibles
1. **Scatter Plot**: Comparaison poids vs âge
2. **Bar Chart**: Distribution par sexe
3. **Histogramme**: Distribution de l'âge
4. **Heatmap**: Matrice de corrélation

### Interactivité
- **Zoom et pan** sur les graphiques
- **Hover data** avec informations détaillées
- **Sélection de données** pour analyse approfondie

## 🚨 Gestion d'Erreurs

### Erreurs API
- **Connexion refusée**: Message d'erreur avec instructions
- **Timeout**: Retry automatique avec délai
- **Données invalides**: Validation côté client

### Fallback
- **Données simulées** si le fichier CSV n'est pas disponible
- **Mode démo** avec prédictions factices

## 🔄 Workflow d'Utilisation

1. **Démarrer l'API FastAPI** (port 8000)
2. **Lancer Streamlit** (port 8501)
3. **Saisir les caractéristiques** de l'abalone
4. **Cliquer sur "Prédire l'Âge"**
5. **Analyser les résultats** et visualisations

## 📝 Notes de Développement

### Structure du Code
- **Modulaire**: Fonctions séparées pour chaque fonctionnalité
- **Type hints**: Annotations de type pour la clarté
- **Documentation**: Docstrings détaillées
- **Gestion d'erreurs**: Try/catch appropriés

### Bonnes Pratiques
- **Séparation des responsabilités**: UI, API, données
- **Configuration externalisée**: Fichiers de config séparés
- **Logging**: Messages informatifs pour l'utilisateur
- **Performance**: Chargement paresseux des données

## 🎯 Prochaines Améliorations

- [ ] **Authentification utilisateur**
- [ ] **Sauvegarde des prédictions**
- [ ] **Export des résultats**
- [ ] **Mode batch** pour prédictions multiples
- [ ] **Intégration MLflow** pour le tracking
- [ ] **Tests automatisés** de l'interface
