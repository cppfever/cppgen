import clang.cindex
import typing

index = clang.cindex.Index.create()
translation_unit = index.parse('main.cpp', args=['-std=c++17'])

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
[clang.cindex.CursorKind.CLASS_DECL, clang.cindex.CursorKind.STRUCT_DECL, clang.cindex.CursorKind.NAMESPACE,
clang.cindex.CursorKind.CLASS_TEMPLATE, clang.cindex.CursorKind.INCLUSION_DIRECTIVE
])

print(len(all_classes))

for i in all_classes:
    print (i.spelling)

print("end of script")