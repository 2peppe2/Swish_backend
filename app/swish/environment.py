from typing import Dict, Optional

class Environment:
    Test = None
    Production = None
    All: Dict[str, 'Environment'] = {}

    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def parse_environment(environment: Optional['Environment']) -> Optional['Environment']:
        if isinstance(environment, Environment) or environment is None:
            return environment
        try:
            return Environment.All[environment]
        except KeyError:
            print("ERROR: Provided environment name is invalid")
            # raise ConfigurationError("Provided environment name is invalid")

# Now, initialize these attributes outside the class definition
Environment.Test = Environment( # type: ignore
    name="test",
    base_url="https://mss.cpc.getswish.net/swish-cpcapi/api/",
)
Environment.Production = Environment( # type: ignore
    name="production",
    base_url="https://cpc.getswish.net/swish-cpcapi/api/"
)
Environment.All = { # type: ignore
    "test": Environment.Test,
    "production": Environment.Production,
    "dev": Environment.Test,
}