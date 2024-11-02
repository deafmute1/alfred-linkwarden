import shutil
import subprocess
import os 
import sys 
import urllib.parse

from workflow import Workflow, web, ICON_INFO

def get_links(query: str|None, collection_id: str|None = None): 
    params = {
        "searchByName": "true",
        "searchByDescription": "true",
        "searchByUrl": "true"
    } 
    if query is not None: params['searchQueryString'] = query 
    if collection_id is not None: params['collectionId'] = collection_id
    return web.get(
        url=urllib.parse.urljoin(os.environ['LW_URL'], "/api/v1/links"),
        headers={"Authorization": f"Bearer {os.environ["LW_API_KEY"]}"},
        params=params       
    )

def main(workflow):
    if sys.argv[1] == "link": 
        response = get_links(' '.join(sys.argv[2:]), None)
    elif sys.argv[1] == "collection": 
        if len(sys.argv) > 3:
            query = ' '.join(sys.argv[3:]) 
        else:
            query = None
        response = get_links(query, sys.argv[2])
    else: 
        return

    for item in response.json()["response"]:
        workflow.add_item(
            title=item["name"],
            subtitle=item["url"],
            copytext=item["url"],
            arg=item["url"],
            valid=True
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
