import tabulate

tprint = print  # noqa: T001


class Table(object):

    def __init__(self, data):
        self.data = data

    def show(self):
        tprint(self.data)


def build_table(metro, spec_builder=None):
    data = []
    instances = metro.instances
    theoretical = metro.theoretical
    ratio = metro.ratio
    for size, cost in metro.experimental.items():
        data.append((instances[size].label, cost, theoretical[size], ratio[size]))

    return Table(tabulate.tabulate(
        data,
        headers=['size', 'experimental', f'theoretical {metro.complexity.text}', 'ratio'],
        tablefmt="fancy_grid"
    ))
