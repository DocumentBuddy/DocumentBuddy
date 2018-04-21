# Dokumentation Database REST API

## Contents

- [Get Data](#get-data)

  - [Get all Documents](#get-all-documents)

  - [Get all Keywords](get-all-keywords)

  - [Get Documents by exact Keyword](#get-documents-by-exact-keyword)

  - [Get Documents by like Keyword](#get-documents-by-like-keyword)

- [Insert Data](#insert-data)

  - [Insert Documents without Keywords](#insert-documents-without-keywords)

  - [Insert Documents with Keywords](#insert-documents-with-keywords)

  - [Insert Keywords](#insert-keywords)





## Get Data

### Get all Documents

GET Request

```
URL/database/api/v1.0/documents/
```

### Get all Keywords

GET Request

``` 
URL/database/api/v1.0/keywords/
```

### Get Documents by exact Keyword

GET Request

``` 
URL/database/api/v1.0/documents/keyword/exact/<string:keyword>
```

### Get Documents by like Keyword

GET Request

```
URL/database/api/v1.0/documents/keyword/like/<string:keyword>
```



## Insert Data

### Insert Documents without Keywords

POST Request

**Header:** `"content-type" = "application/json"`

**Body:**

```json
{
	"link": "Path/To/File",
	"text": "some text",
	"doctype": "some doctype"
}
```

### Insert Documents with Keywords

POST Request

**Header:** `"content-type" = "application/json"`

**Body:**

```
{
	"link": "Path/To/File"	
	"text": "some text",
	"keywords": ["Keyword", "some more Keywords"],
	"doctype": "some doctype"
}
```

### Insert Keywords

POST Request

**Header:** `"content-type" = "application/json"`

**Body:**

```json
{
	"link": "Path/To/File",
	"keywords": ["Keyword", "some more Keywords"] 
}
```


