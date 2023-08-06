from covgen.run.inputgenerator import InputGenerator
import logging

# logging.basicConfig(level=logging.DEBUG)
generator = InputGenerator(
    'target/orelse.py', function_name='func1')

generator.target_function.branch_tree.print()

result = generator.generate_input('2T')
print(result)
