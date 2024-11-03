import shutil
import subprocess
import os 
import sys 
import urllib.parse

import requests 
from workflow import Workflow 

def get_links(query: str|None, collection_id: str|None = None): 
    params = {
        "searchByName": "true",
        "searchByDescription": "true",
        "searchByUrl": "true"
    } 
    if query is not None: params['searchQueryString'] = query 
    if collection_id is not None: params['collectionId'] = collection_id
    return requests.get(
        url=urllib.parse.urljoin(os.environ['LW_URL'], "/api/v1/links"),
        headers={"Authorization": f"Bearer {os.environ["LW_API_KEY"]}"}, 
        params=params       
    )
    
def delete_link(link_id: str): 
    return requests.delete(
        url=urllib.parse.urljoin(os.environ['LW_URL'], f"/api/v1/links/{link_id}"), 
        headers={"Authorization": f"Bearer {os.environ["LW_API_KEY"]}"},
    )
    
def proc_args_lw(args: list) -> requests.Response:
    if args[0] == "link": 
        return get_links(' '.join(args[1:]), None)
    elif args[0] == "collection": 
        if len(args) > 2:
            query = ' '.join(args[2:]) 
        else:
            query = None
        return get_links(query, args[1])
    elif args[0] == "delete": 
        delete_link(args[1])
        sys.exit()
    else: 
        sys.exit()
        
def main(workflow):
    response = proc_args_lw(sys.argv[1:])
    
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
    
if __name__ == "__main__":
    # if somehow not inside venv, force recreate venv and rerun helper script
    def in_venv():
        return (hasattr(sys, 'real_prefix') or
                (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
    if not in_venv():
        env_loc = os.environ.get("ENV_LOC", "./env")
        if os.path.isdir(env_loc):
            shutil.rmtree(env_loc)
        subprocess.run(["bash", "./helper.sh"])
    
    workflow = Workflow(update_settings={'github_slug': 'deafmute1/alfred-linkwarden'})
    workflow.data_serializer = 'json'
    sys.exit(workflow.run(main))
