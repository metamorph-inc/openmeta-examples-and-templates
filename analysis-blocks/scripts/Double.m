% variable: double_out double output
% variable: doublearray_out double[] output
% variable: string_out string output
% variable: stringarray_out string[] output
% variable: object_out object output
% variable: double_in double input
% variable: doublearray_in double[] input
% variable: string_in string input
% variable: stringarray_in string[] input
% variable: object_in object input


double_out = double_in * 2
doublearray_out = doublearray_in * 2
string_out = strcat(string_in, string_in)
stringarray_out = [stringarray_in, stringarray_in]
object_out = structfun(@(x) (x * 2), object_in, 'uni', 0)
