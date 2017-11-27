function [y] = MultipleFunctions(x)
y = g(f(x))
end

function [y] = g(x)
y = x * x
end

function [y] = f(x)
y = x + x
end