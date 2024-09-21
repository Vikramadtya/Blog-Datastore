All the directory must follow the format {id}:{title}

The mandatory metadata is expected to have the following key mandatory

```json
{
    "blogNumber": "blog-number-as-int",
    "author": "author-of-blog",
    "demo": {
        "live": false,
        "preview": null,
        "repository": null
    },
    "publish": false, 
    "slug": "the-slug-of-blog",
    "summary": "description",
    "tags": [
        "tag-string"
    ],
    "title": "Blog Title",
    "previewImageSrc" : ""
}
```


only blog having metadata as `"publish": true` will be processed