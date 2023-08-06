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
            table = core.add_table(table_name="table")
            print('table_id', table.id)
            view = table.add_view(view_name="viewname", view_type=ViewType.GRID)
            print(view.id)
            print('view_id', table.id)

            rows = table.add_rows(2)
            print('rows', rows)
            column_configs = [
                ColumnConfig(field_type=FieldType.TEXT, field_name='col_{0}'.format(i), order=i, foreign_table_id='')
                for i in range(2)]
            columns = table.add_columns(column_configs)
            print('columns', columns)

            cells_from_table = table.get_cells(rows, columns, mode='intersection')
            # cells_from_table.update([['1', '2'], ['3', '4']])
            # time.sleep(1)
            # print('cells from table', table.get_cells(rows, columns, mode='intersection'))

            # rows[0].update(['6', '6'])
            # time.sleep(1)
            # print('cells from row updated table', table.get_cells(rows, columns, mode='intersection'))
            #
            # table, cells = treelab.add_table_with_content(field_names=['A', 'B', 'C'], field_types=[FieldType.TEXT] * 3,
            #                                            view_type=ViewType.GRID, view_name='viewName',
            #                                            table_name="new table",
            #                                            data_matrix=[['caminer', 'inc', 'is'],
            #                                                         ['the', 'best', 'company'],
            #                                                         ['in', 'the', 'world']])
            #
            # time.sleep(2)

            listener1 = lambda e: print('FROM LISTENER 1: received cell id: \n', e)
            listener2 = lambda e: print('FROM LISTENER 2: received cell id: \n', e)
            cells_from_table[:2].listen_to(listener1, name='listener1', thread_num=1, user_only=False)
            cells_from_table[2:].listen_to(listener2, name='listener2', thread_num=0, user_only=False)

            # print('cells', cells_from_table)

            # cells.listen_to(lambda e: print('received cell id', e.rowId + ':' + e.columnId), 'cell listener')

            print('all listeners ...', workspace.event_handler.registered_listeners)
            print('all threads ...', threading.enumerate())
            print('updating cells in a different thread...')
            threading.Thread(target=update_cell, args=(cells_from_table, 30)).start()

            # print('get column, col_0', table.get_columns_by_name('col_0'))
            # print('get all cells', table.get_cells(mode='all').values_dict())
            # print('get all columns', table.get_columns(mode='all').objects)

    # def test(self):
    #     workspace_id = "wspb526e8d9bc861efd"
    #     core_id = "creb526e8d9fd0ab879"
    #     table_id = "tblb526e8da250b3b9c"
    #     view_id = "viwb526e8da9b852372"
    #
    #     table = Workspace(workspace_id=workspace_id)\
    #         .get_core(core_id=core_id)\
    #         .get_table(table_id=table_id)
    #     table.add_row()
    #     table.add_column(field_type=FieldType.TEXT, field_name="lolllllll", order=0)
    #     print(table.get_content()['viewDatas'][0]['columns'])


if __name__ == '__main__':
    unittest.main()
