# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from . import price_pb2 as price__pb2


class PriceStub(object):
  """The price service definition.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetPrice = channel.unary_unary(
        '/price.Price/GetPrice',
        request_serializer=price__pb2.PriceRequest.SerializeToString,
        response_deserializer=price__pb2.PriceReply.FromString,
        )
    self.GetAllTariffsAndUtilities = channel.unary_unary(
        '/price.Price/GetAllTariffsAndUtilities',
        request_serializer=price__pb2.Empty.SerializeToString,
        response_deserializer=price__pb2.AllTariffUtilityReply.FromString,
        )
    self.GetTariffAndUtility = channel.unary_unary(
        '/price.Price/GetTariffAndUtility',
        request_serializer=price__pb2.BuildingRequest.SerializeToString,
        response_deserializer=price__pb2.TariffUtilityReply.FromString,
        )


class PriceServicer(object):
  """The price service definition.
  """

  def GetPrice(self, request, context):
    """A simple RPC.

    Sends a price for a utility, tariff, type, duration (start, end), and window
    A PriceReply with an empty name is returned if there are no prices for the given request
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetAllTariffsAndUtilities(self, request, context):
    """Sends all available tariffs and utilities
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetTariffAndUtility(self, request, context):
    """Sends a tariff and utility for the specified building name
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_PriceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetPrice': grpc.unary_unary_rpc_method_handler(
          servicer.GetPrice,
          request_deserializer=price__pb2.PriceRequest.FromString,
          response_serializer=price__pb2.PriceReply.SerializeToString,
      ),
      'GetAllTariffsAndUtilities': grpc.unary_unary_rpc_method_handler(
          servicer.GetAllTariffsAndUtilities,
          request_deserializer=price__pb2.Empty.FromString,
          response_serializer=price__pb2.AllTariffUtilityReply.SerializeToString,
      ),
      'GetTariffAndUtility': grpc.unary_unary_rpc_method_handler(
          servicer.GetTariffAndUtility,
          request_deserializer=price__pb2.BuildingRequest.FromString,
          response_serializer=price__pb2.TariffUtilityReply.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'price.Price', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
