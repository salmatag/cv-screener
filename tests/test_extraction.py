from src.extract_skills import extraire_competences, extraire_experience


def test_experience_extraite():
    assert extraire_experience("Experience : 4 ans") == 4


def test_experience_absente():
    assert extraire_experience("Aucune experience") is None


def test_competences_detectees():
    comp = extraire_competences("Python, SQL et Docker")
    assert "python" in comp
    assert "sql" in comp
    assert "docker" in comp
    assert "react" not in comp