def foo(kwargs):
	print kwargs
	kwargs["b"] = 3
	print kwargs


kwargs = {"a":"a"}

foo(kwargs)
print kwargs
