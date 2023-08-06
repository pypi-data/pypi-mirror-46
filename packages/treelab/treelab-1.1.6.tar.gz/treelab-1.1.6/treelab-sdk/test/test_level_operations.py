import unittest

from treelab.api import *


class TestGRPCBasicOperations(unittest.TestCase):
    def init_table(self):
        workspace = Treelab.add_workspace(workspace_name="workspace")
        with subscribe_under(workspace):
            self.workspace_id = workspace.id
            print(workspace.id)
            core = workspace.add_core("corename")
            self.core_id = core.id
            print(core.id)
            table = core.add_table("table")
            self.table_id = table.id
            print(table.id)
            view = table.add_view("viewname", ViewType.GRID)
            self.view_id = view.id
            print(view.id)

    def add_row_test(self):
        row = Workspace(workspace_id=self.workspace_id).get_core(core_id=self.core_id).get_table(
            table_id=self.table_id).add_row()
        self.row_id = row.id
        self.row = row
        print(row.id)

    def add_rows_test(self):
        rows = Workspace(workspace_id=self.workspace_id).get_core(core_id=self.core_id).get_table(
            table_id=self.table_id).add_rows(2)
        self.row_ids = [row.id for row in rows]
        self.rows = rows
        print(self.row_ids)

    def add_column_test(self):
        col = Workspace(workspace_id=self.workspace_id).get_core(core_id=self.core_id).get_table(
            table_id=self.table_id).add_column(field_type=FieldType.TEXT, field_name='col_name', order=1)
        self.col_id = col.id
        self.col = col
        print(self.col_id)

    def add_columns_test(self):
        column_configs = [
            ColumnConfig(field_type=FieldType.TEXT, field_name='col_{0}'.format(i), order=i, foreign_table_id='')
            for i in range(2)]
        cols = Workspace(workspace_id=self.workspace_id).get_core(core_id=self.core_id).get_table(
            table_id=self.table_id).add_columns(column_configs)
        self.col_ids = [col.id for col in cols]
        self.cols = cols
        print(self.col_ids)

    def update_cells_test(self):
        table = Workspace(workspace_id=self.workspace_id).get_core(core_id=self.core_id).get_table(
            table_id=self.table_id)
        data_matrix = [['1', '2'], ['4', '5']]

        cells = table.get_cells(rows=self.rows, columns=self.cols,
                                mode='intersection').reshape(np.array(data_matrix).shape)
        cells.update(data_matrix)

    def add_table_with_content_test(self):
        field_types = [FieldType.TEXT] * 2
        field_names = ['col_{0}'.format(i) for i in range(2)]
        data_matrix = [['Treelab', 'is'], ['sooo', 'awesome']]

        table = Workspace(workspace_id=self.workspace_id).get_core(core_id=self.core_id).add_table_with_content(
            table_name='table_2', view_name='v_2', view_type=ViewType.GRID, field_types=field_types,
            field_names=field_names, data_matrix=data_matrix)

    def snapshots_core(self):
        core = Workspace(workspace_id=self.workspace_id).get_core(core_id=self.core_id).snapshots()
        print(core.id)

    def get_table_test(self):
        self.table_data = Workspace(workspace_id=self.workspace_id).get_core(core_id=self.core_id).get_table(
            table_id=self.table_id).data.table_dict
        print(self.table_data)

    def test_all(self):
        self.init_table()
        # self.add_row_test()
        self.add_rows_test()
        # self.add_column_test()
        self.add_columns_test()
        self.update_cells_test()

        self.add_table_with_content_test()

        self.snapshots_core()

        self.get_table_test()

    @staticmethod
    def update_cell(cell):
        print(cell)

    def ttest_for_me(self):
        workspace_id = 'wspb529eb565a07f2c3'
        core_id = 'creb529eb569e89af03'
        view_id = 'viwb529eb577a09f24f'
        table_id = 'tblb529eb56d68aa08a'
        row_id = 'rowb529eb57f8862842'
        col_id = 'colb529eb5b6b0e5c63'
        workspace = Workspace(workspace_id=workspace_id)
        with subscribe_under(workspace):
            print(workspace.id)
            core = workspace.get_core(core_id=core_id)
            print(core.id)
            table = core.get_table(table_id=table_id)
            print('table_id', table.id)
            row = table.get_row(row_id=row_id)
            col = table.get_column(col_id=col_id, field_type=FieldType.TEXT, field_name='', order=1)
            cell = table.get_cell(row, col)
            cell.listen_to(self.update_cell, 'cell listener')

    def ttest_listen(self):
        workspace = Workspace(name="workspace")
        with subscribe_under(workspace):
            print(workspace.id)
            core = workspace.add_core("corename")
            print(core.id)
            table = core.add_table("table")
            print('table_id', table.id)
            view = table.add_view("viewname", ViewType.GRID)
            print(view.id)
            print('view_id', table.id)

            rows = table.add_rows(3)
            column_configs = [
                ColumnConfig(field_type=FieldType.TEXT, field_name='col_{0}'.format(i), order=i, foreign_table_id='')
                for i in range(5)]
            columns = table.add_columns(column_configs)
            cells = table.get_cells(rows, columns)
            cells.listen_to(self.update_cell, 'listen')


if __name__ == '__main__':
    unittest.main()
