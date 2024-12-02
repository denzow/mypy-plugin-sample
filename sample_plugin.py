# plugin.py
from mypy.plugin import Plugin, ClassDefContext
from mypy.nodes import ClassDef, NameExpr, Var
from typing import List, Tuple


class UserCodeMustBeStrPlugin(Plugin):
    def get_class_decorator_hook(self, fullname: str):
        # 全クラスのデコレータを調べるフックを設定
        def decorator_hook(ctx: ClassDefContext):
            class_def = ctx.cls
            if self.is_dataclass(class_def):
                attributes = self.get_dataclass_attributes(class_def)
                for attr_name, typer_str in attributes:
                    if attr_name.endswith('user_code') and typer_str != 'builtins.str':
                        ctx.api.fail(
                            f"Attribute '{attr_name}' should be of type 'builtins.str'",
                            ctx.cls
                        )
            return None
        return decorator_hook

    def is_dataclass(self, class_def: ClassDef) -> bool:
        # クラスのデコレータに@dataclassがあるかチェック
        for decorator in class_def.decorators:
            if isinstance(decorator, NameExpr) and decorator.fullname == 'dataclasses.dataclass':
                return True
        return False

    def get_dataclass_attributes(self, class_def: ClassDef) -> List[Tuple[str, str]]:
        # dataclassの属性を取得する
        attributes = []
        for name, symbol in class_def.info.names.items():
            # symbol.nodeがVarであれば、それは属性を示す
            if isinstance(symbol.node, Var):
                var_node = symbol.node
                attr_type = var_node.type
                type_str = str(attr_type) if attr_type else "Unknown"
                attributes.append((name, type_str))
        return attributes


def plugin(version: str):
    return UserCodeMustBeStrPlugin
