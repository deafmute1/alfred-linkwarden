A linkwarden client for alfred.

[Download Here](https://github.com/deafmute1/alfred-linkwarden/releases/latest/download/Linkwarden.Search.alfredworkflow)

Requires: Python. Tested on Python3.9+.

## Setup 
1. Set linkwarden API key 
2. Set instance URL
3. Optionally change keywords, or set up optional keyword for a specific collection.
3. After install, please run any command and allow the script some time (>1 min) to install dependancies in the background before it will display results on subsequent uses.

## Usage 
To display/search all links: `lw {query}`
- To open in browser, return the link.
- To delete a link, use `Shift` modifier
- To open a preserved version on your linkwarden server use `cmd/⌘`.

To display/search all collections: `lwc {query}`
- You can display/search each collection by returning it. The contents of each collection are searchable and have the same modifier options as `lw`
- You can open the collection in your browser with `cmd/⌘` modifier

To add a link: `lwa {url}` (or via universal action "Add to Linkwarden")
- After entering the URL, you will be asked to select a collection to add the link to.

You can search/display a collection via a custom keyword. 
- The "id" is the nmumber at the end of the url when you navigate to that collection in the Web App. 

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
  - [ ] Export workflow file
- [ ] Push and create git tag for version
- [ ] Make GitHub release and upload `Linkwarden.Search.alfredworkflow`
