JSON_TESTS = {
  "map<int|std::vector<float>>": {
    "object": [{
      "key": 123,
      "value": [
        1,
        2
      ]
    }]
  },
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
  },
  "map<int|std::vector<const DataUnit*>>": {
    "object": [{
      "key": 123,
      "value": [
        "unit1",
        "unit1"
      ]
    }]
  },
  "map<int|std::vector<intrusive_ptr<AllTypesChildren>>": {
    "object": [{
      "key": 123,
      "value": [{
        "type": "AllTypesChildren"
      },{
        "type": "AllTypesChildren"
      }]
    }]
  },

}


XML_TESTS = {
  "map<int|std::vector<AllTypesChildren>>": "<root><object><pair key='123'><value><item /><item /></value></pair></object></root>",
  "map<int|std::vector<const DataUnit*>>": "<root><object><pair key='123'><value><item value='unit1' /><item value='unit1' /></value></pair></object></root>",
  "map<int|std::vector<intrusive_ptr<AllTypesChildren>>": "<root><object><pair key='123'><value><AllTypesChildren /><AllTypesChildren /></value></pair></object></root>",
  "map<int|int>": "<root><object><pair key='123' value='123' /></object></root>",
  "map<int|bool>": "<root><object><pair key='123' value='true' /></object></root>",
  "map<int|float>": "<root><object><pair key='123' value='123.5' /></object></root>",
  "map<int|std::string>": "<root><object><pair key='123' value='434312some_random' /></object></root>",
  "map<int|TestEnum>": "<root><object><pair key='123' value='value2' /></object></root>",
  "map<int|const DataUnit*>": "<root><object><pair key='123' value='unit1' /></object></root>",
  "map<int|AllTypesChildren>": "<root><object><pair key='123'><value /></pair></object></root>",
  "map<int|intrusive_ptr<AllTypesChildren>>": "<root><object><pair key='123'><value type='AllTypesChildren' /></pair></object></root>",
  "map<int|std::vector<int>>": "<root><object><pair key='123'><value><item value='1' /><item value='2' /><item value='3' /><item value='4' /></value></pair></object></root>",
  "map<int|std::vector<std::vector<bool>>>": "<root><object><pair key='123'><value><item><item value='true' /><item /></item><item><item /><item value='true'/></item></value></pair></object></root>",
  "map<int|std::map<int, int>>": "<root><object><pair key='123'><value><pair key='1' value='2' /><pair key='2' value='3' /></value></pair></object></root>",
  "map<bool|int>": "<root><object><pair key='true' value='123' /></object></root>",
  "map<bool|bool>": "<root><object><pair key='true' value='true' /></object></root>",
  "map<bool|float>": "<root><object><pair key='true' value='123.5' /></object></root>",
  "map<bool|std::string>": "<root><object><pair key='true' value='434312some_random' /></object></root>",
  "map<bool|TestEnum>": "<root><object><pair key='true' value='value2' /></object></root>",
  "map<bool|const DataUnit*>": "<root><object><pair key='true' value='unit1' /></object></root>",
  "map<bool|AllTypesChildren>": "<root><object><pair key='true'><value /></pair></object></root>",
  "map<bool|intrusive_ptr<AllTypesChildren>>": "<root><object><pair key='true'><value type='AllTypesChildren' /></pair></object></root>",
  "map<bool|std::vector<int>>": "<root><object><pair key='true'><value><item value='1' /><item value='2' /><item value='3' /><item value='4' /></value></pair></object></root>",
  "map<bool|std::vector<std::vector<bool>>>": "<root><object><pair key='true'><value><item><item value='true' /><item /></item><item><item /><item value='true'/></item></value></pair></object></root>",
  "map<bool|std::map<int, int>>": "<root><object><pair key='true'><value><pair key='1' value='2' /><pair key='2' value='3' /></value></pair></object></root>",
  "map<float|int>": "<root><object><pair key='123.5' value='123' /></object></root>",
  "map<float|bool>": "<root><object><pair key='123.5' value='true' /></object></root>",
  "map<float|float>": "<root><object><pair key='123.5' value='123.5' /></object></root>",
  "map<float|std::string>": "<root><object><pair key='123.5' value='434312some_random' /></object></root>",
  "map<float|TestEnum>": "<root><object><pair key='123.5' value='value2' /></object></root>",
  "map<float|const DataUnit*>": "<root><object><pair key='123.5' value='unit1' /></object></root>",
  "map<float|AllTypesChildren>": "<root><object><pair key='123.5'><value /></pair></object></root>",
  "map<float|intrusive_ptr<AllTypesChildren>>": "<root><object><pair key='123.5'><value type='AllTypesChildren' /></pair></object></root>",
  "map<float|std::vector<int>>": "<root><object><pair key='123.5'><value><item value='1' /><item value='2' /><item value='3' /><item value='4' /></value></pair></object></root>",
  "map<float|std::vector<std::vector<bool>>>": "<root><object><pair key='123.5'><value><item><item value='true' /><item /></item><item><item /><item value='true' /></item></value></pair></object></root>",
  "map<float|std::map<int, int>>": "<root><object><pair key='123.5'><value><pair key='1' value='2' /><pair key='2' value='3' /></value></pair></object></root>",
  "map<std::string|int>": "<root><object><pair key='434312some_random' value='123' /></object></root>",
  "map<std::string|bool>": "<root><object><pair key='434312some_random' value='true' /></object></root>",
  "map<std::string|float>": "<root><object><pair key='434312some_random' value='123.5' /></object></root>",
  "map<std::string|std::string>": "<root><object><pair key='434312some_random' value='434312some_random' /></object></root>",
  "map<std::string|TestEnum>": "<root><object><pair key='434312some_random' value='value2' /></object></root>",
  "map<std::string|const DataUnit*>": "<root><object><pair key='434312some_random' value='unit1' /></object></root>",
  "map<std::string|AllTypesChildren>": "<root><object><pair key='434312some_random'><value /></pair></object></root>",
  "map<std::string|intrusive_ptr<AllTypesChildren>>": "<root><object><pair key='434312some_random'><value type='AllTypesChildren' /></pair></object></root>",
  "map<std::string|std::vector<int>>": "<root><object><pair key='434312some_random'><value><item value='1' /><item value='2' /><item value='3' /><item value='4' /></value></pair></object></root>",
  "map<std::string|std::vector<std::vector<bool>>>": "<root><object><pair key='434312some_random'><value><item><item value='true' /><item /></item><item><item /><item value='true' /></item></value></pair></object></root>",
  "map<std::string|std::map<int, int>>": "<root><object><pair key='434312some_random'><value><pair key='1' value='2' /><pair key='2' value='3' /></value></pair></object></root>",
  "map<TestEnum|int>": "<root><object><pair key='value2' value='123' /></object></root>",
  "map<TestEnum|bool>": "<root><object><pair key='value2' value='true' /></object></root>",
  "map<TestEnum|float>": "<root><object><pair key='value2' value='123.5' /></object></root>",
  "map<TestEnum|std::string>": "<root><object><pair key='value2' value='434312some_random' /></object></root>",
  "map<TestEnum|TestEnum>": "<root><object><pair key='value2' value='value2' /></object></root>",
  "map<TestEnum|const DataUnit*>": "<root><object><pair key='value2' value='unit1' /></object></root>",
  "map<TestEnum|AllTypesChildren>": "<root><object><pair key='value2'><value /></pair></object></root>",
  "map<TestEnum|intrusive_ptr<AllTypesChildren>>": "<root><object><pair key='value2'><value type='AllTypesChildren' /></pair></object></root>",
  "map<TestEnum|std::vector<int>>": "<root><object><pair key='value2'><value><item value='1' /><item value='2' /><item value='3' /><item value='4' /></value></pair></object></root>",
  "map<TestEnum|std::vector<std::vector<bool>>>": "<root><object><pair key='value2'><value><item><item value='true' /><item /></item><item><item /><item value='true' /></item></value></pair></object></root>",
  "map<TestEnum|std::map<int, int>>": "<root><object><pair key='value2'><value><pair key='1' value='2' /><pair key='2' value='3' /></value></pair></object></root>",
  "map<const DataUnit*|int>": "<root><object><pair key='unit1' value='123' /></object></root>",
  "map<const DataUnit*|bool>": "<root><object><pair key='unit1' value='true' /></object></root>",
  "map<const DataUnit*|float>": "<root><object><pair key='unit1' value='123.5' /></object></root>",
  "map<const DataUnit*|std::string>": "<root><object><pair key='unit1' value='434312some_random' /></object></root>",
  "map<const DataUnit*|TestEnum>": "<root><object><pair key='unit1' value='value2' /></object></root>",
  "map<const DataUnit*|const DataUnit*>": "<root><object><pair key='unit1' value='unit1' /></object></root>",
  "map<const DataUnit*|AllTypesChildren>": "<root><object><pair key='unit1'><value /></pair></object></root>",
  "map<const DataUnit*|intrusive_ptr<AllTypesChildren>>": "<root><object><pair key='unit1'><value type='AllTypesChildren' /></pair></object></root>",
  "map<const DataUnit*|std::vector<int>>": "<root><object><pair key='unit1'><value><item value='1' /><item value='2' /><item value='3' /><item value='4' /></value></pair></object></root>",
  "map<const DataUnit*|std::vector<std::vector<bool>>>": "<root><object><pair key='unit1'><value><item><item value='true' /><item /></item><item><item /><item value='true' /></item></value></pair></object></root>",
  "map<const DataUnit*|std::map<int, int>>": "<root><object><pair key='unit1'><value><pair key='1' value='2' /><pair key='2' value='3' /></value></pair></object></root>",
  "map<AllTypesChildren|int>": "<root><object><pair value='123'><key /></pair></object></root>",
  "map<AllTypesChildren|bool>": "<root><object><pair value='true'><key /></pair></object></root>",
  "map<AllTypesChildren|float>": "<root><object><pair value='123.5'><key /></pair></object></root>",
  "map<AllTypesChildren|std::string>": "<root><object><pair value='434312some_random'><key /></pair></object></root>",
  "map<AllTypesChildren|TestEnum>": "<root><object><pair value='value2'><key /></pair></object></root>",
  "map<AllTypesChildren|const DataUnit*>": "<root><object><pair value='unit1'><key /></pair></object></root>",
  "map<AllTypesChildren|AllTypesChildren>": "<root><object><pair><key /><value /></pair></object></root>",
  "map<AllTypesChildren|intrusive_ptr<AllTypesChildren>>": "<root><object><pair><key /><value type='AllTypesChildren' /></pair></object></root>",
  "map<AllTypesChildren|std::vector<int>>": "<root><object><pair><key /><value><item value='1' /><item value='2' /><item value='3' /><item value='4' /></value></pair></object></root>",
  "map<AllTypesChildren|std::vector<std::vector<bool>>>": "<root><object><pair><key /><value><item><item value='true' /><item /></item><item><item /><item value='true' /></item></value></pair></object></root>",
  "map<AllTypesChildren|std::map<int, int>>": "<root><object><pair><key /><value><pair key='1' value='2' /><pair key='2' value='3' /></value></pair></object></root>",
  "map<intrusive_ptr<AllTypesChildren>|int>": "<root><object><pair value='123'><key type='AllTypesChildren' /></pair></object></root>",
  "map<intrusive_ptr<AllTypesChildren>|bool>": "<root><object><pair value='true'><key type='AllTypesChildren' /></pair></object></root>",
  "map<intrusive_ptr<AllTypesChildren>|float>": "<root><object><pair value='123.5'><key type='AllTypesChildren' /></pair></object></root>",
  "map<intrusive_ptr<AllTypesChildren>|std::string>": "<root><object><pair value='434312some_random'><key type='AllTypesChildren' /></pair></object></root>",
  "map<intrusive_ptr<AllTypesChildren>|TestEnum>": "<root><object><pair value='value2'><key type='AllTypesChildren' /></pair></object></root>",
  "map<intrusive_ptr<AllTypesChildren>|const DataUnit*>": "<root><object><pair value='unit1'><key type='AllTypesChildren' /></pair></object></root>",
  "map<intrusive_ptr<AllTypesChildren>|AllTypesChildren>": "<root><object><pair><key type='AllTypesChildren' /><value /></pair></object></root>",
  "map<intrusive_ptr<AllTypesChildren>|intrusive_ptr<AllTypesChildren>>": "<root><object><pair><key type='AllTypesChildren' /><value type='AllTypesChildren' /></pair></object></root>",
  "map<intrusive_ptr<AllTypesChildren>|std::vector<int>>": "<root><object><pair><key type='AllTypesChildren' /><value><item value='1' /><item value='2' /><item value='3' /><item value='4' /></value></pair></object></root>",
  "map<intrusive_ptr<AllTypesChildren>|std::vector<std::vector<bool>>>": "<root><object><pair><key type='AllTypesChildren' /><value><item><item value='true' /><item /></item><item><item /><item value='true' /></item></value></pair></object></root>",
  "map<intrusive_ptr<AllTypesChildren>|std::map<int, int>>": "<root><object><pair><key type='AllTypesChildren' /><value><pair key='1' value='2' /><pair key='2' value='3' /></value></pair></object></root>",
}
