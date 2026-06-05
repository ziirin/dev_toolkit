def require_args(args: dict[str, str],
				 requirements: list[str]) -> bool:
	result = set(requirements).issubset(args)
	return result


# def get_args_from_path(path: str) -> dict[str, str]:
# 	args = {}
# 	splitted_path = path.split('?', 1)
# 	if len(splitted_path) == 2:
# 		str_args = splitted_path[-1].split('&')
# 		for arg in str_args:
# 			arg_pair = arg.split('=', 1)
# 			if len(arg_pair) == 2:
# 				args[arg_pair[0]] = arg_pair[1]
	
# 	return args

# def get_args_from_path(path: str) -> dict[str, str]:
#     if '?' not in path:
#         return {}
    
#     params_str = path.split('?', 1)[1]
#     params = {}
#     buffer = ''
#     quoted = False
    
#     for char in params_str:
#         if char == '"':
#             quoted=True
#             continue
        
#         elif char == '&' and not quoted:
#             if '=' in buffer:
#                 key, value = buffer.split('=', 1)
#                 params[key] = value
#             buffer = ''
        
#         else:
#             buffer += char
    
#     if buffer and '=' in buffer:
#         key, value = buffer.split('=', 1)
#         params[key] = value
    
#     return params

import re
def get_args_from_path(path: str) -> dict[str, str]:
    if '?' not in path:
        return {}
    
    params_str = path.split('?', 1)[1]
    pattern = patron = r'([a-zA-Z0-9_]+)=(?:"([^"]*)"|([^&]*))'
    matches = re.findall(patron, params_str)
    
    result = {}
    for group in matches:
        key = group[0]
        value = group[1] if group[1] else group[2]
        result[key] = value
        
    return result