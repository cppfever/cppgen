import clang.cindex
import typing

index = clang.cindex.Index.create()
tu = index.parse('SDL2/include/SDL_keycode.h', args=['-std=c++17'])


def find_enums(nodes: typing.Iterable[clang.cindex.Cursor]):
    for i in nodes:
    	if i.kind == clang.cindex.CursorKind.ENUM_DECL :
    		find_enum_constants(i.get_children())

def find_enum_constants(nodes: typing.Iterable[clang.cindex.Cursor]):
    for i in nodes:
    	if i.kind == clang.cindex.CursorKind.ENUM_CONSTANT_DECL :
    		print(i.displayname)

find_enums(tu.cursor.get_children())
print("\nEnd of script")
