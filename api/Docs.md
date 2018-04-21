# Dokumentation Database REST API

## Contents

- [Get Data](#get-data)

  - [Get all Documents](#get-all-documents)

  - [Get all Keywords](get-all-keywords)

  - [Get Documents by exact Keyword](#get-documents-by-exact-keyword)

  - [Get Documents by like Keyword](#get-documents-by-like-keyword)

  - [Get Documents by more than one Keyword](#get-documents-by-more-than-one-keyword)

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

### Get Documents by  more than one Keyword

POST Request

```
URL/database/api/v1.0/keywords/many/
```

**Header:** `"content-type" = "application/json"`

**Body:**

```json
{
    "keywords": ["Keyword", "some more Keywords"] 
}
```

## Insert Data

### Insert Documents without Keywords

It will automatically detect wether the request was entered with or without keywords

POST Request

```
URL/database/api/v1.0/documents/insert/
```

**Header:** `"content-type" = "application/json"`

**Body:**

```json
{
    "link": "Path/To/Any/File"    
    "text": "some text",
    "doctype": "some doctype",
    "toc": "Table of content",
    "author": "AnyName",
    "name_entities": "Name1 Name2",
    "pages":4,
    "date":"2018-10-10"
}
```

### Insert Documents with Keywords

POST Request

```
URL/database/api/v1.0/documents/insert/
```

**Header:** `"content-type" = "application/json"`

**Body:**

```
{
    "link": "Path/To/File"    
    "text": "some text",
    "keywords": ["Keyword", "some more Keywords"],
    "doctype": "some doctype",
    "toc": "Table of content",
    "author": "AnyName",
    "name_entities": "Name1 Name2",
    "pages":4,
    "date":"2018-10-10"
}
```

### Insert Keywords

POST Request

```
URL/database/api/v1.0/keywords/insert/
```

**Header:** `"content-type" = "application/json"`

**Body:**

```json
{
    "id": 1,
    "keywords": ["Keyword", "some more Keywords"] 
}
```
