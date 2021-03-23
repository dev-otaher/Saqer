from typing import List

from modules.Student import Student


class Students(List[Student]):
    def __init__(self):
        super().__init__()

    def extend(self, std_list):
        if len(self) == 0:
            super().extend(std_list)
        else:
            for self_std in self:
                for std in std_list:
                    if self_std.uni_id == std.uni_id:
                        self_std.appear_counter += std.appear_counter
                        std_list.remove(std)
                    else:
                        self.append(std)
                        std_list.remove(std)
