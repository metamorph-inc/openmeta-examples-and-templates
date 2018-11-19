PET Analysis Error Example
===============================

This example demonstrates the use of OpenMDAO's `AnalysisError` within a PET
Python Wrapper or Analysis Block.  If a PET block raises `AnalysisError` within
its `solve_nonlinear` function, execution of that iteration is immediately
stopped, and any PET blocks dependent on the results of the block will not
run; the PET then continues execution with the next iteration.  This is
particularly useful when a PET block can take a long time to run and should be
skipped under certain conditions (for example, if another upstream component has
failed and its outputs are invalid).

In this example, `Adder1`, `ExceptionAdder`, and `Adder2` execute in sequence,
logging to the PET's log file (in the `log` folder of the output directory).
When `ExceptionAdder` receives an input value between 2 and 4, it raises an
`AnalysisException`; in those cases, note that (in the log file) only `Adder1`
executes and `Adder2` is skipped for that iteration.
