import tabulate


def build_table(metro, spec_builder=None):
    data = []
    for n, cost in metro.experimental.items():
        data.append((n, cost, metro.theoretical[n], metro.ratio[n]))

    return tabulate.tabulate(
        data,
        headers=['n', 'experimental', f'theoretical {metro.complexity.text}', 'ratio'],
        tablefmt="fancy_grid"
    )
