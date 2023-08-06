bodhi.update.comment
--------------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.update.comment#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when a comment is added to an update",
        "type": "object",
        "properties": {
            "comment": {
                "type": "object",
                "description": "The comment added to an update",
                "properties": {
                    "karma": {
                        "type": "integer",
                        "description": "The karma associated with the comment"
                    },
                    "text": {
                        "type": "string",
                        "description": "The text of the comment"
                    },
                    "timestamp": {
                        "type": "string",
                        "description": "The timestamp that the comment was left on."
                    },
                    "update": {
                        "type": "object",
                        "description": "An update",
                        "properties": {
                            "alias": {
                                "type": "string",
                                "description": "The alias of the update"
                            },
                            "builds": {
                                "type": "array",
                                "description": "A list of builds included in this update",
                                "items": {
                                    "$ref": "#/definitions/build"
                                }
                            },
                            "request": {
                                "type": [
                                    "null",
                                    "string"
                                ],
                                "description": "The request of the update, if any",
                                "enum": [
                                    null,
                                    "testing",
                                    "obsolete",
                                    "unpush",
                                    "revoke",
                                    "stable"
                                ]
                            },
                            "status": {
                                "type": "string",
                                "description": "The current status of the update",
                                "enum": [
                                    null,
                                    "pending",
                                    "testing",
                                    "stable",
                                    "unpushed",
                                    "obsolete",
                                    "side_tag_active",
                                    "side_tag_expired"
                                ]
                            },
                            "user": {
                                "type": "object",
                                "description": "The user that submitted the override",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The user's account name"
                                    }
                                },
                                "required": [
                                    "name"
                                ]
                            }
                        },
                        "required": [
                            "alias",
                            "builds",
                            "request",
                            "status",
                            "user"
                        ]
                    },
                    "user": {
                        "type": "object",
                        "description": "The user that submitted the override",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The user's account name"
                            }
                        },
                        "required": [
                            "name"
                        ]
                    }
                },
                "required": [
                    "karma",
                    "text",
                    "timestamp",
                    "update",
                    "user"
                ]
            }
        },
        "required": [
            "comment"
        ],
        "definitions": {
            "build": {
                "type": "object",
                "description": "A build",
                "properties": {
                    "nvr": {
                        "type": "string",
                        "description": "The nvr the identifies the build in koji"
                    }
                },
                "required": [
                    "nvr"
                ]
            }
        }
    }

bodhi.update.complete.stable
----------------------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.update.complete.stable#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when an update is pushed stable",
        "type": "object",
        "properties": {
            "update": {
                "type": "object",
                "description": "An update",
                "properties": {
                    "alias": {
                        "type": "string",
                        "description": "The alias of the update"
                    },
                    "builds": {
                        "type": "array",
                        "description": "A list of builds included in this update",
                        "items": {
                            "$ref": "#/definitions/build"
                        }
                    },
                    "request": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "description": "The request of the update, if any",
                        "enum": [
                            null,
                            "testing",
                            "obsolete",
                            "unpush",
                            "revoke",
                            "stable"
                        ]
                    },
                    "status": {
                        "type": "string",
                        "description": "The current status of the update",
                        "enum": [
                            null,
                            "pending",
                            "testing",
                            "stable",
                            "unpushed",
                            "obsolete",
                            "side_tag_active",
                            "side_tag_expired"
                        ]
                    },
                    "user": {
                        "type": "object",
                        "description": "The user that submitted the override",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The user's account name"
                            }
                        },
                        "required": [
                            "name"
                        ]
                    }
                },
                "required": [
                    "alias",
                    "builds",
                    "request",
                    "status",
                    "user"
                ]
            }
        },
        "required": [
            "update"
        ],
        "definitions": {
            "build": {
                "type": "object",
                "description": "A build",
                "properties": {
                    "nvr": {
                        "type": "string",
                        "description": "The nvr the identifies the build in koji"
                    }
                },
                "required": [
                    "nvr"
                ]
            }
        }
    }

bodhi.update.complete.testing
-----------------------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.update.complete.testing#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when an update is pushed to testing",
        "type": "object",
        "properties": {
            "update": {
                "type": "object",
                "description": "An update",
                "properties": {
                    "alias": {
                        "type": "string",
                        "description": "The alias of the update"
                    },
                    "builds": {
                        "type": "array",
                        "description": "A list of builds included in this update",
                        "items": {
                            "$ref": "#/definitions/build"
                        }
                    },
                    "request": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "description": "The request of the update, if any",
                        "enum": [
                            null,
                            "testing",
                            "obsolete",
                            "unpush",
                            "revoke",
                            "stable"
                        ]
                    },
                    "status": {
                        "type": "string",
                        "description": "The current status of the update",
                        "enum": [
                            null,
                            "pending",
                            "testing",
                            "stable",
                            "unpushed",
                            "obsolete",
                            "side_tag_active",
                            "side_tag_expired"
                        ]
                    },
                    "user": {
                        "type": "object",
                        "description": "The user that submitted the override",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The user's account name"
                            }
                        },
                        "required": [
                            "name"
                        ]
                    }
                },
                "required": [
                    "alias",
                    "builds",
                    "request",
                    "status",
                    "user"
                ]
            }
        },
        "required": [
            "update"
        ],
        "definitions": {
            "build": {
                "type": "object",
                "description": "A build",
                "properties": {
                    "nvr": {
                        "type": "string",
                        "description": "The nvr the identifies the build in koji"
                    }
                },
                "required": [
                    "nvr"
                ]
            }
        }
    }

bodhi.update.edit
-----------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.update.edit#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when an update is edited",
        "type": "object",
        "properties": {
            "agent": {
                "type": "string",
                "description": "The user who edited the update"
            },
            "update": {
                "type": "object",
                "description": "An update",
                "properties": {
                    "alias": {
                        "type": "string",
                        "description": "The alias of the update"
                    },
                    "builds": {
                        "type": "array",
                        "description": "A list of builds included in this update",
                        "items": {
                            "$ref": "#/definitions/build"
                        }
                    },
                    "request": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "description": "The request of the update, if any",
                        "enum": [
                            null,
                            "testing",
                            "obsolete",
                            "unpush",
                            "revoke",
                            "stable"
                        ]
                    },
                    "status": {
                        "type": "string",
                        "description": "The current status of the update",
                        "enum": [
                            null,
                            "pending",
                            "testing",
                            "stable",
                            "unpushed",
                            "obsolete",
                            "side_tag_active",
                            "side_tag_expired"
                        ]
                    },
                    "user": {
                        "type": "object",
                        "description": "The user that submitted the override",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The user's account name"
                            }
                        },
                        "required": [
                            "name"
                        ]
                    }
                },
                "required": [
                    "alias",
                    "builds",
                    "request",
                    "status",
                    "user"
                ]
            }
        },
        "required": [
            "agent",
            "update"
        ],
        "definitions": {
            "build": {
                "type": "object",
                "description": "A build",
                "properties": {
                    "nvr": {
                        "type": "string",
                        "description": "The nvr the identifies the build in koji"
                    }
                },
                "required": [
                    "nvr"
                ]
            }
        }
    }

bodhi.update.eject
------------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.update.eject#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when an update is ejected from a compose",
        "type": "object",
        "properties": {
            "reason": {
                "type": "string",
                "description": "The reason the update was ejected"
            },
            "repo": {
                "type": "string",
                "description": "The name of the repo that the update is associated with"
            },
            "update": {
                "type": "object",
                "description": "An update",
                "properties": {
                    "alias": {
                        "type": "string",
                        "description": "The alias of the update"
                    },
                    "builds": {
                        "type": "array",
                        "description": "A list of builds included in this update",
                        "items": {
                            "$ref": "#/definitions/build"
                        }
                    },
                    "request": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "description": "The request of the update, if any",
                        "enum": [
                            null,
                            "testing",
                            "obsolete",
                            "unpush",
                            "revoke",
                            "stable"
                        ]
                    },
                    "status": {
                        "type": "string",
                        "description": "The current status of the update",
                        "enum": [
                            null,
                            "pending",
                            "testing",
                            "stable",
                            "unpushed",
                            "obsolete",
                            "side_tag_active",
                            "side_tag_expired"
                        ]
                    },
                    "user": {
                        "type": "object",
                        "description": "The user that submitted the override",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The user's account name"
                            }
                        },
                        "required": [
                            "name"
                        ]
                    }
                },
                "required": [
                    "alias",
                    "builds",
                    "request",
                    "status",
                    "user"
                ]
            }
        },
        "required": [
            "reason",
            "repo",
            "update"
        ],
        "definitions": {
            "build": {
                "type": "object",
                "description": "A build",
                "properties": {
                    "nvr": {
                        "type": "string",
                        "description": "The nvr the identifies the build in koji"
                    }
                },
                "required": [
                    "nvr"
                ]
            }
        }
    }

bodhi.update.karma.threshold.reach
----------------------------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.update.karma.threshold.reach#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when an update reaches its karma threshold",
        "type": "object",
        "properties": {
            "status": {
                "type": "string",
                "description": "Which karma threshold was reached",
                "enum": [
                    "stable",
                    "unstable"
                ]
            },
            "update": {
                "type": "object",
                "description": "An update",
                "properties": {
                    "alias": {
                        "type": "string",
                        "description": "The alias of the update"
                    },
                    "builds": {
                        "type": "array",
                        "description": "A list of builds included in this update",
                        "items": {
                            "$ref": "#/definitions/build"
                        }
                    },
                    "request": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "description": "The request of the update, if any",
                        "enum": [
                            null,
                            "testing",
                            "obsolete",
                            "unpush",
                            "revoke",
                            "stable"
                        ]
                    },
                    "status": {
                        "type": "string",
                        "description": "The current status of the update",
                        "enum": [
                            null,
                            "pending",
                            "testing",
                            "stable",
                            "unpushed",
                            "obsolete",
                            "side_tag_active",
                            "side_tag_expired"
                        ]
                    },
                    "user": {
                        "type": "object",
                        "description": "The user that submitted the override",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The user's account name"
                            }
                        },
                        "required": [
                            "name"
                        ]
                    }
                },
                "required": [
                    "alias",
                    "builds",
                    "request",
                    "status",
                    "user"
                ]
            }
        },
        "required": [
            "status",
            "update"
        ],
        "definitions": {
            "build": {
                "type": "object",
                "description": "A build",
                "properties": {
                    "nvr": {
                        "type": "string",
                        "description": "The nvr the identifies the build in koji"
                    }
                },
                "required": [
                    "nvr"
                ]
            }
        }
    }

bodhi.update.request.obsolete
-----------------------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.update.request.obsolete#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when an update is obsoleted",
        "type": "object",
        "properties": {
            "agent": {
                "type": "string",
                "description": "The user who requested the update to be obsoleted"
            },
            "update": {
                "type": "object",
                "description": "An update",
                "properties": {
                    "alias": {
                        "type": "string",
                        "description": "The alias of the update"
                    },
                    "builds": {
                        "type": "array",
                        "description": "A list of builds included in this update",
                        "items": {
                            "$ref": "#/definitions/build"
                        }
                    },
                    "request": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "description": "The request of the update, if any",
                        "enum": [
                            null,
                            "testing",
                            "obsolete",
                            "unpush",
                            "revoke",
                            "stable"
                        ]
                    },
                    "status": {
                        "type": "string",
                        "description": "The current status of the update",
                        "enum": [
                            null,
                            "pending",
                            "testing",
                            "stable",
                            "unpushed",
                            "obsolete",
                            "side_tag_active",
                            "side_tag_expired"
                        ]
                    },
                    "user": {
                        "type": "object",
                        "description": "The user that submitted the override",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The user's account name"
                            }
                        },
                        "required": [
                            "name"
                        ]
                    }
                },
                "required": [
                    "alias",
                    "builds",
                    "request",
                    "status",
                    "user"
                ]
            }
        },
        "required": [
            "agent",
            "update"
        ],
        "definitions": {
            "build": {
                "type": "object",
                "description": "A build",
                "properties": {
                    "nvr": {
                        "type": "string",
                        "description": "The nvr the identifies the build in koji"
                    }
                },
                "required": [
                    "nvr"
                ]
            }
        }
    }

bodhi.update.request.revoke
---------------------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.update.request.revoke#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when an update is revoked",
        "type": "object",
        "properties": {
            "agent": {
                "type": "string",
                "description": "The user who requested the update to be revoked"
            },
            "update": {
                "type": "object",
                "description": "An update",
                "properties": {
                    "alias": {
                        "type": "string",
                        "description": "The alias of the update"
                    },
                    "builds": {
                        "type": "array",
                        "description": "A list of builds included in this update",
                        "items": {
                            "$ref": "#/definitions/build"
                        }
                    },
                    "request": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "description": "The request of the update, if any",
                        "enum": [
                            null,
                            "testing",
                            "obsolete",
                            "unpush",
                            "revoke",
                            "stable"
                        ]
                    },
                    "status": {
                        "type": "string",
                        "description": "The current status of the update",
                        "enum": [
                            null,
                            "pending",
                            "testing",
                            "stable",
                            "unpushed",
                            "obsolete",
                            "side_tag_active",
                            "side_tag_expired"
                        ]
                    },
                    "user": {
                        "type": "object",
                        "description": "The user that submitted the override",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The user's account name"
                            }
                        },
                        "required": [
                            "name"
                        ]
                    }
                },
                "required": [
                    "alias",
                    "builds",
                    "request",
                    "status",
                    "user"
                ]
            }
        },
        "required": [
            "agent",
            "update"
        ],
        "definitions": {
            "build": {
                "type": "object",
                "description": "A build",
                "properties": {
                    "nvr": {
                        "type": "string",
                        "description": "The nvr the identifies the build in koji"
                    }
                },
                "required": [
                    "nvr"
                ]
            }
        }
    }

bodhi.update.request.stable
---------------------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.update.request.stable#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when an update is requested stable",
        "type": "object",
        "properties": {
            "agent": {
                "type": "string",
                "description": "The user who requested the update to be stable"
            },
            "update": {
                "type": "object",
                "description": "An update",
                "properties": {
                    "alias": {
                        "type": "string",
                        "description": "The alias of the update"
                    },
                    "builds": {
                        "type": "array",
                        "description": "A list of builds included in this update",
                        "items": {
                            "$ref": "#/definitions/build"
                        }
                    },
                    "request": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "description": "The request of the update, if any",
                        "enum": [
                            null,
                            "testing",
                            "obsolete",
                            "unpush",
                            "revoke",
                            "stable"
                        ]
                    },
                    "status": {
                        "type": "string",
                        "description": "The current status of the update",
                        "enum": [
                            null,
                            "pending",
                            "testing",
                            "stable",
                            "unpushed",
                            "obsolete",
                            "side_tag_active",
                            "side_tag_expired"
                        ]
                    },
                    "user": {
                        "type": "object",
                        "description": "The user that submitted the override",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The user's account name"
                            }
                        },
                        "required": [
                            "name"
                        ]
                    }
                },
                "required": [
                    "alias",
                    "builds",
                    "request",
                    "status",
                    "user"
                ]
            }
        },
        "required": [
            "agent",
            "update"
        ],
        "definitions": {
            "build": {
                "type": "object",
                "description": "A build",
                "properties": {
                    "nvr": {
                        "type": "string",
                        "description": "The nvr the identifies the build in koji"
                    }
                },
                "required": [
                    "nvr"
                ]
            }
        }
    }

bodhi.update.request.testing
----------------------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.update.request.testing#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when an update is requested testing",
        "type": "object",
        "properties": {
            "agent": {
                "type": "string",
                "description": "The user who requested the update to be tested"
            },
            "update": {
                "type": "object",
                "description": "An update",
                "properties": {
                    "alias": {
                        "type": "string",
                        "description": "The alias of the update"
                    },
                    "builds": {
                        "type": "array",
                        "description": "A list of builds included in this update",
                        "items": {
                            "$ref": "#/definitions/build"
                        }
                    },
                    "request": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "description": "The request of the update, if any",
                        "enum": [
                            null,
                            "testing",
                            "obsolete",
                            "unpush",
                            "revoke",
                            "stable"
                        ]
                    },
                    "status": {
                        "type": "string",
                        "description": "The current status of the update",
                        "enum": [
                            null,
                            "pending",
                            "testing",
                            "stable",
                            "unpushed",
                            "obsolete",
                            "side_tag_active",
                            "side_tag_expired"
                        ]
                    },
                    "user": {
                        "type": "object",
                        "description": "The user that submitted the override",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The user's account name"
                            }
                        },
                        "required": [
                            "name"
                        ]
                    }
                },
                "required": [
                    "alias",
                    "builds",
                    "request",
                    "status",
                    "user"
                ]
            }
        },
        "required": [
            "agent",
            "update"
        ],
        "definitions": {
            "build": {
                "type": "object",
                "description": "A build",
                "properties": {
                    "nvr": {
                        "type": "string",
                        "description": "The nvr the identifies the build in koji"
                    }
                },
                "required": [
                    "nvr"
                ]
            }
        }
    }

bodhi.update.request.unpush
---------------------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.update.request.unpush#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when an update is unpushed",
        "type": "object",
        "properties": {
            "agent": {
                "type": "string",
                "description": "The user who requested the update to be unpushed"
            },
            "update": {
                "type": "object",
                "description": "An update",
                "properties": {
                    "alias": {
                        "type": "string",
                        "description": "The alias of the update"
                    },
                    "builds": {
                        "type": "array",
                        "description": "A list of builds included in this update",
                        "items": {
                            "$ref": "#/definitions/build"
                        }
                    },
                    "request": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "description": "The request of the update, if any",
                        "enum": [
                            null,
                            "testing",
                            "obsolete",
                            "unpush",
                            "revoke",
                            "stable"
                        ]
                    },
                    "status": {
                        "type": "string",
                        "description": "The current status of the update",
                        "enum": [
                            null,
                            "pending",
                            "testing",
                            "stable",
                            "unpushed",
                            "obsolete",
                            "side_tag_active",
                            "side_tag_expired"
                        ]
                    },
                    "user": {
                        "type": "object",
                        "description": "The user that submitted the override",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The user's account name"
                            }
                        },
                        "required": [
                            "name"
                        ]
                    }
                },
                "required": [
                    "alias",
                    "builds",
                    "request",
                    "status",
                    "user"
                ]
            }
        },
        "required": [
            "agent",
            "update"
        ],
        "definitions": {
            "build": {
                "type": "object",
                "description": "A build",
                "properties": {
                    "nvr": {
                        "type": "string",
                        "description": "The nvr the identifies the build in koji"
                    }
                },
                "required": [
                    "nvr"
                ]
            }
        }
    }

bodhi.update.requirements_met.stable
------------------------------------
::

    {
        "id": "https://bodhi.fedoraproject.org/message-schemas/v1/bodhi.update.requirements_met.stable#",
        "$schema": "http://json-schema.org/draft-04/schema#",
        "description": "Schema for message sent when an update meets stable requirements",
        "type": "object",
        "properties": {
            "update": {
                "type": "object",
                "description": "An update",
                "properties": {
                    "alias": {
                        "type": "string",
                        "description": "The alias of the update"
                    },
                    "builds": {
                        "type": "array",
                        "description": "A list of builds included in this update",
                        "items": {
                            "$ref": "#/definitions/build"
                        }
                    },
                    "request": {
                        "type": [
                            "null",
                            "string"
                        ],
                        "description": "The request of the update, if any",
                        "enum": [
                            null,
                            "testing",
                            "obsolete",
                            "unpush",
                            "revoke",
                            "stable"
                        ]
                    },
                    "status": {
                        "type": "string",
                        "description": "The current status of the update",
                        "enum": [
                            null,
                            "pending",
                            "testing",
                            "stable",
                            "unpushed",
                            "obsolete",
                            "side_tag_active",
                            "side_tag_expired"
                        ]
                    },
                    "user": {
                        "type": "object",
                        "description": "The user that submitted the override",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "The user's account name"
                            }
                        },
                        "required": [
                            "name"
                        ]
                    }
                },
                "required": [
                    "alias",
                    "builds",
                    "request",
                    "status",
                    "user"
                ]
            }
        },
        "required": [
            "update"
        ],
        "definitions": {
            "build": {
                "type": "object",
                "description": "A build",
                "properties": {
                    "nvr": {
                        "type": "string",
                        "description": "The nvr the identifies the build in koji"
                    }
                },
                "required": [
                    "nvr"
                ]
            }
        }
    }

