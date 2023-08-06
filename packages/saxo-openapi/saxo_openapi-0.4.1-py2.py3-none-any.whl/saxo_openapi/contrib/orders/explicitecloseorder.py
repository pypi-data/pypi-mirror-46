# -*- coding: utf-8 -*-

from .baseorder import BaseOrder
from .helper import direction_from_amount, order_duration_spec
import saxo_openapi.definitions.orders as OD


class ExplicitePositionCloseOrder(BaseOrder):
    """create a LimitOrder.

    LimitOrder is used to build the body for a LimitOrder. The body can be
    used to pass to the Order endpoint.
    """

    # allowed OrderDurationTypes:
    ALLOWED_DT = [OD.OrderDurationType.DayOrder,
                  OD.OrderDurationType.GoodTillDate,
                  OD.OrderDurationType.GoodTillCancel]

    def __init__(self,
                 Uic,
                 Amount,
                 AssetType,
                 OrderPrice,
                 AmountType=OD.AmountType.Quantity,
                 OrderDurationType=OD.OrderDurationType.DayOrder,
                 GTDDate=None):
        """
        Instantiate a ExplicitePositionCloseOrder.

        Parameters
        ----------

        Uic: int (required)
            the Uic of the instrument to trade

        Amount: decimal (required)
            the number of lots/shares/contracts or a monetary value
            if amountType is set to CashAmount

        OrderPrice: decimal (required)
            the price indicating the limitprice

        AssetType: string (required)
            the assettype for the Uic

        AmountType: AmountType (optional)
            the amountType, defaults to Quantity, see AmountType for
            other options

        OrderDurationType: string, default DayOrder
            the order duration type, check SAXO Bank specs. for details

        GTDDate: datetime string (required if order duration is GoodTillDate)
            the GTD-datetime

        Example
        -------

        >>> import json
        >>> from saxo_openapi import API
        >>> import saxo_openapi.endpoints.trading as tr
        >>> from saxo_openapi.contrib.orders import ExplicitePositionCloseOrder
        >>>
        >>> lo = ExplicitePositionCloseOrder(Uic=21,
        ...                 AssetType=OD.AssetType.FxSpot,
        ...                 Amount=10000,
        ...                 OrderPrice=1.1025)
        >>> print(json.dumps(lo.data, indent=2))
        {
          "Uic": 21,
          "AssetType": "FxSpot",
          "Amount": 10000,
          "Price": 1.1025,
          "BuySell": "Buy",
          "OrderType": "Limit",
          "AmountType": "Quantity",
          "OrderDuration": {
             "DurationType": "DayOrder"
          }
        }
        >>> # now we have the order specification, create the order request
        >>> r = tr.orders.Order(data=lo.data)
        >>> # perform the request
        >>> rv = client.request(r)
        >>> print(rv)
        >>> print(json.dumps(rv, indent=4))
        {
           "OrderId": "76697286"
        }
        """

        super(LimitOrder, self).__init__()

        # by default for a Limit order
        da = {
             'OrderType': OD.OrderType.Limit,
             'AmountType': AmountType,
        }

        da.update({'OrderDuration': order_duration_spec(OrderDurationType,
                                                        self.ALLOWED_DT,
                                                        GTDDate)})

        # required
        self._data.update({"Uic": Uic})
        self._data.update({"AssetType": AssetType})
        self._data.update({"Amount": abs(Amount)})
        self._data.update({"OrderPrice": OrderPrice})
        self._data.update({"BuySell": direction_from_amount(Amount)})
        self._data.update(da)

    @property
    def data(self):
        """data property.

        return the JSON body.
        """
        return super(LimitOrder, self).data
