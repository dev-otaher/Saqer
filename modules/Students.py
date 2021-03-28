from typing import List

from modules.Student import Student


class Students(List[Student]):
    def __init__(self):
        super().__init__()

    def extend(self, students: List[Student]):
        if len(self) == 0:
            super().extend(students)
        else:
            for self_std in self:
                for std in students:
                    if self_std.uni_id == std.uni_id:
                        self_std.appear_counter += std.appear_counter
                        students.remove(std)
                        break
