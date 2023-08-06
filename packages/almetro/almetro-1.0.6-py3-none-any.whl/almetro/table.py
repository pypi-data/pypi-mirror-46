import tabulate

tprint = print  # noqa: T001


class Table(object):

    def __init__(self, data):
        self.data = data

    def show(self):
        tprint(self.data)


def build_table(metro, spec_builder=None):
    data = []
    for n, cost in metro.experimental.items():
        data.append((n, cost, metro.theoretical[n], metro.ratio[n]))

    return Table(tabulate.tabulate(
        data,
        headers=['n', 'experimental', f'theoretical {metro.complexity.text}', 'ratio'],
        tablefmt="fancy_grid"
    ))
