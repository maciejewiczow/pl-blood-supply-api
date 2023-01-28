from flask_openapi3 import Info
from flask_openapi3 import OpenAPI
from api.endpoints import defineEndpoints
from api.utils.BaseModelEncoder import BaseModelEncoder

info = Info(
    title="Polish blood supply info API",
    description="API exposing the information about RCKiK facilites accross Poland and their blood supply",
    version="1.0.0"
)
app = OpenAPI(__name__, info=info)

app.json_encoder = BaseModelEncoder

defineEndpoints(app)

if __name__ == "__main__":
    app.run()
