# -*- coding: utf-8 -*-
import typing


def register_rest_api(
    app, view, endpoint, url: str, pk: str = "_id", pk_type: str = "int"
) -> None:
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None}, view_func=view_func, methods=["GET"])
    app.add_url_rule(url, view_func=view_func, methods=["POST"])
    app.add_url_rule(
        f"{url}<{pk_type}:{pk}>", view_func=view_func, methods=["GET", "PUT", "DELETE"]
    )
