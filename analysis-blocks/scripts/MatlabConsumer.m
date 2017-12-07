% variable: bool_in bool input
% variable: dict_hetero_in object input
% variable: dict_str_int_in object input
% variable: float_in double input
% variable: npfloatarray_in double[] input
% variable: npintarray_in double[] input
% variable: stringarray_in string[] input
% variable: unicode_in string input
% variable: unicodearray_in string[] input

fileID = fopen('consumermatlab.txt','w');

if bool_in
    fprintf(fileID,'bool_in: True\r\n');
else
    fprintf(fileID,'bool_in: False\r\n');
end

fprintf(fileID,'dict_hetero_in: (%s)\r\n', class(dict_hetero_in));
cellfun(@(x) (fprintf(fileID,'%s,',x)), fieldnames(dict_hetero_in));
fprintf(fileID,'\r\n');
structfun(@(x) (fprintf(fileID,'%s,',ItemToString(x))), dict_hetero_in, 'uni', 0);
fprintf(fileID,'\r\n');
% You could also use the method below to output a struct to a txt file.
%writetable(struct2table(dict_hetero_in), 'dict_hetero_in.txt');

fprintf(fileID,'dict_str_int_in: (%s)\r\n', class(dict_str_int_in));
cellfun(@(x) (fprintf(fileID,'%s,',x)), fieldnames(dict_str_int_in));
fprintf(fileID,'\r\n');
structfun(@(x) (fprintf(fileID,'%d,',x)), dict_str_int_in, 'uni', 0);
fprintf(fileID,'\r\n');
% You could also use the method below to output a struct to a txt file.
%writetable(struct2table(dict_str_int_in), 'dict_str_int_in.txt');

fprintf(fileID,'float_in: %f (%s)\r\n', float_in, class(float_in));

fprintf(fileID,'npfloatarray_in: (%s)\r\n', class(npfloatarray_in));
arrayfun(@(x) (fprintf(fileID,'%d,',x)), npfloatarray_in);
fprintf(fileID,'\r\n');

fprintf(fileID,'npintarray_in: (%s)\r\n', class(npintarray_in));
arrayfun(@(x) (fprintf(fileID,'%d,',x)), npintarray_in);
fprintf(fileID,'\r\n');

fprintf(fileID,'stringarray_in: (%s)\r\n', class(stringarray_in));
cellfun(@(x) (fprintf(fileID,'"%s",',x)), stringarray_in);
fprintf(fileID,'\r\n');

fprintf(fileID, 'unicode_in: "%s"', unicode_in);
fprintf(fileID, ' (%s)\r\n', class(unicode_in));

fprintf(fileID,'unicodearray_in: (%s)\r\n', class(unicodearray_in));
cellfun(@(x) (fprintf(fileID,'"%s",',x)), unicodearray_in);
fprintf(fileID,'\r\n');

fclose(fileID);