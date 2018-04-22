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

### Get all name_entities

GET Request

```
URL/database/api/v1.0/names/
```

### Get all places

GET Request

```
URL/database/api/v1.0/places/
```

### Get Documents by ID

GET Request

```
URL/database/api/v1.0/id/<int:id>
```


### Get Documents by exact Keyword

GET Request

```
URL/database/api/v1.0/keyword/exact/<string:keyword>
```

### Get Documents by like Keyword

GET Request

```
URL/database/api/v1.0/keyword/like/<string:keyword>
```

### Get Documents by more than one (many) Keyword

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

### Get Documents by like Author

GET Request

```
URL/database/api/v1.0/author/like/<string:author>
```

### Get Documents by like Doctype

GET Request

```
URL/database/api/v1.0/doctype/like/<string:doctype>
```


### Get Documents by like place

GET Request

```
URL/database/api/v1.0/place/like/<string:place>
```

### Get Documents by exact place

GET Request

```
URL/database/api/v1.0/place/exact/<string:place>
```

### Get Documents by exact name_entity

GET Request

```
URL/database/api/v1.0/name_entity/exact/<string:name_entity>
```

### Get Documents by like name_entity

GET Request

```
URL/database/api/v1.0/name_entity/like/<string:name_entity>
```

### Get Documents for many names

POST Request

```
URL/database/api/v1.0/name_entity/many/
```

**Header:** `"content-type" = "application/json"`

**Body:**

```json
{
    "name_entity": ["Name1","Name2"]
}
```

### Get Summary by ID

GET Request

```
URL/database/api/v1.0/summary/<int:id>
```

returns

```
{
  "summary": "Hallo Hallo"
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

## Hyper Special Functions

### translate
Text to Text: Text1: 2^8 Chars --> Text2: 2^4 Chars 

### se_id
Helperfunktion: Returns String as a path
