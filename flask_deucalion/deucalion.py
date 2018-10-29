from flask import Blueprint, jsonify, url_for, Response, request
from typing import Optional
from .models import Model
from .formats import Formats, JsonLd
from .errors import UnknownModel, DeucalionException

__all__ = [
    "Deucalion",
    "api_home",
    "api_documentation",
    "api_documentation_model",
    "api_model_get",
    "deucalion_error",
    "jsonldify"
]

_context = {
    "@vocab": "https://www.w3.org/ns/hydra/core#",
    "dc": "http://purl.org/dc/terms/"
}


def jsonldify(data: dict, status_code: int=200, headers: Optional[dict]=None) -> Response:
    response = jsonify(data)
    response.status_code = status_code
    if headers:
        response.headers = headers
    return response


class _Deucalion(Blueprint):
    def __init__(self, *args, **kwargs):
        super(_Deucalion, self).__init__(*args, **kwargs)
        self.models = {}

    def register_model(self, model: Model):
        self.models[model.identifier] = model

    def get_model(self, model_id):
        if model_id in self.models:
            return self.models[model_id]
        raise UnknownModel("Model {} is unknown".format(model_id))


Deucalion = _Deucalion("deucalion", "deucalion")


@Deucalion.errorhandler(DeucalionException)
def deucalion_error(error: DeucalionException):
    return jsonldify(
        {"status": "error", "message": error.message},
        status_code=error.code
    )


@Deucalion.route("/")
def api_home():
    return jsonldify({
        "@context": _context,
        "title": "Translation models",
        "description": "Each model can be called using its URI @id with a POST request"
                       "where `data` is the input plain/text",
        "members": [
            model.export(JsonLd)
            for model in Deucalion.models.values()
        ]
    })


@Deucalion.route("/model/<model_id>", methods=["GET"])
def api_model_get(model_id):
    response = Deucalion.get_model(model_id).export(JsonLd)
    response["@context"] = _context
    return jsonldify(response)


@Deucalion.route("/model/<model_id>", methods=["POST"])
def api_model_post(model_id):
    text = request.form.get("text")
    if not text:
        return "Missing data in text parameter", 401, {"Content-Type": "plain/text"}
    response = Deucalion.get_model(model_id).lemmatize(text)
    return response, 200, {"Content-Type": "plain/text"}


@Deucalion.route("/doc")
def api_documentation():
    return jsonify({
      "@context": "http://www.w3.org/ns/hydra/context.jsonld",
      "@id": url_for("deucalion.api_documentation", _external=True),
      "@type": "ApiDocumentation",
      "title": "Deucalion API",
      "description": "API built to help use lemmatisation model produced with deep learning tools.",
      "entrypoint": url_for("deucalion.api_home", _external=True),
      "supportedClass": [
          url_for("deucalion.api_documentation_model", _external=True)
      ]
    })


@Deucalion.route("/doc/Model")
def api_documentation_model():
    return jsonify({
      "@context": "http://www.w3.org/ns/hydra/context.jsonld",
      "@id": url_for("deucalion.api_documentation_model", _external=True),
      "@type": "Class",
      "title": "Model",
      "description": "A model produced and usable for lemmatization",
      "supportedOperation": [
          {
              "@type": "Operation",
              "title": "Lemmatization",
              "method": "POST",
              "expects": "text/plain",
              "returns": "text/plain",
          }
      ]
    })

