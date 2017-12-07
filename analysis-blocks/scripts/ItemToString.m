function string = ItemToString(input)
if ischar(input)
    string = input
elseif isnumeric(input)
    string = num2str(input)
elseif iscell(input)
    string = '<Cell>'
elseif isstruct(input)
    string = '<Struct>'
else
    string = '<Unknown>'
end