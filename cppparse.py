import typing
import re
import clang.cindex


index = clang.cindex.Index.create()
tu = index.parse('SDL2/include/SDL_keycode.h')

enums = []
new_enums = []
enums_count = 0#for anonimouse enums(like C 'typedef enum')

#Find clang.cindex.CursorKind.ENUM_DECL
def find_enums(nodes: typing.Iterable[clang.cindex.Cursor]):
    for i in nodes:
    	if i.kind == clang.cindex.CursorKind.ENUM_DECL :
    		if len(i.displayname) == 0:
	    		global enums_count
    			enums.append(('SomeEnum' + str(enums_count), []))
    			enums_count = enums_count+1
    		else:
    			enums.append((i.displayname, [])) 			
    		find_enum_constants(i.get_children())

#Find clang.cindex.CursorKind.ENUM_CONSTANT_DECL
def find_enum_constants(nodes: typing.Iterable[clang.cindex.Cursor]):
    for i in nodes:
    	if i.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL :
    		enums[-1][1].append(i.displayname)

#Find all anums
find_enums(tu.cursor.get_children())	

def upper_repl(match):
	return match.group(1).upper()

def replace_prefix(src: str, prefix: str)->str:
	prefix_length = len(prefix)
	result =  src[prefix_length:].capitalize()
	result = re.sub(r'_(.)', upper_repl, result)
	return result

def replace_pattern(enum, pattern: str):
	new_enums.append([])
	for i in enum[1]:
		s = replace_prefix(i, pattern)
		new_enums[-1].append(s)

replace_pattern(enums[2], 'SDL_SCANCODE_')
replace_pattern(enums[3], 'SDLK_')
replace_pattern(enums[4], 'KMOD_')

for i in new_enums:
	print(i)		


print("End of script")
