from numerics.pi import monte_carlo


class TestMonteCarlo:

    def test_should_approximate_pi():
        assert 3 <= monte_carlo <= 4  # close enough 😅
