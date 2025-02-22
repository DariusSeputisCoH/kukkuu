# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["test_add_child_mutation 1"] = {
    "data": {
        "addChild": {
            "child": {
                "birthdate": "2020-11-11",
                "firstName": "Pekka",
                "lastName": "Perälä",
                "postalCode": "00820",
            }
        }
    }
}

snapshots["test_available_events_and_event_groups 1"] = {
    "data": {
        "child": {
            "availableEventsAndEventGroups": {
                "edges": [
                    {
                        "node": {
                            "__typename": "EventGroupNode",
                            "name": "this should be the first",
                        }
                    },
                    {
                        "node": {
                            "__typename": "EventNode",
                            "name": "this should be the second",
                        }
                    },
                    {
                        "node": {
                            "__typename": "EventGroupNode",
                            "name": "this should be the third",
                        }
                    },
                    {
                        "node": {
                            "__typename": "EventNode",
                            "name": "this should be the fourth",
                        }
                    },
                ]
            }
        }
    }
}

snapshots["test_child_query 1"] = {
    "data": {
        "child": {
            "birthdate": "2020-06-24",
            "firstName": "Michael",
            "lastName": "Patton",
            "postalCode": "55777",
            "relationships": {
                "edges": [
                    {
                        "node": {
                            "guardian": {
                                "email": "michellewalker@example.net",
                                "firstName": "Samantha",
                                "lastName": "Bryant",
                                "phoneNumber": "240-675-0649",
                            },
                            "type": "ADVOCATE",
                        }
                    }
                ]
            },
        }
    }
}

snapshots["test_child_query_not_own_child_project_user 1"] = {
    "data": {
        "child": {
            "birthdate": "2020-06-24",
            "firstName": "Michael",
            "lastName": "Patton",
            "postalCode": "55777",
            "relationships": {
                "edges": [
                    {
                        "node": {
                            "guardian": {
                                "email": "funderwood@example.com",
                                "firstName": "Blake",
                                "lastName": "Newton",
                                "phoneNumber": "976-380-3466x9727",
                            },
                            "type": "PARENT",
                        }
                    }
                ]
            },
        }
    }
}

snapshots["test_children_offset_pagination[10-None] 1"] = {
    "data": {
        "children": {
            "edges": [
                {"node": {"lastName": "0"}},
                {"node": {"lastName": "1"}},
                {"node": {"lastName": "2"}},
                {"node": {"lastName": "3"}},
                {"node": {"lastName": "4"}},
            ]
        }
    }
}

snapshots["test_children_offset_pagination[2-2] 1"] = {
    "data": {"children": {"edges": [{"node": {"lastName": "4"}}]}}
}

snapshots["test_children_offset_pagination[2-None] 1"] = {
    "data": {
        "children": {
            "edges": [{"node": {"lastName": "0"}}, {"node": {"lastName": "1"}}]
        }
    }
}

snapshots["test_children_offset_pagination[None-2] 1"] = {
    "data": {"children": {"edges": [{"node": {"lastName": "4"}}]}}
}

snapshots["test_children_offset_pagination[None-5] 1"] = {
    "data": {"children": {"edges": []}}
}

snapshots["test_children_project_filter 1"] = {
    "data": {
        "children": {
            "edges": [
                {"node": {"firstName": "Only I", "lastName": "Should be returned"}}
            ]
        }
    }
}

snapshots["test_children_query_normal_user 1"] = {
    "data": {
        "children": {
            "edges": [
                {
                    "node": {
                        "birthdate": "2020-06-24",
                        "firstName": "Michael",
                        "lastName": "Patton",
                        "postalCode": "55777",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "email": "michellewalker@example.net",
                                            "firstName": "Samantha",
                                            "lastName": "Bryant",
                                            "phoneNumber": "240-675-0649",
                                        },
                                        "type": "ADVOCATE",
                                    }
                                }
                            ]
                        },
                    }
                }
            ]
        }
    }
}

snapshots["test_children_query_ordering 1"] = {
    "data": {
        "children": {
            "edges": [
                {
                    "node": {
                        "createdAt": "2020-11-11T00:00:00+00:00",
                        "firstName": "",
                        "lastName": "",
                    }
                },
                {
                    "node": {
                        "createdAt": "2020-12-12T00:00:00+00:00",
                        "firstName": "",
                        "lastName": "",
                    }
                },
                {
                    "node": {
                        "createdAt": "2020-12-12T00:00:00+00:00",
                        "firstName": "Alpha",
                        "lastName": "",
                    }
                },
                {
                    "node": {
                        "createdAt": "2020-12-12T00:00:00+00:00",
                        "firstName": "Beta",
                        "lastName": "",
                    }
                },
                {
                    "node": {
                        "createdAt": "2020-11-11T00:00:00+00:00",
                        "firstName": "",
                        "lastName": "Korhonen",
                    }
                },
                {
                    "node": {
                        "createdAt": "2020-12-12T00:00:00+00:00",
                        "firstName": "",
                        "lastName": "Korhonen",
                    }
                },
                {
                    "node": {
                        "createdAt": "2020-12-12T00:00:00+00:00",
                        "firstName": "Beta",
                        "lastName": "Korhonen",
                    }
                },
                {
                    "node": {
                        "createdAt": "2020-12-12T00:00:00+00:00",
                        "firstName": "",
                        "lastName": "Virtanen",
                    }
                },
                {
                    "node": {
                        "createdAt": "2020-12-12T00:00:00+00:00",
                        "firstName": "Alpha",
                        "lastName": "Virtanen",
                    }
                },
                {
                    "node": {
                        "createdAt": "2020-12-12T00:00:00+00:00",
                        "firstName": "Beta",
                        "lastName": "Virtanen",
                    }
                },
            ]
        }
    }
}

snapshots["test_children_query_project_user 1"] = {
    "data": {
        "children": {
            "edges": [
                {
                    "node": {
                        "birthdate": "2020-05-21",
                        "firstName": "Same project",
                        "lastName": "Should be returned 1/1",
                        "postalCode": "73557",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "email": "jessica67@example.com",
                                            "firstName": "Blake",
                                            "lastName": "Newton",
                                            "phoneNumber": "976-380-3466x9727",
                                        },
                                        "type": "PARENT",
                                    }
                                }
                            ]
                        },
                    }
                }
            ]
        }
    }
}

snapshots["test_children_query_project_user_and_guardian 1"] = {
    "data": {
        "children": {
            "edges": [
                {
                    "node": {
                        "birthdate": "2020-11-15",
                        "firstName": "Own child same project",
                        "lastName": "Should be returned 1/3",
                        "postalCode": "50649",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "email": "michellewalker@example.net",
                                            "firstName": "Michael",
                                            "lastName": "Patton",
                                            "phoneNumber": "355.777.6712x406",
                                        },
                                        "type": "ADVOCATE",
                                    }
                                }
                            ]
                        },
                    }
                },
                {
                    "node": {
                        "birthdate": "2020-06-08",
                        "firstName": "Own child another project",
                        "lastName": "Should be returned 2/3",
                        "postalCode": "80346",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "email": "michellewalker@example.net",
                                            "firstName": "Michael",
                                            "lastName": "Patton",
                                            "phoneNumber": "355.777.6712x406",
                                        },
                                        "type": "ADVOCATE",
                                    }
                                }
                            ]
                        },
                    }
                },
                {
                    "node": {
                        "birthdate": "2020-08-09",
                        "firstName": "Not own child same project",
                        "lastName": "Should be returned 3/3",
                        "postalCode": "27011",
                        "relationships": {
                            "edges": [
                                {
                                    "node": {
                                        "guardian": {
                                            "email": "hernandezdennis@example.org",
                                            "firstName": "Sandra",
                                            "lastName": "Meyer",
                                            "phoneNumber": "072.770.8981",
                                        },
                                        "type": "ADVOCATE",
                                    }
                                }
                            ]
                        },
                    }
                },
            ]
        }
    }
}

snapshots["test_children_total_count[None] 1"] = {"data": {"children": {"count": 5}}}

snapshots["test_children_total_count[first] 1"] = {"data": {"children": {"count": 5}}}

snapshots["test_children_total_count[limit] 1"] = {"data": {"children": {"count": 5}}}

snapshots["test_delete_child_mutation 1"] = {
    "data": {"deleteChild": {"__typename": "DeleteChildMutationPayload"}}
}

snapshots["test_get_available_events 1"] = {
    "data": {
        "child": {
            "availableEvents": {
                "edges": [
                    {
                        "node": {
                            "createdAt": "2020-12-12T00:00:00+00:00",
                            "occurrences": {
                                "edges": [{"node": {"remainingCapacity": 46}}]
                            },
                        }
                    }
                ]
            },
            "occurrences": {"edges": [{"node": {"time": "2020-12-12T00:00:00+00:00"}}]},
            "pastEvents": {"edges": []},
        }
    }
}

snapshots["test_get_past_events 1"] = {
    "data": {
        "child": {
            "availableEvents": {"edges": []},
            "occurrences": {
                "edges": [
                    {"node": {"time": "2020-12-11T22:59:00+00:00"}},
                    {"node": {"time": "2020-12-11T23:01:00+00:00"}},
                ]
            },
            "pastEvents": {
                "edges": [
                    {
                        "node": {
                            "createdAt": "2020-12-12T00:00:00+00:00",
                            "name": "enrolled occurrence in the past",
                            "occurrences": {
                                "edges": [
                                    {"node": {"remainingCapacity": 12}},
                                    {"node": {"remainingCapacity": 13}},
                                ]
                            },
                        }
                    }
                ]
            },
        }
    }
}

snapshots["test_submit_children_and_guardian 1"] = {
    "data": {
        "submitChildrenAndGuardian": {
            "children": [
                {
                    "birthdate": "2020-01-01",
                    "firstName": "Matti",
                    "lastName": "Mainio",
                    "postalCode": "00840",
                    "relationships": {
                        "edges": [
                            {
                                "node": {
                                    "guardian": {
                                        "email": "michellewalker@example.net",
                                        "firstName": "Gulle",
                                        "lastName": "Guardian",
                                        "phoneNumber": "777-777777",
                                    },
                                    "type": "OTHER_GUARDIAN",
                                }
                            }
                        ]
                    },
                },
                {
                    "birthdate": "2020-02-02",
                    "firstName": "Jussi",
                    "lastName": "Juonio",
                    "postalCode": "00820",
                    "relationships": {
                        "edges": [
                            {
                                "node": {
                                    "guardian": {
                                        "email": "michellewalker@example.net",
                                        "firstName": "Gulle",
                                        "lastName": "Guardian",
                                        "phoneNumber": "777-777777",
                                    },
                                    "type": None,
                                }
                            }
                        ]
                    },
                },
            ],
            "guardian": {
                "email": "michellewalker@example.net",
                "firstName": "Gulle",
                "languagesSpokenAtHome": {
                    "edges": [
                        {"node": {"alpha3Code": "swe"}},
                        {"node": {"alpha3Code": "fin"}},
                    ]
                },
                "lastName": "Guardian",
                "phoneNumber": "777-777777",
            },
        }
    }
}

snapshots["test_submit_children_and_guardian_with_email 1"] = {
    "data": {
        "submitChildrenAndGuardian": {
            "children": [
                {
                    "birthdate": "2020-01-01",
                    "firstName": "Matti",
                    "lastName": "Mainio",
                    "postalCode": "00840",
                    "relationships": {
                        "edges": [
                            {
                                "node": {
                                    "guardian": {
                                        "email": "updated_email@example.com",
                                        "firstName": "Gulle",
                                        "lastName": "Guardian",
                                        "phoneNumber": "777-777777",
                                    },
                                    "type": "OTHER_GUARDIAN",
                                }
                            }
                        ]
                    },
                },
                {
                    "birthdate": "2020-02-02",
                    "firstName": "Jussi",
                    "lastName": "Juonio",
                    "postalCode": "00820",
                    "relationships": {
                        "edges": [
                            {
                                "node": {
                                    "guardian": {
                                        "email": "updated_email@example.com",
                                        "firstName": "Gulle",
                                        "lastName": "Guardian",
                                        "phoneNumber": "777-777777",
                                    },
                                    "type": None,
                                }
                            }
                        ]
                    },
                },
            ],
            "guardian": {
                "email": "updated_email@example.com",
                "firstName": "Gulle",
                "languagesSpokenAtHome": {"edges": []},
                "lastName": "Guardian",
                "phoneNumber": "777-777777",
            },
        }
    }
}

snapshots["test_upcoming_events_and_event_groups 1"] = {
    "data": {
        "child": {
            "upcomingEventsAndEventGroups": {
                "edges": [
                    {
                        "node": {
                            "__typename": "EventGroupNode",
                            "canChildEnroll": True,
                            "name": "This should be the first",
                        }
                    },
                    {
                        "node": {
                            "__typename": "EventNode",
                            "canChildEnroll": True,
                            "name": "This should be the second",
                        }
                    },
                    {
                        "node": {
                            "__typename": "EventGroupNode",
                            "canChildEnroll": True,
                            "name": "This should be the third",
                        }
                    },
                    {
                        "node": {
                            "__typename": "EventNode",
                            "canChildEnroll": True,
                            "name": "This should be the fourth",
                        }
                    },
                    {
                        "node": {
                            "__typename": "EventNode",
                            "canChildEnroll": False,
                            "name": "Enrolled event",
                        }
                    },
                    {
                        "node": {
                            "__typename": "EventGroupNode",
                            "canChildEnroll": False,
                            "name": "Event group with one of two events enrolled",
                        }
                    },
                ]
            }
        }
    }
}

snapshots["test_update_child_mutation 1"] = {
    "data": {
        "updateChild": {
            "child": {
                "birthdate": "2020-01-01",
                "firstName": "Matti",
                "lastName": "Mainio",
                "postalCode": "00840",
            }
        }
    }
}

snapshots["test_update_child_mutation_should_have_no_required_fields 1"] = {
    "data": {
        "updateChild": {
            "child": {
                "birthdate": "2020-06-10",
                "firstName": "Brandon",
                "lastName": "Adams",
                "postalCode": "27011",
            }
        }
    }
}
