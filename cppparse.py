import typing
import re
import clang.cindex


index = clang.cindex.Index.create()
tu = index.parse('SDL2/include/SDL_keycode.h')

enums = []
new_enums = []
enums_count = 0#for anonimouse enums(like C 'typedef enum')

def print_enums():
	for i in enums:
		print(i)		

def print_new_enums():
	for i in new_enums:
		print(i)		

def compare_enums():
	for i in new_enums:
		print(i)		

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

def remove_underscore_capitalize_next(match):
	return match.group(1).upper()

def replace_prefix_impl(src: str, prefix: str)->str:
	prefix_length = len(prefix)
	# Remove prefix and capitalize begin of result string
	result =  src[prefix_length:].capitalize()
	# Remove all '_' sumbols and capitalize next symbol
	result = re.sub(r'_(.)', remove_underscore_capitalize_next, result)
	return result

def replace_prefix(enum, pattern: str, new_name: str):
	new_enums.append([new_name])
	for i in enum[1]:
		s = replace_prefix_impl(i, pattern)
		new_enums[-1].append(s)

replace_prefix(enums[2], 'SDL_SCANCODE_', 'ScanCode')
replace_prefix(enums[3], 'SDLK_', 'KeyCode')
replace_prefix(enums[4], 'KMOD_', 'KeyMode')

#print_enums()
print_new_enums()

# def generate_new_enums():
# 	for i in new_enums[1]:
# 		new_enums[-1].append(s)

print('End of script')


# C++ generators
class Generator:	
	tablevel: int = 0
	tabsize: int = 4
	
	def __init__(self, *generators):
		self.generators = generators				
	
	def format(self) -> str:
		pass


class TranslationUnit(Generator):		
	def __init__(self, *generators):
		Generator.__init__(self, generators)
		self.result: str = self.format()

	def format(self) -> str:
		s: str = ''
		for gs in self.generators:
			for g in gs:
				s = s + g.format()
		return s

	def save(self, file_name: str):
		file = open(file_name, 'w')
		file.write(self.result)
		file.close()


class Namespace(Generator):

	def __init__(self, name: str, *generators):
		Generator.__init__(self, generators)
		self.name = name

	def format(self) -> str:
		s: str = 'namespace ' + self.name +'\n{\n'
		for gs in self.generators:
			for g in gs:
				s += g.format()
		s += '\n}\\\\namespace ' + self.name
		return s

class Block(Generator):

	def __init__(self, *generators):
		Generator.__init__(self, generators)
		self.result: str

class Enum(Generator):

	def __init__(self, name: str, consts: [str]):
		Generator.__init__(self)
		self.name = name
		self.result: str
		self.consts = consts		

	def format(self) -> str:
		s: str = 'enum class ' + self.name +'\n{\n'
		for c in self.consts:
			s += c + ',' + '\n'
		s += '\n}\\\\enum class ' + self.name
		return s


tu = TranslationUnit(
	Namespace('vgui',
		Enum(new_enums[2][0], new_enums[2])))
print(tu.format())
tu.save('keys.hpp')


