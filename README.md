A linkwarden client for alfred.

[Download Here](https://github.com/deafmute1/alfred-linkwarden/releases/latest/download/Linkwarden.Search.alfredworkflow)

Requires: Python. Tested on Python3.9+.

## Setup 
1. Set linkwarden API key 
2. Set instance URL
3. After install, please write `lw` or `lwc` and allow the script some time (>1 min) to install dependancies in the background before it will display results on subsequent uses.

## Usage 
To display/search all links: `lw {query}`
- To open in browser, return the link.
- To delete a link, use `Shift` modifier
- To open a preserved version on your linkwarden server use `cmd/⌘`.

To display/search all collections: `lwc {query}`
- You can display/search each collection by returning it. The contents of each collection are searchable and have the same modifier options as `lw`
- You can open the collection in your browser with `cmd/⌘` modifier

You can search/display a collection via a custom keyword. 
- An example is given in the workflow object. 
- You need create a `Script Filter` with the script `bash ./helper.sh collection 16 "$@"`, where `16` is the specific collection id.
-  You can retrieve this id by looking at the url of a collection when it is open in your browse, it will be the final value in the path.

This workflow supports some special meta "magic" arguments. To view them, use `lw workflow:help`. To force the workflow to check for and install updates, use `lw workflow:update`. 

## TODO
- Download and display favicons? - expensive
- Show generic icons for collections, links and each preserved format
- Refresh Script Filter after deleting item.

## Release Checklist
- [ ] Test all three commands are working still. 
- [ ] Update `__version__` string
- [ ] Delete `workflow/env` folder 
- [ ] Export workflow from Alfred Workflow Editor. 
  - [ ] Copy README 
  - [ ] Copy Version 
- [ ] Push and create git tag for version
- [ ] Make GitHub release and upload `Linkwarden.Search.alfredworkflow`