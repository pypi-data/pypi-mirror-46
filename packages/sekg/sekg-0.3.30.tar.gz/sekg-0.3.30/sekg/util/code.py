import re


class CodeElementNameUtil:
    PATTERN = re.compile(r'((?<=[a-z])[A-Z]|(?<!\A)[A-Z](?=[a-z]))')

    PATTERN_2_4 = re.compile(r'(2|4)')
    PATTERN_split = re.compile(r'([A-Z]+)([A-Z][a-z0-9]+)')
    PATTERN_split_num = re.compile(r'([0-9]?[A-Z]+)')

    def get_simple_name_with_parent(self, name):
        if not name:
            return None
        team_name = name.split("(")[0]
        split_names = team_name.split(".")
        if len(split_names) <= 1:
            return split_names[-1]

        child = split_names[-1].strip()
        parent = split_names[-2].strip()

        return parent + "." + child

    def get_simple_name(self, name):
        """
        get the simple name for class, method, field
        :param name:
        :return:
        """
        if not name:
            return None
        team_name = name.split("(")[0]
        simple_name = team_name.split(".")[-1].strip()

        return simple_name

    def split_camel_name_and_underline(self, name):
        if not name:
            return None
        simple_name = self.get_simple_name(name)

        sub = re.sub(self.PATTERN_2_4, r' \1 ', simple_name).strip()
        sub = re.sub(r'_', " ", sub)
        sub = re.sub(self.PATTERN_split, r'\1 \2', sub)
        sub = re.sub(self.PATTERN_split_num, r' \1', sub)
        sub = re.sub(r'\s+', " ", sub).strip()

        # alias_name = re.sub(CodeElementNameUtil.PATTERN, r' \1', simple_name)
        # alias_name = alias_name.replace("_", " ")
        # return alias_name.strip()

        return sub

    def generate_aliases(self, qualified_name, include_simple_parent_name=False):
        if not qualified_name:
            return []

        simple_name = self.get_simple_name(qualified_name)
        separate_name = self.split_camel_name_and_underline(simple_name)

        name_list = [qualified_name, simple_name, separate_name, ]

        if include_simple_parent_name:
            name_list.append(self.get_simple_name_with_parent(qualified_name))

        name_list = [name for name in name_list if name]

        return list(set(name_list))
