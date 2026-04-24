# Pinterest Image Downloader

Used to mass download images from Pinterest via the URLs.

## Usage


`--threads 5` ( How many threads it will use to download the files, default is 5 )

`--input imageurls.txt` ( Put your pintrest image links in here, default is "urls.txt")

`--timeout 10` ( how long it will wait before timing out a request, default is 5 seconds)

`--out images` ( the folder name of where the images will go, default is "downloads")

## Getting Pinterest URLs

Open your Pinterest feed, press `F12` for console, paste this:

```javascript
copy(Array.from(new Set(Array.from(document.querySelectorAll('a[href*="/pin/"]')).map(a => a.href.match(/https:\/\/[^\/]+\/pin\/\d+/)?.[0]).filter(Boolean))).join('\n'))
