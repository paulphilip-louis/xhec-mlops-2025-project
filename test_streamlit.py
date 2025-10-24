"""
Tests simples pour l'interface Streamlit
Vérifie que les fonctions principales fonctionnent correctement
"""

import pytest
import pandas as pd
import numpy as np
import requests
from unittest.mock import patch, Mock
import sys
import os

# Ajouter le répertoire racine au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def test_load_sample_data():
    """Test du chargement des données d'exemple"""
    # Mock du fichier CSV
    mock_data = pd.DataFrame(
        {
            "Sex": ["M", "F", "I"] * 10,
            "Length": np.random.uniform(0.1, 0.8, 30),
            "Diameter": np.random.uniform(0.1, 0.7, 30),
            "Height": np.random.uniform(0.01, 0.3, 30),
            "Whole weight": np.random.uniform(0.1, 2.0, 30),
            "Shucked weight": np.random.uniform(0.05, 1.0, 30),
            "Viscera weight": np.random.uniform(0.01, 0.5, 30),
            "Shell weight": np.random.uniform(0.01, 0.5, 30),
            "Rings": np.random.randint(1, 30, 30),
        }
    )

    with patch("pandas.read_csv", return_value=mock_data):
        from streamlit_app import load_sample_data

        result = load_sample_data()

        assert isinstance(result, pd.DataFrame)
        assert len(result) <= 100  # Échantillon limité
        assert "Sex" in result.columns
        assert "Rings" in result.columns


def test_check_api_health():
    """Test de la vérification de santé de l'API"""
    from streamlit_app import check_api_health

    # Test avec API accessible
    with patch("streamlit_app.requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = check_api_health()
        assert result

    # Test avec API inaccessible - utiliser requests.exceptions.RequestException
    with patch(
        "streamlit_app.requests.get",
        side_effect=requests.exceptions.RequestException("Connection error"),
    ):
        result = check_api_health()
        assert not result


def test_make_prediction():
    """Test de la fonction de prédiction"""
    from streamlit_app import make_prediction

    # Données de test
    test_data = {
        "sex": "M",
        "length": 0.5,
        "diameter": 0.4,
        "height": 0.15,
        "whole_weight": 0.8,
        "shucked_weight": 0.3,
        "viscera_weight": 0.15,
        "shell_weight": 0.2,
    }

    # Mock de la réponse API
    mock_response = Mock()
    mock_response.json.return_value = {"predicted_age": 15.2, "confidence": 0.85}
    mock_response.raise_for_status.return_value = None

    with patch("streamlit_app.requests.post", return_value=mock_response):
        result = make_prediction(test_data)

        assert result is not None
        assert "predicted_age" in result
        assert "confidence" in result
        assert result["predicted_age"] == 15.2


def test_data_validation():
    """Test de la validation des données d'entrée"""
    # Test des valeurs limites
    valid_data = {
        "sex": "M",
        "length": 0.5,
        "diameter": 0.4,
        "height": 0.15,
        "whole_weight": 0.8,
        "shucked_weight": 0.3,
        "viscera_weight": 0.15,
        "shell_weight": 0.2,
    }

    # Vérifier que toutes les clés requises sont présentes
    required_keys = [
        "sex",
        "length",
        "diameter",
        "height",
        "whole_weight",
        "shucked_weight",
        "viscera_weight",
        "shell_weight",
    ]

    for key in required_keys:
        assert key in valid_data

    # Vérifier les types de données
    assert isinstance(valid_data["sex"], str)
    assert isinstance(valid_data["length"], (int, float))
    assert isinstance(valid_data["diameter"], (int, float))
    assert isinstance(valid_data["height"], (int, float))
    assert isinstance(valid_data["whole_weight"], (int, float))
    assert isinstance(valid_data["shucked_weight"], (int, float))
    assert isinstance(valid_data["viscera_weight"], (int, float))
    assert isinstance(valid_data["shell_weight"], (int, float))


def test_sample_data_structure():
    """Test de la structure des données d'exemple"""
    mock_data = pd.DataFrame(
        {
            "Sex": ["M", "F", "I"] * 10,
            "Length": np.random.uniform(0.1, 0.8, 30),
            "Diameter": np.random.uniform(0.1, 0.7, 30),
            "Height": np.random.uniform(0.01, 0.3, 30),
            "Whole weight": np.random.uniform(0.1, 2.0, 30),
            "Shucked weight": np.random.uniform(0.05, 1.0, 30),
            "Viscera weight": np.random.uniform(0.01, 0.5, 30),
            "Shell weight": np.random.uniform(0.01, 0.5, 30),
            "Rings": np.random.randint(1, 30, 30),
        }
    )

    # Vérifier les colonnes requises
    required_columns = [
        "Sex",
        "Length",
        "Diameter",
        "Height",
        "Whole weight",
        "Shucked weight",
        "Viscera weight",
        "Shell weight",
        "Rings",
    ]

    for col in required_columns:
        assert col in mock_data.columns

    # Vérifier les valeurs de sexe
    assert set(mock_data["Sex"].unique()).issubset({"M", "F", "I"})

    # Vérifier les plages de valeurs
    assert mock_data["Length"].min() >= 0
    assert mock_data["Rings"].min() >= 1
    assert mock_data["Rings"].max() <= 30


if __name__ == "__main__":
    # Exécuter les tests
    pytest.main([__file__, "-v"])
