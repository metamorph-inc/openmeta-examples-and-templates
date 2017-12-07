% variable: bool_in bool input
% variable: dict_hetero_in object input
% variable: dict_str_int_in object input
% variable: float_in double input
% variable: npfloatarray_in double[] input
% variable: npintarray_in double[] input
% variable: stringarray_in string[] input
% variable: unicode_in string input
% variable: unicodearray_in string[] input
% variable: bool_out bool output
% variable: dict_hetero_out object output
% variable: dict_str_int_out object output
% variable: float_out double output
% variable: npfloatarray_out double[] output
% variable: npintarray_out double[] output
% variable: stringarray_out string[] output
% variable: unicode_out string output
% variable: unicodearray_out string[] output

bool_out = ~bool_in
dict_hetero_out = dict_hetero_in % too complext to 'double'
dict_str_int_out = structfun(@(x) (x * 2), dict_str_int_in, 'uni', 0)
float_out = float_in * 2
npfloatarray_out = npfloatarray_in * 2
npintarray_out = npintarray_in * 2
stringarray_out = [stringarray_in, stringarray_in]
unicode_out = strcat(unicode_in, unicode_in)
unicodearray_out = [unicodearray_in, unicodearray_in]

