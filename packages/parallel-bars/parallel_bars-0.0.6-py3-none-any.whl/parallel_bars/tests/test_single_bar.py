from unittest import TestCase

from parallel_bars.main import compute_with_single_bar
from parallel_bars.tests import fun, items, squared_items


class TestSingleBar(TestCase):
    def test_computes_with_default_params(self):
        results = compute_with_single_bar(
            fun=fun,
            items=items,
        )

        self.assertEqual(
            sorted(results),
            squared_items,
        )

    def test_computes_with_specified_num_processes(self):
        results = compute_with_single_bar(
            fun=fun,
            items=items,
            num_processes=20,
        )

        self.assertEqual(
            sorted(results),
            squared_items,
        )

    def test_throws_an_error_for_wrong_num_processes(self):
        self.assertRaises(
            ValueError,
            compute_with_single_bar,
            fun=fun,
            items=items,
            num_processes=-1,
        )

    def test_returns_results_in_order(self):
        self.assertEqual(
            squared_items,
            compute_with_single_bar(fun, items, in_order=True)
        )
