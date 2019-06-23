import clang.cindex
import typing

index = clang.cindex.Index.create()
translation_unit = index.parse('SDL2/include/SDL_keycode.h', args=['-std=c++17'])

def filter_node_list_by_node_kind(
    nodes: typing.Iterable[clang.cindex.Cursor],
    kinds: list,
) -> typing.Iterable[clang.cindex.Cursor]: 
    result = []

    for i in nodes:
        if i.kind in kinds:
            result.append(i)

    return result

all_classes = filter_node_list_by_node_kind(translation_unit.cursor.get_children(), 
[clang.cindex.CursorKind.ENUM_DECL,clang.cindex.CursorKind.ENUM_CONSTANT_DECL])


def find_nodes(nodes: typing.Iterable[clang.cindex.Cursor]):
    for i in nodes:
    	if len(i.displayname) > 0:
    		print(i.displayname)
    	find_nodes(i.get_children())


print(len(all_classes))

for i in all_classes:
    print (i.displayname)

print("end of script")

find_nodes(translation_unit.cursor.get_children())