from covgen.run.inputgenerator import InputGenerator
from covgen.localsearch.fitnesscalc import FitnessCalculator

import unittest


class TestInputGenerator(unittest.TestCase):
    def test_input_generator(self):
        generator = InputGenerator(
            'target/orelse.py')
        result = generator.generate_all_inputs()['func1']

        branch_tree = generator.target_function.branch_tree

        for branch_id, args in result.items():
            if args is not None:
                calculator = FitnessCalculator(
                    generator.target_function, branch_id, generator.AST)

                self.assertEqual(0, calculator.calculate(args))
