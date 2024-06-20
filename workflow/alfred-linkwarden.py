import shutil
import subprocess
import os 
import sys 
import urllib.parse

from workflow import Workflow, web, ICON_INFO

def main(workflow):
    if workflow.update_available:
        workflow.add_item('New version available',
            'Action this item to install the update',
            autocomplete='workflow:update',
            icon=ICON_INFO
        )

    response = web.get(
        url=urllib.parse.urljoin(os.environ['LW_URL'], "/api/v1/links"),
        headers={"Authorization": f"Bearer {os.environ["LW_API_KEY"]}"},
        params={
            "searchQueryString": sys.argv[1:],
            "searchByName": "true",
            "searchByDescription": "true",
            "searchByUrl": "true"
        }        
    )

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