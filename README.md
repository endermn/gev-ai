├── main.py                 
├── gev-ai/                 # Your main application package
│   ├── __init__.py        # Makes 'gevai' a Python package
│   ├── core/              # Core logic and orchestration
│   │   ├── __init__.py
│   │   ├── orchestrator.py # Manages the workflow and interaction between components
│   │   └── models.py      # Data models for system specs, prompts, responses, etc.
│   ├── services/          # External service integrations
│   │   ├── __init__.py
│   │   ├── genai_service.py # Handles interactions with the GenAI API
│   │   └── system_info.py   # Gathers system information (like fastfetch)
│   ├── utils/             # Utility functions
│   │   ├── __init__.py
│   │   └── history_parser.py # Handles parsing terminal history
│   └── exceptions.py      # Custom exceptions
└── tests/                 # Unit and integration tests
    ├── __init__.py
    ├── core/
    │   ├── __init__.py
    │   └── test_orchestrator.py
    ├── services/
    │   ├── __init__.py
    │   └── test_genai_service.py
    └── utils/
        ├── __init__.py
        └── test_history_parser.py
