# Usage

The Treelab Python API provides an easy way to integrate Treelab with any external system. The API closely follows REST semantics, uses JSON to encode objects, and relies on standard HTTP codes to signal operation outcomes.

## Installation
    
    pip install treelab

## Reference
    
    from treelab.api import *

# Dictionary

## Core 
A core contains a collection of tables. A table can belong to multiple Cores. 

## Table 
A table is a collection of fields and rows. Each table is also made up of a series of different views. 


## Views 
A view is essentially a materialized view of a table's data. The same table data can be visualized in a variety of different ways. The current view types supported are: 

- `Grid View` 
- `Timeline View` 
- `List View` 
- `Form View (*After alpha release)`
- `Kanban View (*After alpha release)`

Views can not only be used to create interactive visualizations, but it can also be used to pass data from one user/process to another. By applying different filter conditions, the admin user can essentially configure data flow by inviting different users to different views. 

## Field Types
Treelab has a lot of rich field types but the main field types are: 

- `Number`
- `Text`
- `Record Reference`
- `Table Reference` 
- `Core Reference`
- `Formula` 
- `Single Select`
- `Multi-Select`
- `Collaborator (User)`

# Events 
Treelab is an event-driven system that encodes all state and data changes within the system into a series of `events`. These `events` are then written into a series of different `topics`, which can then be consumed by different parties for processing. Treelab's Python SDK abstracts these events into different Python objects that can then be used to read and write data from Treelab. 

## Topic 
A topic is an event stream name-spaced by workspace ID. You can use topics to subscribe for data changes within a specific workspace, and then invoke custom callback functions upon those events. 
The current set of `topics` available to the Python SDK are the following: 

- `WorkspaceCreated`
- `CoreCreated`
- `TableCreated`
- `TableAdded`
- `CellUpdated`
- `ColumnAdded`
- `RowAdded`

## Example Event Data

    {
      "topic": "ColumnAdded",
      "attributes": {
              "workspaceId": "wspb515f6837a07c6d3",
              "coreId": "creb515f6846406b982",
              "tableId": "tblb515f684b30a52b0",
              "columnId": "colb515f6874682258c",
              "columnConfig": {
                      "type": "TEXT",
                      "name": "Test Column",
                      "order": 0,
                      "foreignTableId": "",
                      "default": 0,
                      "precision": 0
              },
              "_metadata": {
                      "source": "EXTERNAL_API",
                      "userId": "usr15f684b30a52123d2",
                      "aggregateId": "tblb515f684b30a52b0",
                      "sequence": 1
              }
        }
    }


# Treelab Objects

`_TreelabObject` are the backbone of all operations in Treelab, that includes `Workspace`, 
`Core`, `Table`, `Row`, `Column` and `Cell`. 

For each `TreelabObject`, there are 

attributes:
   - `id`
   - `name`

`_TreelabObject` inherits `BasicListenable` class which has the following function.
`BasicListenable` and its parent class `Listenable` are classes that can be listened by the `Listener`. The `Listener`,
`Listenable` and all the subscription related classes and functions will be introduced later in this document.
   
functions:   
 - `listen_to(listener: Listener)` which will be used for event subscription.
 

## Workspace

Workspace is the heart of the bud and is where a bud is developed upon, all the events initially
subscribes to the workspace through `workspace.event_handler`.

#### Create a new workspace
    workspace: Workspace = Treelab.add_workspace(name: str)

#### Get a pre-created a workspace from workspace_id
    workspace: Workspace = Treelab.workspace(workspace_id: str)

## Core

`Core` lies right under workspace and can be and only be created from workspace

#### Create a new core
    core: Core = workspace.add_core(name: str)

#### Get a pre-created a core from `core_id`
    core: Core = workspace.core(core_id: str)
    # or
    core: Core = workspace.get_core(core_id: str)

#### Get a snapshots
    core: Core= workspace.core(core_id: str).snapshots()
    
## Table

Similar to core, `Table` is a `TreelabObject` below `Core`.

#### Create a new table
    table: Table = core.add_table(name='table_name')

#### Get a pre-created a table from `table_id`
    table: Table = core.table(table_id: str) 
    # or
    table: Table = core.get_table(table_id: str)
    
## View

`View` is a `TreelabObject` below `Table`.

#### Create a new view on table
    view: View = table.add_view(name='table_name')

#### Get a pre-created a table from `table_id`
    view: View = table.view(view_id: str) 
    # or
    table: Table = table.get_view(view_id: str)
    
## Row

#### Create a new row
    row: row = table.add_row()
    
#### Create multiple rows
    column: Column = table.add_column(n_rows: int)

#### Get a pre-created a row from row_id
    row: Row = table.row(row_id: str) 
    # or
    row: Row = table.get_row(row_id: str)

## Column

#### Create a new column
    column: Column = table.add_column(field_type: FieldType, field_name: str, order: int, foreign_table_id: str)
    # or
    column_config = ColumnConfig(field_type: FieldType, name: str, order: int, foreign_table_id: str)
    column: Column = table.add_column(column_config: ColumnConfig)

#### Get a pre-created a column from column_id
    column: Column = table.column(row_id='rowb5174b4f9b897333') 
    # or
    column: Column = table.get_column(row_id='rowb5174b4f9b897333')
    
#### Create multiple columns
    table.add_columns(column_configs: List[ColumnConfig])
    
    
## Cell

#### Get a single `cell` from `row` and `column`
    cell: Cell = table.get_cell(row, column)
    
#### Get cells from `row`s and `column`s with three different mode
    
    # get the cells created by the intersection of rows and columns
    # i.e [rows -> [row1, row2], columns -> [col1, col2]] -> 
    [cell(row1, col1), cell[row1, col2], cell(row2, col1), cell(row2, col2)]
    
    cells: CellArray = table.get_cells(rows, columns, mode='intersection')
    
    
    # get the cells created by rows and columns pairs
    # i.e [rows -> [row1, row2], columns -> [col1, col2]] -> 
    cell(row1, col1), cell(row2, col2)
    
    cells: CellArray = table.get_cells(rows, columns, mode='pair')
    
    # get all cells of the table, rows and columns will be ignored here
    cells CellArray = table.get_cells(mode='all')
    
    
## _TreelabObjectArray

`_TreelabObjectArray` is the parent class for `CoreArray`, `TableArray`, `ViewArray`,
`ColumnArray`, `RowArray` and `CellArray`. It supports batch operations like
`update` and `listen_to` functions for each object inside of it. 

It also has functions for object selection and sortings on the objects

- `select(max_size: int, filter_func: Callable[T, bool])`
- `sort(max_size: int, sort_func: Callable[T, Any])`

You will get `_TreelabObjectArray` when doing queries like 

    cells: CellArray = table.get_cells()
    columns: ColumnArray = table.get_columns()

# Higher Level Functions

## Update a table
    
    table.update(data_matrix: Union[np.array, pd.DataFrame, List[List[str]]])
    
## Update a row

    # Update a whole row    
    row.update(vector: List[str])
    
    # Update specific columns of the row, requiring the size of the vector 
    equals the size of the columns
    row.update(vector: List[str], columns=List[Column])
    

# Examples

## add_table_with_content
        
    field_types = [FieldType.TEXT] * 2
    field_names = ['col_{0}'.format(i) for i in range(2)]
    data_matrix = [['Treelab', 'is'], ['sooo', 'awesome']]

    table = Treelab.workspace(workspace_id='wspb5290314c6886fe7').
                core(='creb5174b2e64889940').
                add_table_with_content(table_name='fancy table name', 
                                       view_name='fancy view name', 
                                       view_type=ViewType.GRID, 
                                       field_types=field_types,
                                       field_names=field_names,
                                       data_matrix=data_matrix)

    
    
## add_columns


    column_configs = [
            ColumnConfig(field_type=FieldType.TEXT, 
                         name='col_{0}'.format(i), 
                         order=i, 
                         foreign_table_id='')
                         for i in range(3)]
    
    columns: List[Column] = Treelab
                .workspace(workspace_id='wspb5174b2e27034a57').
                core(core_id='creb5174b2e64889940').
                table(table_id='tblb5174b452c885294').
                add_columns(column_configs)
    

## Updating a row
    vector = ['1', '2', '3']
    
    column_configs = [
            ColumnConfig(field_type=FieldType.TEXT, 
                         name='col_{0}'.format(i), 
                         order=i, 
                         foreign_table_id='')
                         for i in range(3)]
                         
    table = Treelab.workspace(workspace_id='wspb5174b2e27034a57').
                        core(core_id='creb5174b2e64889940').
                        table(table_id='tblb5174b452c885294')
                        row(row_id='rowb517dac3bb88cfb9')
    

    columns = table.add_columns(column_configs)
    rows = table.add_rows(3)
    
    rows[0].update(vector=vector)
    row[1].update(vector[:2], columns[:2])
    row[2].update(vector[1:], columns[1:])
    
    
## add_rows

    rows: List[Row] = Treelab.workspace(workspace_id='wspb5174b2e27034a57').
                core(core_id='creb5174b2e64889940').
                table(table_id='tblb5174b452c885294').
                add_rows(n_rows=2)
    row_ids = [row.id for row in rows]


# Subscriptions

## Event payload

This is the object you will receive in the subscription stream. It has the format,


    eventName: "creb5174b2e64889940.tblb5174b452c885294.CellUpdated"
    workspaceId: "wspb5174b2e27034a57"
    coreId: "creb5174b2e64889940"
    tableId: "tblb5174b452c885294"
    columnId: "colb5174b55ec0f785d"
    rowId: "rowb5174b4f9b897333"
    value {
      type: "TEXT"
      text: "2"
    }

For example, to get the `columnId` in the `event`, you can simply use `event.columnId`. 

## Listener

`Listener` defines what can be done during the event subscription. A listener can be either a function that takes an `event: EventPayload` as input, or inherit `Listener` class by overriding the `run(event: EventPayload)` function.

## Listenable

`Listenable` defines an object that can be listened to. It's basic implementation is called `BasicListenable` and will 
be the object that you will inherit at most times.

To build your own `Listenable`, you should at least implement one abstract function

```should_be_listened(self, event: EventPayload, listener: Listener) -> bool```

This function basically defines when the `run(self, event: EventPayload)` function should be triggered in Listener.

Every `_TreelabObject` including `Core`, `Table`, `Column` etc, has inherited `Listenable` and is already well implemented so you can simply call `listen_to` on them to get the 
`listener: Listener` registered to the object.


## Examples

### Subscribing to all event changes for a Table
       
    def table_update_listener(event: EventPayload):
        print("Table " + event.tableId + " Updated")
            
    workspace = Treelab.workspace(name="workspace")
    # use the with statement to subscribe to the workspace created
    with subscribe_under(workspace):
        # create a table and core
        table = workspace.add_core("corename").add_table("tablename")            
        table.listen_to(table_update_listener, 'listen')
                
### Subscribing to all event changes for a Column
       
    def col_update_listener((event: EventPayload):
            print("Column " + event.tableID + " Updated")
        
    # create a new workspace
    workspace = Treelab.workspace(name="workspace")
    # use the with statement to subscribe to the workspace created
    with subscribe_under(workspace):
        table = workspace.add_core(name="corename").add_table(name="tablename")
        view = table.add_view(name="viewname", ViewType.GRID)
        rows = table.add_rows(3)
        column_configs = [ColumnConfig(field_type=FieldType.TEXT,name='col_{0}'.format(i),order=i,foreign_table_id='')
                           for i in range(5)]
        columns = table.add_columns(column_configs)
        columns.listen_to(update_col, 'listen')

                
### Subscribing to all event changes for a Row
       
    def row_update_listener(event: EventPayload):
        print("Row " + event.tableID + " Updated")
        
    # create a new workspace
    workspace = Treelab.workspace(name="workspace")
    # use the with statement to subscribe to the workspace created
    with subscribe_under(workspace):
        # create table
        table = workspace.add_core(name="corename").add_table(name="tablename")
        view = table.add_view(name="viewname", ViewType.GRID)
        rows = table.add_rows(3)
        # rows will listen to the row changes        
        rows.listen_to(row_update_listener, 'listener_row')
                
           
### Subscribing to all event changes for a Cell
   Cells are collections of cells, which means that each cell in the collection
   is listened to by a custom function
       
    def cell_update_listener(event: EventPayload):
        print("Cell " + event.tableID + " Updated")
    
    # create a new workspace
    workspace = Treelab.workspace(name="workspace")
    # use the with statement to subscribe to the workspace created
    with subscribe_under(workspace):
        # add a new core to the workspace with name "corename"
        core = workspace.add_core(name="corename")
        # add a new table to the core with name "tablename"
        table = core.add_table(name="tablename")
        # add a view to the table with name "viewname"
        view = table.add_view(name="viewname", ViewType.GRID)
        # add three rows to the table
        rows = table.add_rows(3)
        # define column configs
        column_configs = [ColumnConfig(field_type=FieldType.TEXT,name='col_{0}'.format(i),order=i,foreign_table_id='')
                           for i in range(5)]
        # add new columns to the table
        columns = table.add_columns(column_configs)
        # get all cells from the table given rows and columns
        cells = table.get_cells(rows, columns)
        # let all cells listen to the update_cell listener
        cells.listen_to(cell_update_listener, 'listener_cell')
                
### Building your customized Listener and Listenable

    class OrderEntry:
    def __init__(self):
        pass


    class OrderDAO(BasicListenable):
        def __init__(self, workspace: Workspace):
            super().__init__(workspace)
            self._id = None
            self.orders: List[OrderEntry] = []
        
        # when should OrderDAO be listened, it is equivalent to say when should the listener be triggered    
        def should_be_listened(self, event: EventPayload, listener: Listener):
            order_columns = self.workspace.core(event.coreId).table(event.tableId).get_column_by_name("order")
            if order_columns:
                return True
            return False
            
            
    class OrderListener(Listener[OrderDAO]):
        
        # The listener will take all the listenables that it registered to, and run your defined customized functions
        def run(self, event: EventPayload):
            # listenable_list = [completed_order_dao, non_completed_order_dao]
            for listenable in self.listenable_list:
                listenable.orders.append(OrderEntry())
                
    if __name__ == '__main__':
        wkspace = Treelab.add_workspace("workspace_name")
        
        with subscribe_under(wkspace):
            completed_order_dao = OrderDAO(wkspace)
            non_completed_order_dao = OrderDAO(wkspace)
            order_listener = OrderListener('name')
            completed_order_dao.listen_to(order_listener)
            non_completed_order_dao.listen_to(order_listener)
