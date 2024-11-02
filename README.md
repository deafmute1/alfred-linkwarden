Search linkwarden from alfred.

[Download Here](https://github.com/deafmute1/alfred-linkwarden/releases/latest/download/Linkwarden.Search.alfredworkflow)

## Usage
You can search all links with the default keyword, `lw {query}`

You can search within a collection/show all items in collection ordered by date added by adding a custom keyword. An example is given in the workflow object. You need to create a `Script Filter` object, and add `bash ./helper.sh collection 16 "$@"` as the script value, where `16` is the specific collection id. You can retrieve this id by looking at the url of a collection when it is open in your browse, it will be the final value in the path.


TODO
- Add options to action url in other browser, incognito etc.
- More options to browse linkwarden (e.g. collections)
- Download and display favicons