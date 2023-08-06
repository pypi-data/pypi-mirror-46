bodhi.composer.start
--------------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.composer.start#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when a compose is requested to start",
        "type": "object",
        "properties": {
            "agent": {
                "type": "string",
                "description": "The name of the user who started this compose."
            },
            "composes": {
                "type": "array",
                "description": "A list of composes included in this compose job",
                "items": {
                    "$ref": "#/definitions/compose"
                }
            },
            "resume": {
                "type": "boolean",
                "description": "true if this is a request to resume the given composes"
            }
        },
        "required": [
            "agent",
            "composes",
            "resume"
        ],
        "definitions": {
            "compose": {
                "type": "object",
                "description": "A compose being requested",
                "properties": {
                    "content_type": {
                        "type": "string",
                        "description": "The content type of this compose"
                    },
                    "release_id": {
                        "type": "integer",
                        "description": "The database ID for the release being requested"
                    },
                    "request": {
                        "type": "string",
                        "description": "The request being requested"
                    },
                    "security": {
                        "type": "boolean",
                        "description": "true if this compose contains security updates"
                    }
                },
                "required": [
                    "content_type",
                    "release_id",
                    "request",
                    "security"
                ]
            }
        }
    }

