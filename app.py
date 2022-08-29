from flask import Flask, request
from flask_restx import fields, Resource, Api
from tasks import add, celery_app, name
from celery.result import AsyncResult


app = Flask(__name__)
app.config["DEBUG"] = True


api = Api(app, version='0.0.1',
          title='Flask-RESTX and Swagger test', doc='/api/doc')


task_id_output = api.model("task id", {
    "task id": fields.String(required=True,
                             default="9bc07713-640d-4cbc-8074-74cbf765c635")
})


status_output = api.model("status", {
    "status": fields.String(required=True, default="PENDING"),
    "echo": fields.String(required=True, default="{'done': 0, 'total': 10}")
})


add_input = api.model("add", {
    "x": fields.Integer(required=True, example=1),
    "y": fields.Integer(required=True, example=2)
}
)


@api.route("/post_add")
class Add_input(Resource):
    @api.expect(add_input)
    @api.marshal_with(task_id_output)
    def post(self):
        ans = add.delay(api.payload.get("x"), api.payload.get("y"))
        return {"task id": ans.id}


@api.route("/get_id")
class Add_output(Resource):
    @api.doc(params={"id": "9bc07713-640d-4cbc-8074-74cbf765c635"})
    @api.marshal_with(status_output)
    def get(self):
        res = AsyncResult(request.args.get("id"), app=celery_app)
        return {"status": res.status,
                "echo": res.result}


@api.route("/get_name")
class Name_output(Resource):
    @api.doc(params={"name": "your name"})
    @api.marshal_with(task_id_output)
    def get(self):
        data = name.delay(request.args.get("name"))
        return {"task id": data.id}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
