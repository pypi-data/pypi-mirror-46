from almetro.instance import growing
from almetro.metro import Metro
import timeit


class ExecutionSettings:
    def __init__(self, trials=1, runs=1):
        if not trials or trials < 1:
            raise TypeError('#trials must be provided')
        if not runs or runs < 1:
            raise TypeError('#runs must be provided')
        self.trials = trials
        self.runs = runs

    @staticmethod
    def new():
        return ExecutionSettings()


class InstanceSettings:
    def __init__(self, instances=1, provider=growing()):
        if not instances:
            raise TypeError('#instances must be provided')
        if not provider:
            raise TypeError('provider must be provided')
        self.instances = instances
        self.provider = provider

    @staticmethod
    def new():
        return InstanceSettings()


class Al:

    def __init__(self, instance_settings=InstanceSettings.new(), execution_settings=ExecutionSettings.new()):
        if not instance_settings:
            raise TypeError('instance settings must be provided')
        if not execution_settings:
            raise TypeError('execution settings must be provided')
        self.__instance_settings = instance_settings
        self.__execution_settings = execution_settings

    def with_instances(self, instances, provider):
        return Al(instance_settings=InstanceSettings(instances, provider), execution_settings=self.__execution_settings)

    def with_execution(self, trials, runs):
        return Al(instance_settings=self.__instance_settings, execution_settings=ExecutionSettings(trials, runs))

    def metro(self, algorithm, complexity):
        metro = Metro.new(complexity)
        for _ in range(self.__instance_settings.instances):
            instance = self.__instance_settings.provider.new_instance()

            def runner():
                algorithm(**instance)
            metro.register(instance['size'], timeit.repeat(runner, number=self.__execution_settings.runs, repeat=self.__execution_settings.trials))
        return metro
