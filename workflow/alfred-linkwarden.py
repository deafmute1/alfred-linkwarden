import shutil
import subprocess
import os 
import sys 
from typing import Union

import requests 
from workflow import Workflow 

SAVED_FORMATS = {
    "Screenshot": "1", 
    "PDF": "2",
    "Readable": "3",
    "Webpage Copy": "4"
}

def lw_url() -> str:
    return os.environ['A_LW_URL'].rstrip('/')

def get_links(query: Union[str, None], collection_id: Union[str, None] = None): 
    params = {
        "searchByName": "true",
        "searchByDescription": "true",
        "searchByUrl": "true"
    } 
    if query is not None: params['searchQueryString'] = query 
    if collection_id is not None: params['collectionId'] = collection_id
    return requests.get(
        url=lw_url() + "/api/v1/links",
        headers={"Authorization": "Bearer " + os.environ['A_LW_API_KEY']}, 
        params=params       
    )
    
def delete_link(link_id: str): 
    return requests.delete(
        url=lw_url() + "/api/v1/links/" + link_id, 
        headers={"Authorization": "Bearer " + os.environ['A_LW_API_KEY']},
    )

def get_all_collections(): 
    return requests.get(
        url=lw_url() + "/api/v1/collections",
        headers={"Authorization": "Bearer " + os.environ['A_LW_API_KEY']},
    )

def query_json_to_workflow_item(response: requests.Response):
    for link in response.json()["response"]:
        item = workflow.add_item(
            title=link["name"],
            subtitle=link["url"],
            copytext=link["url"],
            arg=link["url"],
            valid=True
        )
        mod = item.add_modifier(
            "cmd", subtitle="Delete Entry", arg=str(link["id"])
        )
    workflow.send_feedback()
    
def links_to_workflow_items(workflow: Workflow, response: requests.Response):
    for link in response.json()["response"]:
        item = workflow.add_item(
            title=link["name"],
            subtitle=link["url"],
            copytext=link["url"],
            arg=link["url"],
            valid=True
        )
        mod = item.add_modifier(
            "shift", subtitle="Delete Entry", arg=str(link["id"])
        )
        mod = item.add_modifier(
            "cmd", subtitle="Open preserved version", arg=str(link["id"])
        )
    workflow.send_feedback()

def collections_to_workflow_items(workflow: Workflow, response: requests.Response): 
    for c in response.json()["response"]:
        item = workflow.add_item( 
            title=c["name"],
            subtitle=c["description"],
            copytext=lw_url() + "/collections/" + str(c['id']),
            arg=str(c['id']),
            valid=True
        )
        mod = item.add_modifier(
            "cmd", subtitle="Open in Browser"
        )
    workflow.send_feedback()
    
def main(workflow: Workflow) -> requests.Response:
    args = sys.argv[1:]
    if args[0] == "link":
        # alfred-linkwarden.py link <QUERY (STR)> 
        links_to_workflow_items(workflow, get_links(' '.join(args[1:]), None))
    elif args[0] == "collection":
        # alfred-linkwarden.py collection <COLLECTION ID (INT)>  <QUERY>
        if len(args) > 2:
            query = ' '.join(args[2:]) 
        else:
            query = None
        links_to_workflow_items(workflow, get_links(query, args[1]))
    elif args[0] == "collections": 
        # alfred-linkwarden.py collections
        collections_to_workflow_items(workflow, get_all_collections())
    elif args[0] == "delete": 
        # alfred-linkwarden.py delete <LINK ID (INT)>
        delete_link(args[1])
    elif args[0] == "saved": 
        base=lw_url()+ "/preserved/" + args[1] + "?format="
        for k, v in SAVED_FORMATS.items(): 
            workflow.add_item(
                title="Open" + k,
                copytext=base + v, 
                arg=base + v, 
                valid=True
            )
        workflow.send_feedback()

    
if __name__ == "__main__":
    # if somehow not inside venv, force recreate venv and rerun helper script
    def in_venv():
        return (hasattr(sys, 'real_prefix') or
                (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
    if not in_venv():
        env_loc = os.environ.get("A_ENV_LOC", "./env")
        if os.path.isdir(env_loc):
            shutil.rmtree(env_loc)
        subprocess.run(["bash", "./helper.sh"])
    
    workflow = Workflow(update_settings={'github_slug': 'deafmute1/alfred-linkwarden'})
    workflow.data_serializer = 'json'
    sys.exit(workflow.run(main))
