from flask import Flask
from flask_deucalion.deucalion import Deucalion
from flask_deucalion.models import Description, Author, Version, Corpus
from flask_deucalion.services import PieWebApp


app = Flask(__name__)
app.register_blueprint(Deucalion)

APinche = Author("Ariane Pinche", lod="http://chartes.psl.eu/apinche")
JBCamps = Author("Jean-Baptiste Camps", lod="http://chartes.psl.eu/jbcamps")
Wauchier = Corpus(
    "Li Seint Confessors, Édition nativement numérique",
    authors=[APinche],
    uri="http://chartes.psl.eu/corpora/Wauchier",
    date="2014-"
)
# Maybe add funder ?
Geste = Corpus(
    "Floovant et chansons de geste",
    authors=[JBCamps],
    uri="http://chartes.psl.eu/corpora/Geste",
    date="2013-"
)


# Maybe add software version ? Citation ?
ENC_Fro = PieWebApp(
    uri="http://localhost:5001",
    title="Model for Ancient-French",
    language_code="fro",
    identifier="enc-001",
    model_path="./models/path",
    descriptions=[
        Description("Model built on Wauchier de Denain, Graal and other kind of Old French data")
    ],
    authors=[
        Author("Ecole nationale des Chartes", lod="https://viaf.org/viaf/134649805/")
    ],
    corpora=[
        Version(Wauchier, date="2018-10-23"),
        Version(Geste, date="2018-10-23")
    ]
)
Deucalion.register_model(ENC_Fro)

if __name__ == "__main__":
    app.run(debug=True)
