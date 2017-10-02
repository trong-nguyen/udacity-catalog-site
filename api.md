FORMAT: 1A
HOST: http://localhost:5001/

# Sport Gear Catalog

A Catalog Site allows people view sport items, categorized by the sport that they are used
## Sports [/catalog]

### List All Sport Categories [GET]
List all sports that the catalog has gears for.

+ Response 200

        Soccers
        Baseball
        Basketball

### Group Gears [/catalog/{sport_name}]
Showing gears and gear details of a sport

+ Parameters

    + sport_name: `Soccer` (string) - name of a sport category.

#### Gear Collection [GET /catalog/{sport_name}/items]
List all gears in a specific sport

+ Response 201

        Goggles
        Snowboard

#### Group Gear Details [/catalog/{sport_name}/{gear_name}]

+ Parameters

    + gear_name: Ball (string) - name of the gear in the sport

##### Show [GET]
+ Response 200

        Shoes specifically designed to help players get the upper edge in a match.

##### Update [PUT /catalog/{sport_name}/{gear_name}/edit]
Edit gear details

+ Request (application/json)

        {
            "title": "Big Glove",
            "description": "To catch a ball easier",
            "category": "Soccer"
        }

+ Response 200

##### Delete A Gear [DELETE /catalog/{sport_name}/{gear_name}/delete]
Delete a gear

+ Response 204

## API [/api/{version}]
REST API endpoints

+ Parameters

    + version: `v1` (string) - API version

### Sport Collection [GET /api/{version}/catalog]
List all sports that the catalog has gears for.

+ Response 200 (application/json)

        [
            {
                "category": "Snowboarding",
                "items": [
                    {
                        "name": "Goggles",
                        "description": "A pair of glass that can be used underwarter"
                    }, {
                        "name": "Snowboard",
                        "description": "A board which is snow white"
                    }
                ]
            },
            {
                "category": "Soccer",
                "items": [
                ]
            },
            {
                "category": "Baseball",
                "items": [
                ]
            },
            {
                "category": "Frisbee",
                "items": [
                ]
            }
        ]

#### Group Gears [/api/{version}/{sport_name}]

+ Parameters

    + sport_name: `Soccer` (string) - name of a sport category.

##### Gear Collection [GET]
List all gears in a sport

+ Response 200 (application/json)

        [
            {
                "title": "Glove",
                "description": "To catch balls",
                "category": "Soccer"
            },
            {
                "title": "Ball",
                "description": "To play with",
                "category": "Soccer"
            }
        ]

##### Gear Details [GET /api/{version}/{sport_name}/{gear_name}]
Show detail of a gear

+ Parameters

    + gear_name: `Glove` (string) - name of the gear

+ Response 200 (application/json)

        {
            "title": "Glove",
            "description": "To catch balls",
            "category": "Soccer"
        }