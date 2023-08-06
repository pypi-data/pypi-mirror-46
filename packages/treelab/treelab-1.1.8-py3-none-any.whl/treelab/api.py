import json
import threading
from contextlib import contextmanager
from typing import Iterator, Tuple

import numpy as np
import pandas as pd
from google.protobuf.json_format import MessageToJson

from treelab.event_handling.event_handler import *
from treelab.event_handling.listenable import *

from treelab.wrapper_classes import ColumnConfig
import time
from treelab.consts import UpdateAction
from treelab.helper import generate_id
from treelab.grpc.messages import service_pb2


class Treelab:
    @staticmethod
    def add_workspace(workspace_name: str):
        return Workspace(name=workspace_name)

    @staticmethod
    def workspace(workspace_id: str):
        return Workspace(workspace_id=workspace_id)

    @staticmethod
    def get_workspace(workspace_id: str):
        return Workspace(workspace_id=workspace_id)


class _TreelabObject(BasicListenable):
    def __init__(self):
        super().__init__(None)
        self._id = "default_id"
        self._name = "default_name"

    @property
    def id(self):
        return self._id

    @property
    def workspace(self):
        return self._workspace

    @property
    def name(self):
        return self._name

    @property
    @abstractmethod
    def data(self):
        raise NotImplementedError('Data not implemented in '.format(self.__class__))

    @property
    def __repr_fields__(self):
        raise NotImplementedError

    @abstractmethod
    def _get_event_id(self, event: EventPayload):
        return event.workspaceId

    def should_be_listened(self, event: EventPayload, listener: Listener):
        if self.id == self._get_event_id(event):
            return True
        return False

    def __repr__(self):
        items = {k: self.__dict__[k] for k in self.__repr_fields__}
        items = dict([('object_type', self.__class__.__name__)] + list(items.items()))
        return str(items)


class Workspace(_TreelabObject):
    __repr_fields__ = {'_id', '_name', 'topic'}

    def __init__(self, workspace_id=None, name="", topic="#"):
        super().__init__()
        self.topic = topic
        self._name = name
        self._id = self._create_workspace(workspace_id=workspace_id)
        self._setup_init_subscription()
        self._workspace = self

    def _create_workspace(self, workspace_id: str) -> str:
        if not workspace_id:
            workspace_id = TreeLabClient.create_workspace(CreateWorkspaceInput(name=self.name)).id
        else:
            workspace_projection = TreeLabClient.get_workspace(GetWorkspaceInput(id=workspace_id))
            self._name = workspace_projection.name
        return workspace_id

    def _setup_init_subscription(self):
        subscription_input = WorkspaceSubscriptionInput(workspaceId=self.id, topic=self.topic)
        self._event_handler = EventHandler(subscription_input)

    @property
    def event_handler(self) -> EventHandler:
        return self._event_handler

    def register(self, listener: Union[Listener, Callable[[EventPayload], Any]], thread_num: int = 0):
        """
        Register a listener to event handler, the listener are in type of either function that takes an EventPayload
        as parameter, or a Listener, you can specify whether to run this task on a new thread by the parameter
        on_new_thread
        :param listener:
        :param thread_num:
        :return:
        """
        listener = self._get_real_listener(listener)
        listener._thread_num = thread_num
        self.event_handler.register(listener=listener)

    def register_list(self, listeners: List[Union[Listener, Callable[[EventPayload], Any]]]):
        """
        Register a list of listeners to event handler
        :param listeners:
        :return:
        """
        for listener in listeners:
            self.register(listener)

    def _get_real_listener(self, listener: Union[Listener, Callable[[EventPayload], Any]]) -> Listener:
        if isinstance(listener, Callable):
            listener = FunctionListener(listener, self.event_handler.get_new_listener_name())

        return listener

    def get_core(self, core_id: str):
        """
        Get a treelab based on core_id
        :param core_id:
        :return:
        """
        return Core(workspace=self, core_id=core_id, name='')

    def get_all_cores(self):

        cores = TreeLabClient.get_all_cores(GetCoresInput(workspaceId=self.id))
        return [self.get_core(core.id) for core in cores.result]

    def core(self, core_id: str):
        """
        Get a treelab based on core_id, equivalent to get_core
        :param core_id:
        :return:
        """
        return self.get_core(core_id)

    def add_core(self, core_name: str, color: CoreColor = CoreColor.lightRed, icon: Icon = Icon.briefcase):
        """
        Add a treelab with core_name, and color and icon as option
        :param core_name:
        :param color:
        :param icon:
        :return:
        """
        return Core(workspace=self, name=core_name, color=color, icon=icon)

    def dispose(self):
        """
        Closing the subscription streams created by grpc
        :return:
        """
        self.event_handler.dispose()

    @property
    def data(self):
        return super().data

    def _get_event_id(self, event: EventPayload):
        return event.workspaceId


class Core(_TreelabObject):
    __repr_fields__ = {'_id', '_name', 'icon', 'color'}

    def __init__(self, name: str, core_id: str = None, workspace: Workspace = None,
                 color: CoreColor = CoreColor.lightBlack, icon: Icon = Icon.book):
        super().__init__()
        self._name = name
        self.color = color
        self.icon = icon
        self.tables = {}
        self._id = self._add_core(core_id, workspace)

    def _add_core(self, core_id: str, workspace: Workspace):
        if workspace:
            self._workspace = workspace
            if core_id:
                core_projection = TreeLabClient.get_core(GetCoreInput(workspaceId=self.workspace.id, coreId=core_id))
                self._name = core_projection.name
                self.color = CoreColor(core_projection.color)
                self.icon = Icon(core_projection.icon)
                return core_id
            else:
                add_core_input = AddCoreInput(workspaceId=self.workspace.id, coreName=self.name,
                                              color=self.color.value, icon=self.icon.value)
                core_id = TreeLabClient.add_core(add_core_input, workspace_id=self.workspace.id,
                                                 wait_till_complete=True).id

                return core_id
        else:
            raise ValueError("You need to get/create the treelab from the workspace!")

    def remove_core(self):
        remove_core_input = RemoveCoreInput(workspaceId=self.workspace.id, coreId=self.id)
        core_id = TreeLabClient.remove_core(remove_core_input)
        return core_id

    def update_core(self, core_name: str, color: CoreColor = CoreColor.lightBlack, icon: Icon = Icon.book):
        update_core_input = UpdateCoreInput(workspaceId=self.workspace.id, coreName=core_name, color=color, icon=icon)
        core_id = TreeLabClient.update_core(update_core_input)
        return core_id

    def add_table_with_content(self, table_name: str, view_name: str, view_type: ViewType,
                               column_config_inputs: List[ColumnConfigInput],
                               data_matrix: Union[List[List], np.array, pd.DataFrame]):

        """
        Add a table with content in type of TableContent
        :param table_name:
        :param view_name:
        :param view_type:
        :param column_config_inputs:
        :param data_matrix:
        :return:
        """
        table = self.add_table(table_name=table_name)
        view_id = table.add_view(view_name=view_name, view_type=view_type).id

        if isinstance(data_matrix, List):
            if len(data_matrix) == 0:
                raise ValueError('The size of the data matrix must not be zero')
            data_matrix = np.array(data_matrix)

        n_rows, n_cols = data_matrix.shape
        rows = table.add_rows(n_rows=n_rows, view_id=view_id)

        columns = table.add_columns(view_id=view_id, column_configs=column_config_inputs)
        cells = table.get_cells(rows, columns, mode='intersection') \
            .reshape(data_matrix.shape)
        cells.update(data_matrix)

        return table, view_id

    def get_table(self, table_id: str):
        """
        Get table from table_id
        :param table_id:
        :return:
        """
        table = Table(table_id=table_id, core=self)

        return table

    def table(self, table_id: str):
        """
        Get table from table_id, equivalent to get_table
        :param table_id:
        :return:
        """
        return self.get_table(table_id)

    def get_all_tables(self):
        get_tables_input = GetTablesInput(workspaceId=self.workspace.id, coreId=self.id)
        tables = TreeLabClient.get_all_tables(get_tables_input)
        all_tables = [self.get_table(table.id) for table in tables.result]
        return all_tables

    def add_table(self, table_name: str):
        """
        Create a table based on table_name
        not specified
        :param table_name:
        :return:
        """
        return Table(name=table_name, core=self)

    @property
    def data(self):
        return super().data

    def _get_event_id(self, event: EventPayload):
        return event.workspaceId

    def snapshots(self):
        """
        add core snapshots method
        :return:
        """

        tables = self.get_all_tables()
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        core = self.workspace.add_core(core_name='-'.join([self.name, local_time]), color=self.color,
                                       icon=self.icon)
        for table in tables:
            if not table.data.cells:
                continue
            table_name = table.name
            table_snapshots = core.add_table(table_name)
            view_ids = [table_snapshots.add_view(view_name=view.name, view_type=ViewType(view.view_type)).id for view in
                        list(table.data.views.values())]
            columns = table_snapshots.add_columns(view_id=view_ids[0], column_configs=list(table.data.columns.values()))
            rows = table_snapshots.add_rows(n_rows=len(table.data.rows.values()), view_id=view_ids[0])
            df = table.data_frame
            cells = table_snapshots.get_cells(rows, columns, mode='intersection') \
                .reshape(df.shape)
            cells.update(df.values)
        return core


class Table(_TreelabObject):
    __repr_fields__ = {'_id'}

    def __init__(self, name: str = None, table_id: str = None, core: Core = None):
        super().__init__()
        self._name = name
        self._id = self._add_table(table_id, core)

    def _add_table(self, table_id: str, core: Core):
        if core:
            self.core = core
            self._workspace = self.core.workspace
            if table_id:
                try:
                    table_projection = TreeLabClient.get_table(
                        GetTableInput(workspaceId=self.workspace.id, coreId=self.core.id, tableId=table_id))
                    self._name = table_projection.name
                except:
                    print('The table is empty')
                return table_id
            else:
                add_table_input = AddTableInput(workspaceId=self.workspace.id, coreId=self.core.id, tableName=self.name)
                table_id = TreeLabClient.add_table(add_table_input, workspace_id=self.workspace.id,
                                                   wait_till_complete=True, name_spaces=[self.core.id]).id
                return table_id
        else:
            raise ValueError("You need to get/create the table from the treelab!")

    def get_row(self, row_id: str):
        """
        Get row by row_id
        :param row_id:
        :return:
        """
        row = self.data.rows[row_id]

        try:
            row.value = self.data_frame.loc[row_id]
        except:
            row.value = None

        return row

    def row(self, row_id: str):
        """
        Get row by row_id, equivalent to get_row
        :param row_id:
        :return:
        """
        return self.get_row(row_id=row_id)

    def add_row(self, view_id: str):
        """
        Add a single row to the table
        :return:
        """
        row = Row(table=self, view_id=view_id)
        return row

    def add_rows(self, n_rows: int, view_id: str):
        """
        Add rows with number
        :param n_rows:
        :param view_id:
        :return:
        """
        if n_rows <= 0:
            raise ValueError('n_rows has to be a number larger than 0')
        rows = RowArray(parent_object=self, objects=[self.add_row(view_id=view_id) for _ in range(n_rows)],
                        workspace=self.workspace)

        return rows

    def get_rows(self, row_ids: List[str] = None):
        """
        Get rows by row_ids, if row_ids are not specified, get all rows from the table,
        :param row_ids:
        :return:
        """
        if row_ids:
            rows = [self.get_row(row_id=row_id) for row_id in row_ids]
        else:
            rows = self.data.rows

        row_array = RowArray(parent_object=self, objects=rows, workspace=self.workspace)
        try:
            row_array.value = self.data_frame.loc[row_ids]
        except:
            row_array.value = None

        return row_array

    def get_cell(self, row, column):
        """
        Get a single cell from known row and column
        :param row:
        :param column:
        :return:
        """
        return Cell(self, row, column)

    def get_cells(self, rows: List = None, columns: List = None, mode: str = 'all'):
        """
        Get cells from rows and columns
        :param rows:
        :param columns:
        :param mode:
            if mode == intersection:
                returns the cells on the intersection of all rows and columns
            if mode == pair:
                returns the cells based on row/column pairs, in this case, the size
                of rows has to be equal to the size of column
            if mode == all:
                return all cells under this table, rows and columns will be ignored in this case
        :return: cells: CellCollection
        """
        if (rows is None or columns is None) and mode != 'all':
            raise ValueError('rows and columns cannot be None for mode != all')

        if mode == 'intersection':
            cells = [Cell(self, row, column) for row in rows for column in columns]
        elif mode == 'pair':
            if len(rows) != len(columns):
                raise ValueError("The size of rows has to equal to the size of columns when all_cells are set as False")
            cells = [Cell(self, row, column) for row, column in zip(rows, columns)]
        elif mode == 'all':
            cells = list(self.data.cells.values())
        else:
            raise ValueError('{} mode is not supported, please select mode between intersection, pair and all'
                             .format(mode))

        return CellArray(self, cells, self.workspace)

    def add_column(self, view_id: str, field_type: FieldType = None, field_name: str = None, order: int = None,
                   foreign_table_id: str = None,
                   column_config_input: ColumnConfigInput = None, default_number: float = 0.0,
                   precision: int = 1, choices: List[List] = [], date_format: DateFormat = None,
                   include_time: bool = True,
                   time_format: TimeFormat = None, use_gmt: bool = True):
        """
        Add a single column with either (field_type, field_name, order, foreign_table_id),
        or column_config as as parameter which includes the four mentioned above
        :param view_id:
        :param field_type:
        :param field_name:
        :param order:
        :param foreign_table_id:
        :param column_config_input:
        :param default_number:
                    FieldType is NUMBER
        :param precision:
                    FieldType is NUMBER
        :param choices:
                    List contains two parameters, name and color. Name is of type STR and color is of type color
                    FieldType is MULTI_SELECT or SELECT
                    example:
                        [['a',Color.lightRed],
                        ['b',Color.pink]]
        :param date_format:
                    FieldType is DATETIME
        :param include_time:
                    FieldType is DATETIME
        :param time_format:
                    FieldType is DATETIME
        :param use_gmt:
                    FieldType is DATETIME
        :return:
        """
        if column_config_input:
            return Column(table=self, view_id=view_id, field_type=FieldType(column_config_input.type),
                          field_name=column_config_input.name,
                          order=column_config_input.order,
                          foreign_table_id=column_config_input.foreignTableId,
                          default_number=column_config_input.defaultNumber,
                          precision=column_config_input.precision, choices=column_config_input.choices,
                          date_format=DateFormat(
                              column_config_input.dateFormat) if column_config_input.dateFormat else '',
                          include_time=column_config_input.includeTime,
                          time_format=TimeFormat(
                              column_config_input.timeFormat) if column_config_input.timeFormat else '',
                          use_gmt=column_config_input.useGMT)
        else:
            if field_type is None or field_name is None or order is None:
                raise ValueError('Field type, field name and order cannot be None')
            column = Column(table=self, view_id=view_id, field_type=field_type, field_name=field_name, order=order,
                            foreign_table_id=foreign_table_id, default_number=default_number,
                            precision=precision, choices=choices, date_format=date_format,
                            include_time=include_time,
                            time_format=time_format, use_gmt=use_gmt)
            return column

    @staticmethod
    def add_column_record_reference(column_name: str, foreign_table_id: str, order: int = 1):
        return ColumnConfigInput(type=FieldType.RECORD_REFERENCE.value, name=column_name, order=order,
                                 foreignTableId=foreign_table_id)

    @staticmethod
    def add_column_text(column_name: str, order: int = 1):
        return ColumnConfigInput(type=FieldType.TEXT.value, name=column_name, order=order)

    @staticmethod
    def add_column_datetime(column_name: str, order: int = 1, date_format: DateFormat = DateFormat.Friendly,
                            include_time: bool = True, time_format: TimeFormat = TimeFormat.twelve,
                            use_gmt: bool = True):
        return ColumnConfigInput(type=FieldType.DATETIME.value, name=column_name, order=order,
                                 dateFormat=date_format.value,
                                 includeTime=include_time, timeFormat=time_format.value,
                                 useGMT=use_gmt)

    @staticmethod
    def add_column_number(column_name: str, order: int = 1, default_number: int = 12, precision: int = 1):
        return ColumnConfigInput(type=FieldType.NUMBER.value, name=column_name, order=order,
                                 defaultNumber=default_number, precision=precision)

    @staticmethod
    def add_column_multi_select(column_name: str, choices: List[List[Choice]], order: int = 1):
        return ColumnConfigInput(type=FieldType.MULTI_SELECT.value, name=column_name, order=order,
                                 choices=choices)

    @staticmethod
    def add_column_select(column_name: str, choices: List[List[Choice]], order: int = 1):
        return ColumnConfigInput(type=FieldType.SELECT.value, name=column_name, order=order,
                                 choices=choices)

    def add_columns(self, view_id: str, column_configs: List[Union[ColumnConfigInput, Any]]):
        """
        Add columns with List of column configs
        :param view_id:
        :param column_configs:
        :return:
        """
        if isinstance(column_configs[0], Column):
            columns = ColumnArray(self,
                                  [self.add_column(view_id=view_id,
                                                   field_type=column_config.field_type,
                                                   field_name=column_config.name, order=column_config.order,
                                                   foreign_table_id=column_config.foreign_table_id,
                                                   default_number=column_config.default_number,
                                                   precision=column_config.precision,
                                                   choices=column_config.choices,
                                                   date_format=DateFormat(
                                                       column_config.date_format) if column_config.date_format else '',
                                                   include_time=column_config.include_time,
                                                   time_format=TimeFormat(
                                                       column_config.time_format) if column_config.time_format else '',
                                                   use_gmt=column_config.use_gmt)
                                   for column_config in
                                   column_configs], self.workspace)
        elif isinstance(column_configs[0], ColumnConfigInput):
            columns = ColumnArray(self,
                                  [self.add_column(view_id=view_id, column_config_input=column_config) for column_config
                                   in
                                   column_configs],
                                  self.workspace)
        else:
            columns = None
        return columns

    def get_column_by_id(self, col_id: str):
        """
        Get a single column by column id from the table

        :param col_id:
        :return:
        """
        column = self.data.columns[col_id]
        return column

    def get_columns_by_name(self, field_name: str):
        """
        Get a single column by field name from the table

        :param field_name:
        :return:
        """

        if self.data.columns:
            return [v for k, v in self.data.columns.items() if v._name == field_name]
        else:
            return None

    def column(self, col_id: str):
        """
        Get a single column by column id from the table, equivalent to get_column_by_id
        :param col_id:
        :return:
        """
        return self.get_column_by_id(col_id=col_id)

    def get_columns(self, col_ids: List[str] = None, mode: str = 'all'):
        """
        Get either columns by either column ids or all columns under the table
        :param col_ids:
        :param mode:
            if mode == 'id':
                return columns by col_ids
            if mode == 'all':
                return all columns under this table, col_ids, if passed, will be ignored in this case
        :return:
        """
        if mode == 'all':
            columns = self.data.columns.values()
        elif mode == 'id':
            if col_ids is None:
                raise ValueError('col_ids should not be None when mode equals id')
            columns = [self.column(col_id=col_id) for col_id in col_ids]
        else:
            raise ValueError('{} mode is not supported, please select mode between id and all'.format(mode))

        col_array = ColumnArray(self, columns, self.workspace)
        try:
            col_array.value = self.data_frame[col_ids]
        except:
            col_array.value = None

        return col_array

    def get_view(self, view_id: str):
        """
        Get a view from view_id
        :param view_id:
        :return:
        """
        view = self.data.views[view_id]
        return view

    def get_views(self, view_ids: List[str], mode: str = 'id'):
        """
        Get views by a list of view_ids
        :param view_ids:
        :param mode:
        :return:
        """
        if mode == 'all':
            views = self.data.views.values()
        elif mode == 'id':
            if view_ids is None:
                raise ValueError('view_ids should not be None when mode equals id')
            views = [self.get_view(view_id=view_id) for view_id in view_ids]
        else:
            raise ValueError('{} mode is not supported, please select mode between id and all'.format(mode))

        return ViewArray(parent_object=self, objects=views, workspace=self.workspace)

    def add_view(self, view_name, view_type: ViewType = ViewType.GRID):
        """
        Add a view to the table
        :param view_name:
        :param view_type:
        :return:
        """
        view = View(table=self, name=view_name, view_type=view_type)

        return view

    def update(self, data_matrix: Union[List[List], np.array, pd.DataFrame],
               cell_type_matrix: Union[List[List], np.array]):
        """
        Update table content with data_matrix
        The shape of cell_type_matrix and data_matrix must be consistent and used to verify the cell field type
        :param data_matrix:
        :param cell_type_matrix:
        :return:
        """
        self.get_cells().update(data_matrix, cell_type_matrix)

    @property
    def data(self):
        """
        Get table content in dictionary format

        :return:
        """
        get_table_input = GetTableInput(workspaceId=self.workspace.id, coreId=self.core.id, tableId=self.id)
        table_projection = TreeLabClient.get_table(get_table_input)
        table_data = _TableData(table=self, table_dict=json.loads(MessageToJson(table_projection)))
        return table_data

    @property
    def data_frame(self):
        """
        Initialize table data to form a DataFrame format and column name mapping

        :return:
        """
        try:
            data = self.data
            row_ids = list(data.rows.keys())
            column_ids = list(data.columns.keys())
            content = []
            for row_id in row_ids:
                row_data = [
                    data.cells.get((row_id, column_id)).value if data.cells.get((row_id, column_id)) is not None else ''
                    for column_id in column_ids]
                content.append(row_data)
            df_data = pd.DataFrame(data=content, index=row_ids, columns=column_ids)
            return df_data
        except:
            return None

    def _get_event_id(self, event: EventPayload):
        return event.tableId


class View(_TreelabObject):
    __repr_fields__ = {'_id', '_name', 'view_type'}

    def __init__(self, name: str, view_type: ViewType = ViewType.GRID, view_id: str = None,
                 table: Table = None):
        super().__init__()
        self._name = name
        self.view_type = view_type
        self._id = self._add_view(view_id=view_id, table=table)

    def _add_view(self, view_id: str, table: Table):
        if table:
            self.table = table
            self.core = self.table.core
            self._workspace = self.core.workspace
            if view_id:
                return view_id
            else:
                add_view_input = AddViewInput(workspaceId=self.workspace.id, coreId=self.core.id, tableId=self.table.id,
                                              view=ViewDefinitionInput(name=self.name, type=self.view_type.value))
                view_id = TreeLabClient.add_view(add_view_input, workspace_id=self.workspace.id,
                                                 wait_till_complete=True,
                                                 name_spaces=[self.core.id, self.table.id]).id

                return view_id
        else:
            raise ValueError("You need to get/create the view from the table!")

    @property
    def data(self):
        matched_views = list(filter(lambda view: self.id == view.id, self.table.data.views))
        if len(matched_views) != 1:
            raise ValueError('Parent table does not have the current view!')
        return matched_views[0]

    def _get_event_id(self, event: EventPayload):
        return event.viewId


class Row(_TreelabObject):
    __repr_fields__ = {'_id'}

    def __init__(self, view_id: str, row_id: str = None, table: Table = None, order: int = 1):
        super().__init__()
        self.view_id = view_id
        self.order = order
        self._id = self._add_row(row_id, table)

    def _add_row(self, row_id: str, table: Table):
        if table:
            self.table = table
            self.core = self.table.core
            self._workspace = self.core.workspace
            if row_id:
                return row_id
            else:
                add_row_input = AddRowInput(workspaceId=self.workspace.id, coreId=self.core.id, tableId=self.table.id)
                row_id = TreeLabClient.add_row(add_row_input, workspace_id=self.workspace.id, wait_till_complete=True,
                                               name_spaces=[self.core.id, self.table.id, self.view_id]).id

                return row_id
        else:
            raise ValueError("You need to get/create the row from the table!")

    def update(self, vector: Union[List, pd.Series], columns: List = None):
        if not columns:
            columns = self.table.data.columns.values()

        if len(columns) != len(vector):
            raise ValueError("The size of column_ids must equals to the size of row!")

        self.table.get_cells([self], columns, mode='intersection').update([vector])

    @property
    def data(self):
        return super().data

    def _get_event_id(self, event: EventPayload):
        return event.rowId


class Column(_TreelabObject):
    __repr_fields__ = {'_id', '_name', 'order', 'foreign_table_id', 'field_type'}

    def __init__(self, view_id: str, col_id: str = None, field_name: str = '', order: int = 0,
                 foreign_table_id: str = '',
                 table: Table = None, field_type: FieldType = FieldType.TEXT, default_number: float = 0.0,
                 precision: int = 1, choices: List[Choice] = [], date_format: DateFormat = None,
                 include_time: bool = True,
                 time_format: TimeFormat = None, use_gmt: bool = True):
        """
        :param view_id:
        :param col_id:
        :param field_name:
        :param order:
        :param foreign_table_id:
        :param table:
        :param field_type:
        :param default_number:
                    FieldType is NUMBER
        :param precision:
                    FieldType is NUMBER
        :param choices:
                    List contains two parameters, name and color. Name is of type STR and color is of type color
                    FieldType is MULTI_SELECT or SELECT
                    example:
                        [['a',Color.lightRed],
                        ['b',Color.pink]]
        :param date_format:
                    FieldType is DATETIME
        :param include_time:
                    FieldType is DATETIME
        :param time_format:
                    FieldType is DATETIME
        :param use_gmt:
        :param visibility:
        """
        super().__init__()
        self.view_id = view_id
        self.field_type = field_type
        self.order = order
        self.foreign_table_id = foreign_table_id
        self.default_number = default_number
        self.precision = precision
        self.choices = self._get_choices(choices)
        self.date_format = date_format
        self.include_time = include_time
        self.time_format = time_format
        self.use_gmt = use_gmt
        self._name = field_name
        self._id = self._add_column(col_id, table)

    @staticmethod
    def _get_choices(choices):
        if choices and isinstance(choices[0], Choice):
            return choices
        elif choices and isinstance(choices[0], dict):
            return [Choice(id=choice['id'], name=choice['name'], color=choice['color']) for choice in choices]
        return [Choice(id=generate_id(), name=choice[0], color=choice[1].value) for choice in choices]

    def _add_column(self, col_id: str, table: Table):
        if table:
            self.table = table
            self.core = self.table.core
            self._workspace = self.core.workspace
            if col_id:
                return col_id
            else:
                if self.field_type is FieldType.TEXT:
                    column_config = ColumnConfigInput(type=self.field_type.value, name=self.name, order=self.order)
                elif self.field_type is FieldType.DATETIME:
                    column_config = ColumnConfigInput(type=self.field_type.value, name=self.name, order=self.order,
                                                      dateFormat=self.date_format.value,
                                                      includeTime=self.include_time, timeFormat=self.time_format.value,
                                                      useGMT=self.use_gmt)
                elif self.field_type is FieldType.MULTI_SELECT or self.field_type is FieldType.SELECT:
                    column_config = ColumnConfigInput(type=self.field_type.value, name=self.name, order=self.order,
                                                      choices=self.choices)
                elif self.field_type is FieldType.NUMBER:
                    column_config = ColumnConfigInput(type=self.field_type.value, name=self.name, order=self.order,
                                                      defaultNumber=self.default_number, precision=self.precision)
                elif self.field_type is FieldType.RECORD_REFERENCE:
                    column_config = ColumnConfigInput(type=self.field_type.value, name=self.name, order=self.order,
                                                      foreignTableId=self.foreign_table_id)
                # elif self.field_type is FieldType.FORMULA:
                #     column_config = ColumnConfigInput(type=self.field_type.value, name=self.name, order=self.order,
                #                                       foreignTableId=self.foreign_table_id)
                # elif self.field_type is FieldType.LOOKUP:
                #     column_config = ColumnConfigInput(type=self.field_type.value, name=self.name, order=self.order,
                #                                       foreignTableId=self.foreign_table_id)
                # elif self.field_type is FieldType.MULTI_ATTACHMENT:
                #     column_config = ColumnConfigInput(type=self.field_type.value, name=self.name, order=self.order)
                else:
                    raise ValueError('Not FieldType')
                add_col_input = AddColumnInput(workspaceId=self.workspace.id, coreId=self.core.id,
                                               tableId=self.table.id,
                                               columnConfig=column_config)
                col_id = TreeLabClient.add_column(add_col_input, workspace_id=self.workspace.id,
                                                  wait_till_complete=True,
                                                  name_spaces=[self.core.id, self.table.id, self.view_id]).id

                return col_id
        else:
            raise ValueError("You need to get/create the column from the table!")

    @property
    def data(self):
        return super().data

    def _get_event_id(self, event: EventPayload):
        return event.columnId


class Cell(_TreelabObject):
    __repr_fields__ = {'_id'}

    def __init__(self, table: Table, row: Row, column: Column, value: Dict = None
                 ):
        """

        :param table:
        :param row:
        :param column:
        :param value:


        """
        super().__init__()
        self.table = table
        self.core = self.table.core
        self._workspace = self.core.workspace
        self.row = row
        self.column = column
        self._value = value
        self._id = '{}:{}'.format(column.id, row.id)

    def update(self, value):
        """
        Update the value of the cell, the field_type can be inferred from self.row.field_type
        :param value:
                    column_type is FieldType.TEXT
        :return:
        """
        if self.column.field_type is FieldType.MULTI_SELECT:
            update_cell_input = UpdateCellInput(workspaceId=self.workspace.id, coreId=self.core.id,
                                                tableId=self.table.id, columnId=self.column.id, rowId=self.row.id,
                                                action=UpdateCellActionInput(type=UpdateAction.SET_VALUE.value,
                                                                             value=CellValueInput(
                                                                                 type=self.column.field_type.value,
                                                                                 selectedItems=value)))
        elif self.column.field_type is FieldType.SELECT:
            update_cell_input = UpdateCellInput(workspaceId=self.workspace.id, coreId=self.core.id,
                                                tableId=self.table.id, columnId=self.column.id, rowId=self.row.id,
                                                action=UpdateCellActionInput(type=UpdateAction.SET_VALUE.value,
                                                                             value=CellValueInput(
                                                                                 type=self.column.field_type.value,
                                                                                 selectedItem=value)))
        elif self.column.field_type is FieldType.TEXT:
            update_cell_input = UpdateCellInput(workspaceId=self.workspace.id, coreId=self.core.id,
                                                tableId=self.table.id, columnId=self.column.id, rowId=self.row.id,
                                                action=UpdateCellActionInput(type=UpdateAction.SET_VALUE.value,
                                                                             value=CellValueInput(
                                                                                 type=self.column.field_type.value,
                                                                                 text=value
                                                                             )))
        elif self.column.field_type is FieldType.NUMBER:
            update_cell_input = UpdateCellInput(workspaceId=self.workspace.id, coreId=self.core.id,
                                                tableId=self.table.id, columnId=self.column.id, rowId=self.row.id,
                                                action=UpdateCellActionInput(type=UpdateAction.SET_VALUE.value,
                                                                             value=CellValueInput(
                                                                                 type=self.column.field_type.value,
                                                                                 number=int(value),
                                                                             )))
        elif self.column.field_type is FieldType.DATETIME:
            update_cell_input = UpdateCellInput(workspaceId=self.workspace.id, coreId=self.core.id,
                                                tableId=self.table.id, columnId=self.column.id, rowId=self.row.id,
                                                action=UpdateCellActionInput(type=UpdateAction.SET_VALUE.value,
                                                                             value=CellValueInput(
                                                                                 type=self.column.field_type.value,
                                                                                 dateTime=value)))
        elif self.column.field_type is FieldType.RECORD_REFERENCE:
            update_cell_input = UpdateCellInput(workspaceId=self.workspace.id, coreId=self.core.id,
                                                tableId=self.table.id, columnId=self.column.id, rowId=self.row.id,
                                                action=UpdateCellActionInput(type=UpdateAction.ADD_VALUE.value,
                                                                             value=CellValueInput(
                                                                                 type=self.column.field_type.value,
                                                                                 foreignRowId=value
                                                                             )))
        # elif cell_type is FieldType.FORMULA:
        #     pass
        # elif cell_type is FieldType.MULTI_ATTACHMENT:
        #     pass
        # elif cell_type is FieldType.LOOKUP:
        #     pass
        else:
            raise ValueError('Not Cell_Type')

        _ = TreeLabClient.update_cell(update_cell_input, workspace_id=self.workspace.id,
                                      wait_till_complete=True, name_spaces=[self.core.id, self.table.id]).id

    @property
    def data(self):
        return self.table.data.cells[self.row.id, self.column.id]

    @property
    def value(self):
        """
        Get the last updated value dict if there is any, this is not guaranteed to be the most updated value,
        for most updated data, using cell.data
        :return:
        """
        return self._value

    @property
    def text(self):
        """
        Get the last updated value dict if there is any, this is not guaranteed to be the most updated value,
        for most updated data, using cell.data
        :return:
        """
        return self.value['text']

    def _get_event_id(self, event: EventPayload):
        return '{}:{}'.format(event.columnId, event.rowId)


class _TableData:
    def __init__(self, table: Table, table_dict: Dict):
        self.table = table
        self.table_dict = table_dict
        self._parse_dict(table_dict)

    def _parse_dict(self, table_dict: Dict):
        self._rows, self._views, self._columns, self._cells = {}, {}, {}, {}
        views = table_dict['views']
        for view_dict in views:
            view_id = view_dict['id']
            view_type = view_dict['type']
            view_name = view_dict['name']
            view = View(name=view_name, view_type=view_type, view_id=view_id, table=self.table)
            self._views[view_id] = view
            if 'columns' in view_dict:
                for column_dict in view_dict['columns']:
                    column_id = column_dict['id']
                    column_type = FieldType(column_dict['type'])
                    column_name = column_dict['name']
                    # column_order = column_dict.get('order')
                    # visibility = column_dict['visibility']
                    if column_type is FieldType.TEXT:
                        column = Column(view_id=view_id, col_id=column_id, field_name=column_name,
                                        table=self.table, field_type=column_type)
                    elif column_type is FieldType.RECORD_REFERENCE:
                        foreign_table_id = column_dict['foreignTableId']
                        column = Column(view_id=view_id, col_id=column_id, field_name=column_name,
                                        table=self.table, field_type=column_type, foreign_table_id=foreign_table_id)
                    elif column_type is FieldType.NUMBER:
                        default_number = column_dict['defaultNumber']
                        precision = column_dict['precision']
                        column = Column(view_id=view_id, col_id=column_id, field_name=column_name,
                                        table=self.table, field_type=column_type, default_number=default_number,
                                        precision=precision)
                    elif column_type is FieldType.SELECT or column_type is FieldType.MULTI_SELECT:
                        choices = eval(column_dict['choices'])
                        column = Column(view_id=view_id, col_id=column_id, field_name=column_name,
                                        table=self.table, field_type=column_type, choices=choices)
                    elif column_type is FieldType.MULTI_ATTACHMENT:
                        column = Column(view_id=view_id, col_id=column_id, field_name=column_name,
                                        table=self.table, field_type=column_type)
                    elif column_type is FieldType.DATETIME:
                        date_format = column_dict['dateFormat']
                        include_time = column_dict['includeTime']
                        time_format = column_dict['timeFormat']
                        use_gmt = column_dict['useGMT']
                        column = Column(view_id=view_id, col_id=column_id, field_name=column_name,
                                        table=self.table, field_type=column_type, date_format=date_format,
                                        include_time=include_time,
                                        time_format=time_format, use_gmt=use_gmt)
                    else:
                        raise ValueError('Not FieldType')
                    self._columns[column_id] = column

            if 'rows' in view_dict:
                for row_dict in view_dict['rows']:
                    row_id = row_dict['id']
                    row = Row(view_id=view_id, row_id=row_id, table=self.table)
                    self._rows[row_id] = row
                    if 'cells' in row_dict:
                        for cell_dict in row_dict['cells']:
                            column_id = cell_dict['columnId']
                            column_type = FieldType(cell_dict['type'])
                            if column_type is FieldType.TEXT:
                                value = cell_dict['text']
                            elif column_type is FieldType.RECORD_REFERENCE:
                                value = cell_dict['foreignRow'][0]['id']
                            elif column_type is FieldType.NUMBER:
                                value = cell_dict['number']
                            elif column_type is FieldType.SELECT:
                                value = eval(cell_dict['selectedItem'])
                            elif column_type is FieldType.MULTI_SELECT:
                                value = eval(cell_dict['selectedItems'])
                            elif column_type is FieldType.MULTI_ATTACHMENT:
                                value = cell_dict['attachments']
                            elif column_type is FieldType.DATETIME:
                                value = cell_dict['dateTime']
                            else:
                                raise ValueError('Not FieldType')
                            cell = Cell(table=self.table, row=row, column=self._columns[column_id], value=value)
                            self._cells[row_id, column_id] = cell

    @property
    def cells(self) -> Dict:
        return self._cells

    @property
    def rows(self) -> Dict:
        return self._rows

    @property
    def views(self) -> Dict:
        return self._views

    @property
    def columns(self) -> Dict:
        return self._columns


class _TreelabObjectArray(Listenable, Generic[GenericType.PT, GenericType.T]):
    def __init__(self, parent_object: GenericType.PT, objects: List[GenericType.T], workspace):
        super().__init__(workspace)
        self.parent_object = parent_object
        self._objects = objects
        self._size = len(objects)

    def __iter__(self) -> Iterator[GenericType.T]:
        return self._objects.__iter__()

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.__class__(self.parent_object, self._objects[item], self.workspace)
        else:
            return self._objects[item]

    def __contains__(self, obj: GenericType.T) -> bool:
        return obj in self._objects

    def __len__(self) -> int:
        return len(self._objects)

    @property
    def size(self):
        return self._size

    def select(self, filter_func: Callable[[GenericType.T], bool], max_size: int = None):
        """
        Select the objects that meet conditions specified by filter_func
        :param filter_func:
        :param max_size:
        :return:
        """
        selected_objs: List[GenericType.T] = list(filter(filter_func, self._objects))
        if max_size:
            selected_objs = selected_objs[:max_size]

        return _TreelabObjectArray(self.parent_object, selected_objs, self.workspace)

    def select_by_name(self, name):
        return self.select(filter_func=lambda obj: obj.name == name)

    def sort(self, sort_function: Callable[[GenericType.T], bool], max_size: int = None):
        """
        Sort the objects by sort_function
        :param sort_function:
        :param max_size:
        :return:
        """
        sorted_objs: List[GenericType.T] = sorted(self._objects, key=sort_function)[:max_size]
        if max_size:
            sorted_objs = sorted_objs[:max_size]

        return _TreelabObjectArray(self.parent_object, sorted_objs, self.workspace)

    def listen_to(self, listener: Union[Callable[[EventPayload], Any], Listener], name: str = None,
                  thread_num: int = 0, user_only: bool = True):
        """
        Register the listener to every single object in the collection
        :param listener:
        :param name:
        :param thread_num:
        :param user_only:
        :return:
        """
        for i, obj in enumerate(self._objects):
            obj.listen_to(listener, '{}_{}'.format(name, i), thread_num, user_only)

    def __repr__(self):
        return self._objects.__repr__()


class CellArray(_TreelabObjectArray[Table, Cell]):
    def __init__(self, parent_object: GenericType.PT, objects: List[GenericType.T], workspace: Workspace):
        super().__init__(parent_object, objects, workspace)
        self._shape = (self.size, 1)
        self.current_cells = objects

    @property
    def shape(self):
        return self._shape

    @property
    def matrix(self) -> np.array:
        """
        Get the text matrix representation of the cells
        :return:
        """
        return self.parent_object.data.cells
        # matrix = np.array([[self.objects[i * self.shape[1] + j].data.text for j in range(self.shape[1])]
        #                    for i in range(self.shape[0])])
        #
        # return matrix

    def update_all(self, value: str):
        """
        Update all the cells with the same value
        :param value:
        :return:
        """
        for obj in self._objects:
            obj.update(value=value)

    def reshape(self, shape: Tuple[int, int]):
        """
        Reshaping cells to certain shape as long as the size matches the product of width and length of the shape
        :param shape:
        :return:
        """
        m, n = shape
        if m * n != self.size:
            raise ValueError('The product of width and length of the shape must equals to the size of cells')
        self._shape = shape

        return self

    def flatten(self):
        """
        Flattening the cells into vector
        :return:
        """
        self._shape = (self.size, 1)

        return self

    def update(self, data_matrix: Union[List[List], np.array, pd.DataFrame],
               reshape: bool = True):
        """
        Update the cells with data_matrix, use reshape when you want to fit the matrix into the cells
        The shape of cell_type_matrix and data_matrix must be consistent and used to verify the cell field type
        :param data_matrix:
        :param reshape:
        :return:
        """
        data_matrix = self._convert_to_matrix(data_matrix)
        n_rows, n_cols = data_matrix.shape

        if reshape:
            self.reshape(data_matrix.shape)
        for i in range(n_rows):
            for j in range(n_cols):
                if data_matrix[i, j] != '':
                    self._objects[i * n_cols + j].update(value=data_matrix[i, j])

    @staticmethod
    def _convert_to_matrix(data):
        if isinstance(data, List):
            if len(data) == 0:
                raise ValueError('The size of the data matrix must not be zero')
            data = np.array(data)

        return data

    def values_dict(self) -> Dict:
        return {obj.id: obj.value for obj in self._objects}

    def __repr__(self):
        return self.matrix.__repr__()


class CoreArray(_TreelabObjectArray[Workspace, Core]):
    pass


class TableArray(_TreelabObjectArray[Core, Table]):
    pass


class RowArray(_TreelabObjectArray[Table, Row]):
    pass


class ColumnArray(_TreelabObjectArray[Table, Column]):
    pass


class ViewArray(_TreelabObjectArray[Table, View]):
    pass


@contextmanager
def subscribe_under(workspace: Workspace):
    try:
        yield
    finally:
        workspace.event_handler._subscribe_all()
        print('All listeners subscribed')
        threading.Event().wait(500)
        workspace.dispose()


def get_choice(choices: List[List[Choice]]):
    return [Choice(id=generate_id(), name=choice[0], color=choice[1].value) for choice in choices]
