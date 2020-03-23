TESTS = {
  "map<int|int>": {
    "object": [{
      "key": 123,
      "value": 123
    }]
  },
  "map<int|bool>": {
    "object": [{
      "key": 123,
      "value": True
    }]
  },
  "map<int|float>": {
    "object": [{
      "key": 123,
      "value": 123.5
    }]
  },
  "map<int|std::string>": {
    "object": [{
      "key": 123,
      "value": "434312some_random"
    }]
  },
  "map<int|TestEnum>": {
    "object": [{
      "key": 123,
      "value": "value2"
    }]
  },
  "map<int|const DataUnit*>": {
    "object": [{
      "key": 123,
      "value": "unit1"
    }]
  },
  "map<int|AllTypesChildren>": {
    "object": [{
      "key": 123,
      "value": {}
    }]
  },
  "map<int|intrusive_ptr<AllTypesChildren>>": {
    "object": [{
      "key": 123,
      "value": {
        "type": "AllTypesChildren"
      }
    }]
  },
  "map<int|std::vector<int>>": {
    "object": [{
      "key": 123,
      "value": [
        1,
        2,
        3,
        4
      ]
    }]
  },
  "map<int|std::vector<std::vector<bool>>>": {
    "object": [{
      "key": 123,
      "value": [
        [
          True,
          False
        ],
        [
          False,
          True
        ]
      ]
    }]
  },
  "map<int|std::map<int, int>>": {
    "object": [{
      "key": 123,
      "value": [{
          "key": 1,
          "value": 2
        },
        {
          "key": 2,
          "value": 3
        }
      ]
    }]
  },
  "map<bool|int>": {
    "object": [{
      "key": True,
      "value": 123
    }]
  },
  "map<bool|bool>": {
    "object": [{
      "key": True,
      "value": True
    }]
  },
  "map<bool|float>": {
    "object": [{
      "key": True,
      "value": 123.5
    }]
  },
  "map<bool|std::string>": {
    "object": [{
      "key": True,
      "value": "434312some_random"
    }]
  },
  "map<bool|TestEnum>": {
    "object": [{
      "key": True,
      "value": "value2"
    }]
  },
  "map<bool|const DataUnit*>": {
    "object": [{
      "key": True,
      "value": "unit1"
    }]
  },
  "map<bool|AllTypesChildren>": {
    "object": [{
      "key": True,
      "value": {}
    }]
  },
  "map<bool|intrusive_ptr<AllTypesChildren>>": {
    "object": [{
      "key": True,
      "value": {
        "type": "AllTypesChildren"
      }
    }]
  },
  "map<bool|std::vector<int>>": {
    "object": [{
      "key": True,
      "value": [
        1,
        2,
        3,
        4
      ]
    }]
  },
  "map<bool|std::vector<std::vector<bool>>>": {
    "object": [{
      "key": True,
      "value": [
        [
          True,
          False
        ],
        [
          False,
          True
        ]
      ]
    }]
  },
  "map<bool|std::map<int, int>>": {
    "object": [{
      "key": True,
      "value": [{
          "key": 1,
          "value": 2
        },
        {
          "key": 2,
          "value": 3
        }
      ]
    }]
  },
  "map<float|int>": {
    "object": [{
      "key": 123.5,
      "value": 123
    }]
  },
  "map<float|bool>": {
    "object": [{
      "key": 123.5,
      "value": True
    }]
  },
  "map<float|float>": {
    "object": [{
      "key": 123.5,
      "value": 123.5
    }]
  },
  "map<float|std::string>": {
    "object": [{
      "key": 123.5,
      "value": "434312some_random"
    }]
  },
  "map<float|TestEnum>": {
    "object": [{
      "key": 123.5,
      "value": "value2"
    }]
  },
  "map<float|const DataUnit*>": {
    "object": [{
      "key": 123.5,
      "value": "unit1"
    }]
  },
  "map<float|AllTypesChildren>": {
    "object": [{
      "key": 123.5,
      "value": {}
    }]
  },
  "map<float|intrusive_ptr<AllTypesChildren>>": {
    "object": [{
      "key": 123.5,
      "value": {
        "type": "AllTypesChildren"
      }
    }]
  },
  "map<float|std::vector<int>>": {
    "object": [{
      "key": 123.5,
      "value": [
        1,
        2,
        3,
        4
      ]
    }]
  },
  "map<float|std::vector<std::vector<bool>>>": {
    "object": [{
      "key": 123.5,
      "value": [
        [
          True,
          False
        ],
        [
          False,
          True
        ]
      ]
    }]
  },
  "map<float|std::map<int, int>>": {
    "object": [{
      "key": 123.5,
      "value": [{
          "key": 1,
          "value": 2
        },
        {
          "key": 2,
          "value": 3
        }
      ]
    }]
  },
  "map<std::string|int>": {
    "object": [{
      "key": "434312some_random",
      "value": 123
    }]
  },
  "map<std::string|bool>": {
    "object": [{
      "key": "434312some_random",
      "value": True
    }]
  },
  "map<std::string|float>": {
    "object": [{
      "key": "434312some_random",
      "value": 123.5
    }]
  },
  "map<std::string|std::string>": {
    "object": [{
      "key": "434312some_random",
      "value": "434312some_random"
    }]
  },
  "map<std::string|TestEnum>": {
    "object": [{
      "key": "434312some_random",
      "value": "value2"
    }]
  },
  "map<std::string|const DataUnit*>": {
    "object": [{
      "key": "434312some_random",
      "value": "unit1"
    }]
  },
  "map<std::string|AllTypesChildren>": {
    "object": [{
      "key": "434312some_random",
      "value": {}
    }]
  },
  "map<std::string|intrusive_ptr<AllTypesChildren>>": {
    "object": [{
      "key": "434312some_random",
      "value": {
        "type": "AllTypesChildren"
      }
    }]
  },
  "map<std::string|std::vector<int>>": {
    "object": [{
      "key": "434312some_random",
      "value": [
        1,
        2,
        3,
        4
      ]
    }]
  },
  "map<std::string|std::vector<std::vector<bool>>>": {
    "object": [{
      "key": "434312some_random",
      "value": [
        [
          True,
          False
        ],
        [
          False,
          True
        ]
      ]
    }]
  },
  "map<std::string|std::map<int, int>>": {
    "object": [{
      "key": "434312some_random",
      "value": [{
          "key": 1,
          "value": 2
        },
        {
          "key": 2,
          "value": 3
        }
      ]
    }]
  },
  "map<TestEnum|int>": {
    "object": [{
      "key": "value2",
      "value": 123
    }]
  },
  "map<TestEnum|bool>": {
    "object": [{
      "key": "value2",
      "value": True
    }]
  },
  "map<TestEnum|float>": {
    "object": [{
      "key": "value2",
      "value": 123.5
    }]
  },
  "map<TestEnum|std::string>": {
    "object": [{
      "key": "value2",
      "value": "434312some_random"
    }]
  },
  "map<TestEnum|TestEnum>": {
    "object": [{
      "key": "value2",
      "value": "value2"
    }]
  },
  "map<TestEnum|const DataUnit*>": {
    "object": [{
      "key": "value2",
      "value": "unit1"
    }]
  },
  "map<TestEnum|AllTypesChildren>": {
    "object": [{
      "key": "value2",
      "value": {}
    }]
  },
  "map<TestEnum|intrusive_ptr<AllTypesChildren>>": {
    "object": [{
      "key": "value2",
      "value": {
        "type": "AllTypesChildren"
      }
    }]
  },
  "map<TestEnum|std::vector<int>>": {
    "object": [{
      "key": "value2",
      "value": [
        1,
        2,
        3,
        4
      ]
    }]
  },
  "map<TestEnum|std::vector<std::vector<bool>>>": {
    "object": [{
      "key": "value2",
      "value": [
        [
          True,
          False
        ],
        [
          False,
          True
        ]
      ]
    }]
  },
  "map<TestEnum|std::map<int, int>>": {
    "object": [{
      "key": "value2",
      "value": [{
          "key": 1,
          "value": 2
        },
        {
          "key": 2,
          "value": 3
        }
      ]
    }]
  },
  "map<const DataUnit*|int>": {
    "object": [{
      "key": "unit1",
      "value": 123
    }]
  },
  "map<const DataUnit*|bool>": {
    "object": [{
      "key": "unit1",
      "value": True
    }]
  },
  "map<const DataUnit*|float>": {
    "object": [{
      "key": "unit1",
      "value": 123.5
    }]
  },
  "map<const DataUnit*|std::string>": {
    "object": [{
      "key": "unit1",
      "value": "434312some_random"
    }]
  },
  "map<const DataUnit*|TestEnum>": {
    "object": [{
      "key": "unit1",
      "value": "value2"
    }]
  },
  "map<const DataUnit*|const DataUnit*>": {
    "object": [{
      "key": "unit1",
      "value": "unit1"
    }]
  },
  "map<const DataUnit*|AllTypesChildren>": {
    "object": [{
      "key": "unit1",
      "value": {}
    }]
  },
  "map<const DataUnit*|intrusive_ptr<AllTypesChildren>>": {
    "object": [{
      "key": "unit1",
      "value": {
        "type": "AllTypesChildren"
      }
    }]
  },
  "map<const DataUnit*|std::vector<int>>": {
    "object": [{
      "key": "unit1",
      "value": [
        1,
        2,
        3,
        4
      ]
    }]
  },
  "map<const DataUnit*|std::vector<std::vector<bool>>>": {
    "object": [{
      "key": "unit1",
      "value": [
        [
          True,
          False
        ],
        [
          False,
          True
        ]
      ]
    }]
  },
  "map<const DataUnit*|std::map<int, int>>": {
    "object": [{
      "key": "unit1",
      "value": [{
          "key": 1,
          "value": 2
        },
        {
          "key": 2,
          "value": 3
        }
      ]
    }]
  },
  "map<AllTypesChildren|int>": {
    "object": [{
      "key": {},
      "value": 123
    }]
  },
  "map<AllTypesChildren|bool>": {
    "object": [{
      "key": {},
      "value": True
    }]
  },
  "map<AllTypesChildren|float>": {
    "object": [{
      "key": {},
      "value": 123.5
    }]
  },
  "map<AllTypesChildren|std::string>": {
    "object": [{
      "key": {},
      "value": "434312some_random"
    }]
  },
  "map<AllTypesChildren|TestEnum>": {
    "object": [{
      "key": {},
      "value": "value2"
    }]
  },
  "map<AllTypesChildren|const DataUnit*>": {
    "object": [{
      "key": {},
      "value": "unit1"
    }]
  },
  "map<AllTypesChildren|AllTypesChildren>": {
    "object": [{
      "key": {},
      "value": {}
    }]
  },
  "map<AllTypesChildren|intrusive_ptr<AllTypesChildren>>": {
    "object": [{
      "key": {},
      "value": {
        "type": "AllTypesChildren"
      }
    }]
  },
  "map<AllTypesChildren|std::vector<int>>": {
    "object": [{
      "key": {},
      "value": [
        1,
        2,
        3,
        4
      ]
    }]
  },
  "map<AllTypesChildren|std::vector<std::vector<bool>>>": {
    "object": [{
      "key": {},
      "value": [
        [
          True,
          False
        ],
        [
          False,
          True
        ]
      ]
    }]
  },
  "map<AllTypesChildren|std::map<int, int>>": {
    "object": [{
      "key": {},
      "value": [{
          "key": 1,
          "value": 2
        },
        {
          "key": 2,
          "value": 3
        }
      ]
    }]
  },
  "map<intrusive_ptr<AllTypesChildren>|int>": {
    "object": [{
      "key": {
        "type": "AllTypesChildren"
      },
      "value": 123
    }]
  },
  "map<intrusive_ptr<AllTypesChildren>|bool>": {
    "object": [{
      "key": {
        "type": "AllTypesChildren"
      },
      "value": True
    }]
  },
  "map<intrusive_ptr<AllTypesChildren>|float>": {
    "object": [{
      "key": {
        "type": "AllTypesChildren"
      },
      "value": 123.5
    }]
  },
  "map<intrusive_ptr<AllTypesChildren>|std::string>": {
    "object": [{
      "key": {
        "type": "AllTypesChildren"
      },
      "value": "434312some_random"
    }]
  },
  "map<intrusive_ptr<AllTypesChildren>|TestEnum>": {
    "object": [{
      "key": {
        "type": "AllTypesChildren"
      },
      "value": "value2"
    }]
  },
  "map<intrusive_ptr<AllTypesChildren>|const DataUnit*>": {
    "object": [{
      "key": {
        "type": "AllTypesChildren"
      },
      "value": "unit1"
    }]
  },
  "map<intrusive_ptr<AllTypesChildren>|AllTypesChildren>": {
    "object": [{
      "key": {
        "type": "AllTypesChildren"
      },
      "value": {}
    }]
  },
  "map<intrusive_ptr<AllTypesChildren>|intrusive_ptr<AllTypesChildren>>": {
    "object": [{
      "key": {
        "type": "AllTypesChildren"
      },
      "value": {
        "type": "AllTypesChildren"
      }
    }]
  },
  "map<intrusive_ptr<AllTypesChildren>|std::vector<int>>": {
    "object": [{
      "key": {
        "type": "AllTypesChildren"
      },
      "value": [
        1,
        2,
        3,
        4
      ]
    }]
  },
  "map<intrusive_ptr<AllTypesChildren>|std::vector<std::vector<bool>>>": {
    "object": [{
      "key": {
        "type": "AllTypesChildren"
      },
      "value": [
        [
          True,
          False
        ],
        [
          False,
          True
        ]
      ]
    }]
  },
  "map<intrusive_ptr<AllTypesChildren>|std::map<int, int>>": {
    "object": [{
      "key": {
        "type": "AllTypesChildren"
      },
      "value": [{
          "key": 1,
          "value": 2
        },
        {
          "key": 2,
          "value": 3
        }
      ]
    }]
  }
}