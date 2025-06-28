import statistics
import unittest

def calculate_statistics(prices):
    """Calculate basic statistics for a list of prices."""
    if not prices:
        raise ValueError("The list of prices cannot be empty.")

    mean_price = statistics.mean(prices)
    median_price = statistics.median(prices)
    stdev_price = statistics.stdev(prices) if len(prices) > 1 else 0.0

    return {
        "mean": mean_price,
        "median": median_price,
        "stdev": stdev_price
    }


class TestPriceStatistics(unittest.TestCase):
    def test_calculate_statistics(self):
        # Test case with a list of prices
        prices = [100, 150, 200, 250, 300]
        stats = calculate_statistics(prices)

        # Expected values
        self.assertAlmostEqual(stats["mean"], 200.0)
        self.assertAlmostEqual(stats["median"], 200)
        self.assertAlmostEqual(stats["stdev"], 79.05694150420949, places=5)

    def test_calculate_statistics_empty_list(self):
        # Test case with an empty list of prices
        with self.assertRaises(ValueError):
            calculate_statistics([])

    def test_calculate_statistics_single_value(self):
        # Test case with a single price value
        prices = [100]
        stats = calculate_statistics(prices)

        # Expected values
        self.assertAlmostEqual(stats["mean"], 100.0)
        self.assertAlmostEqual(stats["median"], 100)
        self.assertAlmostEqual(stats["stdev"], 0.0)


if __name__ == "__main__":
    unittest.main()