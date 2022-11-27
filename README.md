# Backend for Pojok Statistic website

## API Spec

---

### dataset

- Method : `POST`
- Endpoint : `/api/turnover`
- Header :
  - Content-Type : `multipart/form-data`
  - Accept : `multipart/form-data`
- body :

```json
{
  "file": file.xls
}
```

- response :

```json
{
  "message": "Success",
  "code": 200,
  "error": "",
  "data": [
    { "label": "John Doe", "data": 200000 },
    { "label": "Jane Doe", "data": 500000 },
    { "label": "Mike Doe", "data": 150000 }
  ]
}
```
