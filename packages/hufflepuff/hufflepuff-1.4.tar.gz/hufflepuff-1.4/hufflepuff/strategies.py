"""
This file provides various "strategies" for searching.

Given a search.Searcher object, a strategy is responsible for running the
searcher (by repeatedly calling the step method).
"""

import itertools

def fixed_iterations(searcher, num_iterations):
    for _ in range(num_iterations):
        yield searcher.step()

def gradient_retry(searcher):
    max_none = lambda a, b: b if a is None else max(a, b)

    # TODO: make these configurable
    min_iterations = 10
    weight = .5
    reset_factor = .05
    max_rounds = 10

    scores = searcher.step()
    yield scores
    smoothed_score = scores[0][0]

    for i in range(max_rounds):
        best_gradient = None

        for j in itertools.count():
            scores = searcher.step()
            yield scores
            score = scores[0][0]

            new_smoothed_score = (
                smoothed_score * (1 - weight) +
                score * weight
            )
            gradient = smoothed_score - new_smoothed_score
            smoothed_score = new_smoothed_score

            best_gradient = max_none(best_gradient, gradient)
            if j >= min_iterations:
                if gradient <= best_gradient * reset_factor:
                    break

        if j == min_iterations and i != 0:
            break
        searcher.states = [
            state
            for _, state in searcher.best
        ]

STRATEGIES = {
    'fixed-iterations': lambda searcher, args: (
        fixed_iterations(searcher, args.num_iterations)),
    'gradient-retry': lambda searcher, args: gradient_retry(searcher),
}
