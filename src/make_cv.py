from fpdf import FPDF

cvs = {
    "cv_data.pdf": [
        "DATA SCIENTIST",
        "Nom : Alice Martin",
        "Experience : 4 ans",
        "Competences : Python, pandas, scikit-learn, SQL, TensorFlow, NLP, Docker",
        "Formation : Master Data Science",
    ],
    "cv_web.pdf": [
        "DEVELOPPEUR WEB",
        "Nom : Bruno Leroy",
        "Experience : 5 ans",
        "Competences : JavaScript, React, Node.js, HTML, CSS, PHP",
        "Formation : Licence Informatique",
    ],
    "cv_data_junior.pdf": [
        "DATA ANALYST JUNIOR",
        "Nom : Chloe Bernard",
        "Experience : 1 an",
        "Competences : Python, SQL, Excel, Power BI, statistiques",
        "Formation : Master Statistiques",
    ],
}

for nom, lignes in cvs.items():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    for ligne in lignes:
        pdf.cell(0, 10, ligne, ln=True)
    pdf.output(f"data/{nom}")
    print("cree : data/" + nom)