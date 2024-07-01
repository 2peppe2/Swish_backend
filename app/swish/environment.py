class Environment(object):
    def __init__(self, name, base_url, base_url_get):
        self.name = name
        self.base_url = base_url
        self.base_url_get = base_url_get

    def __str__(self):
        return self.name

    @staticmethod
    def parse_environment(environment):
        if isinstance(environment, Environment) or environment is None:
            return environment
        try:
            return Environment.All[environment]
        except KeyError:
            print("ERROR: Provided environment name is invalid")
            # raise ConfigurationError("Provided environment name is invalid")


Environment.Test = Environment(
    name="test",
    base_url="https://mss.cpc.getswish.net/swish-cpcapi/api/v2/",
    base_url_get="https://mss.cpc.getswish.net/swish-cpcapi/api/v1/",
)
Environment.Production = Environment(
    name="production",
    base_url="https://cpc.getswish.net/swish-cpcapi/api/v2/",
    base_url_get="https://mss.cpc.getswish.net/swish-cpcapi/api/v1/",
)
Environment.All = {
    "test": Environment.Test,
    "production": Environment.Production,
    "dev": Environment.Test,
}
