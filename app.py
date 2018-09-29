from flask import Flask
from flask_deucalion.deucalion import Deucalion
from flask_deucalion.models import Model, Description, Author


app = Flask(__name__)
app.register_blueprint(Deucalion)


ENC_Fro = Model(
    title="Model for Ancient-French",
    language_code="fro",
    identifier="enc-001",
    model_path="./models/path",
    descriptions=[
        Description("Model built on Wauchier de Denain, Graal and other kind of Old French data")
    ],
    authors=[
        Author("Ecole nationale des Chartes", lod="https://viaf.org/viaf/134649805/")
    ]
)
Deucalion.register_model(ENC_Fro)

if __name__ == "__main__":
    app.run(debug=True)
