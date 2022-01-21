# __PRINT__ #
import inspect

def aux(D, loop='|___', tab='   ', n=-1):
	types = [bool, int, float, complex, str, list, tuple, dict]
	n+=1
	if n <= 1:
		loop = loop * n 
		tab = tab * n + '|___'
	else:
		loop = (tab + '|') * (n - 1) + loop 
		tab = tab  + ('|' + tab) * (n - 1) + '|___'
	# print(n)
	for key in list(D.keys()):
		if n == 0:
			print(f'{loop}.{key}, {type(D[key])}')
		else:
			print(f'|{loop}.{key}, {type(D[key])}')
		if not type(D[key]) is dict:
			if not type(D[key]) is list:
				if n == 0:
					print(f'{tab}{D[key]}')
				else:
					print(f'|{tab}{D[key]}')
			else:
				for item in D[key]:
					if not type(item) is dict:
						if n == 0:
							print(f'{tab}{item}')
						else:
							print(f'|{tab}{item}')
					else:
						aux(item, loop='___', n=n)
		else:
			aux(D[key], loop='___',  n=n)
	return True
	
def dictPrint(D):
	aux(D)
	print('|___')
	
def listPrint(lst, n_splits=1):
	types = [bool, int, float, complex, str, list, tuple, dict]
	n = 0
	if len(lst)%n_splits == 0:
		loops = range(len(lst)//n_splits)
	else:
		loops = range(len(lst)//n_splits + 1 )
	for i in loops:
		try:
			if n_splits == 1:
				if type(lst[i]) is dict:
					dictPrint(lst[i])
				else:
					print(lst[n:n+n_splits])
			n += n_splits
		except IndexError:
			print(lst[n-1:])
	return True


if __name__ == '__main__':
	pass