# graphql
Study GraphQL on GitLab Enterprise Edition 13.3.1-ee

## GraphQL object explorer  
https://gitlab.com/-/graphql-explorer

## GraphQL API:
### Header
POST http://gitlab.local/api/graphql  
Authorization: Bearer $TOKEN  
Content-Type: application/json  
### Query body
```json
{"query":"query {group(fullPath:\"sdn\"){fullName  id path iterations{nodes{title}}}}"}
```

Result: OK
```json
{
  "data": {
    "group": {
      "fullName": "sdn",
      "id": "gid://gitlab/Group/113",
      "path": "sdn",
      "iterations": {
        "nodes": [
          {
            "title": "Sprint 68 (2020-09-21 to 2020-09-25)"
          }
        ]
      }
    }
  }
}
```
### Mutation body
#### Example: Update iteration
```json
{"query":"mutation{updateIteration(input:{groupPath:\"gid://gitlab/Group/113\",id:\"gid://gitlab/Iteration/1\",title:\"Test\"}){ iteration{id title} errors}}"}
```

Result: fail due to error of gitlab 13.3.1-ee
```json
{
  "data": {
    "updateIteration": null
  },
  "errors": [
    {
      "message": "The resource that you are attempting to access does not exist or you don't have permission to perform this action",
      "locations": [
        {
          "line": 1,
          "column": 10
        }
      ],
      "path": [
        "updateIteration"
      ]
    }
  ]
}
```
#### Example: Create iteration
```json
{"query":"mutation{createIteration(input:{groupPath:\"testgroup\",title:\"Test\",startDate:\"2020-12-06\",dueDate:\"2020-12-08\"}){ iteration{id title} errors}}"}
```

Result: OK
```json
{
  "data": {
    "createIteration": {
      "iteration": {
        "id": "gid://gitlab/Iteration/30",
        "title": "Test1"
      },
      "errors": []
    }
  }
}
```

## Refer: 
https://docs.gitlab.com/ee/api/graphql/getting_started.html   
https://docs.gitlab.com/ee/api/graphql/reference/index.html#updateiterationpayload

