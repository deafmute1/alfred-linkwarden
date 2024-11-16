A linkwarden client for alfred.

[Download Here](https://github.com/deafmute1/alfred-linkwarden/releases/latest/download/Linkwarden.Search.alfredworkflow)

## Setup 
1. Set linkwarden API key 
2. Set instance URL

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


## TODO
- Download and display favicons? - expensive
- Show generic icons for collections, links and each preserved format