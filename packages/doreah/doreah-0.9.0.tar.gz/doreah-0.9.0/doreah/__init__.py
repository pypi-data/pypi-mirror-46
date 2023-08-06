name = "doreah"
version = 0,9,0


__all__ = [
	"caching",
	"logging",
	"persistence",
	"pyhp",
	"regular",
	"settings",
	"timing",
	"tsv"

]




# useful things for everyone


def deprecated(func):
	"""Function decorator to deprecate a function"""

	def newfunc(*args,**kwargs):
		print("\033[93m" + "Function " + func.__name__ + " is deprecated!" + "\033[0m")
		return func(*args,**kwargs)

	return newfunc
