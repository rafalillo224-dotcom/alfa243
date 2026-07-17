from alfa243.engines.poisson import PoissonEngine


def test_poisson_probability_zero_goals():
    probability = PoissonEngine.probability(1.5, 0)

    assert 0 < probability < 1


def test_poisson_probability_one_goal():
    probability = PoissonEngine.probability(1.5, 1)

    assert 0 < probability < 1

def test_distribution_sum_is_close_to_one():

    distribution = PoissonEngine.distribution(1.5)

    assert abs(sum(distribution) - 1.0) < 0.001    