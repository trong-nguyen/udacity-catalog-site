# Udacity Catalog Site
A Catalog Site For Full-stack Practice Purposes

## Dependencies

## Usage

## Design

### Mockups

### Routing

```yaml
/: root
/catalog: root
	-/<string:catalog-name>/items: display all items of catalog-name
	-/<string:catalog-name>/<string:item-name>: display info for item-name
	-/<string:catalog-name>/<string:item-name>/edit: edit item-name
	-/<string:catalog-name>/<string:item-name>/delete: delete item-name
/api/v1/catalog: RESTful endpoint displaying all catalogs in json format
```

### Templates and Forms

### CRUD functionalities

### API endpoints
