def require_args(args: dict[str, str],
				 requirements: list[str]) -> bool:
	result = set(requirements).issubset(args)
	return result


def get_args_from_path(path: str) -> dict[str, str]:
	args = {}
	splitted_path = path.split('?', 1)
	if len(splitted_path) == 2:
		str_args = splitted_path[-1].split('&')
		for arg in str_args:
			arg_pair = arg.split('=', 1)
			if len(arg_pair) == 2:
				args[arg_pair[0]] = arg_pair[1]
	
	return args