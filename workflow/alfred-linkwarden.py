import os
import shutil
import subprocess
import sys
from collections.abc import Iterable, Mapping
from typing import Union
from urllib.parse import urlsplit

import requests

from workflow import Workflow

__version__ = "1.9"

SAVED_FORMATS = {
    "Screenshot": "1", "PDF": "2", "Readable": "3", "Webpage Copy": "4"
}

"""
API QUERIES
"""


def lw_url() -> str:
    return os.environ["A_LW_URL"].rstrip("/")


def lw_bearer() -> str:
    return {"Authorization": "Bearer " + os.environ["A_LW_API_KEY"]}


def get_links_old(
    query: Union[str, None], collection_id: Union[str, None] = None
) -> requests.Response:
    # this method is depreciated but is currently the only way to retrieve all
    # links in a collection by id.
    params = {
        "searchByName": "true",
        "searchByDescription": "true",
        "searchByUrl": "true",
        "searchByTags": "true",
    }
    if query is not None:
        params["searchQueryString"] = query
    if collection_id is not None:
        params["collectionId"] = collection_id
    return requests.get(
        url=lw_url() + "/api/v1/links", headers=lw_bearer(), params=params
    )


def search_links(query: Union[str, None]) -> requests.Response:
    return requests.get(
        url=lw_url() + "/api/v1/search",
        headers=lw_bearer(),
        params={
            "searchQueryString": query,
        },
    )


def delete_link(link_id: str) -> requests.Response:
    return requests.delete(
        url=lw_url() + "/api/v1/links/" + link_id,
        headers=lw_bearer(),
    )


def post_link(
    url: str, collection_id: Union[str, None] = None
) -> requests.Response:
    return requests.post(
        url=lw_url() + "/api/v1/links",
        headers=lw_bearer(),
        json={
            "url": url, "type": "url", "collection": {"id": int(collection_id)}
        }
    )


def add_link_to_collection(collection_id: str, url: str) -> None:
    # Assume https if no scheme.
    if not urlsplit(url).scheme:
        url = f"https://{url}"
    # Require a netloc as minimum url
    if not urlsplit(url).netloc:
        raise RuntimeError("No netloc (domain) segment in url, exiting")
    return post_link(url, collection_id)


def get_all_collections() -> requests.Response:
    return requests.get(
        url=lw_url() + "/api/v1/collections",
        headers=lw_bearer(),
    )


"""
WORKFLOW LOGIC
"""


def links_to_workflow_items(
    workflow: Workflow, links: Iterable[Mapping[str, any]]
) -> None:
    for link in links:
        item = workflow.add_item(
            title=link["name"],
            uid="l" + str(link["id"]),
            subtitle=link["url"],
            copytext=link["url"],
            arg=link["url"],
            valid=True,
        )
        item.add_modifier(
            "shift", subtitle="Delete Entry", arg=str(link["id"])
        )
        item.add_modifier(
            "cmd", subtitle="Open preserved version", arg=str(link["id"])
        )
    workflow.send_feedback()


def match_substring(f: str, s: str) -> bool:
    return f is not None \
        and f.casefold() in s.casefold()


def collections_to_workflow_items(
    workflow: Workflow,
    collections: Iterable[Mapping[str, any]],
    match_string: Union[str, None] = None,
) -> None:
    for c in collections:
        if match_substring(match_string, c["name"]):
            item = workflow.add_item(
                title=c["name"],
                uid="c" + str(c["id"]),
                subtitle=c["description"],
                copytext=lw_url() + "/collections/" + str(c["id"]),
                arg=str(c["id"]),
                valid=True,
            )
            item.add_modifier("cmd", subtitle="Open in Browser")
    workflow.send_feedback()


def saved_urls_to_workflow_items(workflow: Workflow, link_id: str) -> None:
    base = lw_url() + "/preserved/" + link_id + "?format="
    for k, v in SAVED_FORMATS.items():
        workflow.add_item(
            title="Open " + k, copytext=base + v, arg=base + v, valid=True
        )
    workflow.send_feedback()


"""
MAIN
"""


def query_join(lst: list, from_index: int = 0) -> Union[str, None]:
    ret = " ".join(lst[from_index:])
    return ret if ret else None


def main(workflow: Workflow) -> requests.Response:
    args = workflow.args
    if args[0] == "link":
        # alfred-linkwarden.py link <QUERY (STR)>
        links_to_workflow_items(
            workflow, search_links(query_join(args, 1)).json()["data"]["links"]
        )
    elif args[0] == "collection":
        # alfred-linkwarden.py collection <COLLECTION ID (INT)> <QUERY (STR)>
        links_to_workflow_items(
            workflow,
            get_links_old(query_join(args, 2), args[1]).json()["response"]
        )
    elif args[0] == "collections":
        # alfred-linkwarden.py collections <QUERY OR EMPTY>
        collections_to_workflow_items(
            workflow,
            get_all_collections().json()["response"], query_join(args, 1)
        )
    elif args[0] == "delete":
        # alfred-linkwarden.py delete <LINK ID (INT)>
        delete_link(args[1])
    elif args[0] == "saved":
        # alfred-linkwarden.py saved <LINK ID (INT)>
        saved_urls_to_workflow_items(workflow, args[1])
    elif args[0] == "add":
        # alfred-linkwarden.py add <COLLECTION ID (INT)> <URL (STR) OR NONE>
        add_link_to_collection(args[1], query_join(args, 2))


if __name__ == "__main__":
    # if somehow not inside venv, force recreate venv and rerun helper script
    def in_venv():
        return hasattr(sys, "real_prefix") or (
            hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
        )

    if not in_venv():
        env_loc = os.environ.get("A_ENV_LOC", "./env")
        if os.path.isdir(env_loc):
            shutil.rmtree(env_loc)
        subprocess.run(["bash", "./helper.sh"])

    workflow = Workflow(
        update_settings={
            "github_slug": "deafmute1/alfred-linkwarden",
            "version": __version__,
            "frequency": 7,
        }
    )
    workflow.data_serializer = "json"
    if workflow.update_available:
        workflow.start_update()
    sys.exit(workflow.run(main))
