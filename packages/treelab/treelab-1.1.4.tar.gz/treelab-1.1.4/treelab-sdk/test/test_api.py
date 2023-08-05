import unittest

from treelab.api import *
import time


def update_cell(cells, wait_time):
    time.sleep(wait_time)
    cells.update_all(value="text")


class TestApi(unittest.TestCase):
    def test(self):
        workspace = Treelab.add_workspace(workspace_name="workspace")
        with subscribe_under(workspace):
            print(workspace.id)
            core = workspace.add_core(core_name="corename")
            print(core.id)

            table, cells = core.add_table_with_content(field_names=['A', 'B', 'C'], field_types=[FieldType.TEXT] * 3,
                                                       view_type=ViewType.GRID, view_name='viewName',
                                                       table_name="new table",
                                                       data_matrix=[['caminer', 'inc', 'is'],
                                                                    ['the', 'best', 'company'],
                                                                    ['in', 'the', 'world']])

            time.sleep(2)


if __name__ == '__main__':
    unittest.main()
