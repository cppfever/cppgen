import clang.cindex
import typing

index = clang.cindex.Index.create()
tu = index.parse('SDL2/include/SDL_keycode.h', args=['-std=c++17'])

enums = []
enums_count = 0#for anonimouse enums

def find_enums(nodes: typing.Iterable[clang.cindex.Cursor]):
    for i in nodes:
    	if i.kind == clang.cindex.CursorKind.ENUM_DECL :
    		global enums_count
    		enums.append(('SomeEnum' + str(enums_count), []))
    		enums_count = enums_count+1
    		find_enum_constants(i.get_children())

def find_enum_constants(nodes: typing.Iterable[clang.cindex.Cursor]):
    for i in nodes:
    	if i.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL :
    		enums[-1][1].append(i.displayname)

find_enums(tu.cursor.get_children())

for i in enums:
	print(i[1],'\n')		

print("End of script")
