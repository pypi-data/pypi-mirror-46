import treelab.grpc.messages.service_pb2_grpc as treelab_service
from treelab.consts import GRPCConfig
from treelab.grpc.messages.service_pb2 import *
from treelab.utils.decorator_utils import *

"""
Interfacing Treelab gRPC APIs
"""


class TreeLabClient:
    channel = grpc.insecure_channel(GRPCConfig.ip)
    client = treelab_service.TreeLabApiServiceStub(channel)
    metadata = [('access_token', GRPCConfig.TOKEN)]

    @classmethod
    @wait("WorkspaceCreated")
    def create_workspace(cls, create_workspace_input: CreateWorkspaceInput):
        return cls.client.CreateWorkspace, create_workspace_input, cls.metadata

    @classmethod
    @wait("CoreCreated")
    def add_core(cls, add_core_input):
        return cls.client.AddCore, add_core_input, cls.metadata

    @classmethod
    @wait("TableCreated")
    def add_table(cls, add_table_input: AddTableInput):
        return cls.client.AddTable, add_table_input, cls.metadata

    @classmethod
    @wait("ViewAdded")
    def add_view(cls, add_view_input: AddViewInput):
        return cls.client.AddView, add_view_input, cls.metadata

    @classmethod
    @wait("ColumnAdded")
    def add_column(cls, add_column_input: AddColumnInput):
        return cls.client.AddColumn, add_column_input, cls.metadata

    @classmethod
    @wait("RowAdded")
    def add_row(cls, add_row_input: AddRowInput):
        return cls.client.AddRow, add_row_input, cls.metadata

    @classmethod
    @wait("CellUpdated")
    def update_cell(cls, update_cell_input: UpdateCellInput):
        return cls.client.UpdateCell, update_cell_input, cls.metadata

    @classmethod
    def get_all_workspaces(cls):
        return cls.client.GetAllWorkspaces(EmptyInput(), metadata=cls.metadata)

    @classmethod
    def subscribe_to_workspace(cls, subscription_input: WorkspaceSubscriptionInput):
        return cls.client.SubscribeToWorkspace(subscription_input, metadata=cls.metadata)

    @classmethod
    def get_workspace(cls, get_workspace_input: GetWorkspaceInput):
        return cls.client.GetWorkspace(get_workspace_input)

    @classmethod
    def get_table(cls, get_table_input: GetTableInput):
        return cls.client.GetTable(get_table_input)

    @classmethod
    def get_all_tables(cls, get_tables_input: GetTablesInput):
        return cls.client.GetAllTables(get_tables_input)

    @classmethod
    def get_core(cls, get_core_input: GetCoreInput):
        return cls.client.GetCore(get_core_input)
