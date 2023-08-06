def spec_line(data, label, color):
    return {'data': data, 'label': label, 'color': color}


def spec_axis(title, lines):
    return {'title': title, 'lines': lines}


def spec_chart(title, axes):
    return {'title': title, 'axes': axes}


def experimental_with_ratio_spec(metro, complexity):
    return spec_chart(
        '~ Elapsed time {} in seconds'.format(metro.elapsed_time),
        [
            spec_axis(
                'Experimental',
                [
                    spec_line(metro.ratio, r'ratio: $\mathcal{T}/\mathcal{O}$', 'tab:green'),
                    spec_line(metro.experimental, r'experimental: $\mathcal{T}(\mathcal{f}(n))$', 'tab:blue'),
                ]
            ),
            spec_axis(
                'Theoretical',
                [
                    spec_line(metro.theoretical, complexity.latex, 'tab:red')
                ]
            )
        ]
    )
