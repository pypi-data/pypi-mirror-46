from shioaji.base import BaseObj, attrs
from shioaji.account import Account
from shioaji.orderprops import OrderProps


@attrs
class Trade(BaseObj):
    """ the base trade object

    Attributes:
        contract (:obj:Contract): 
        order (:obj:Order):
        status (:obj:OrderStatus):
    """
    _defaults = dict(
        contract=None,
        order=None,
        status=None,
        log=[],
    )

    def calculate_remain(self):
        ostatus = self.status
        ostatus._remaining = self.order.quantity - ostatus.deal_quantity - ostatus.cancel_quantity

    def fupdate_status(self):  #need test for this function
        ostatus = self.status
        seqno = self.order.seqno
        self.calculate_remain()
        if not seqno:
            ostatus._status = Status.PendingSubmit
        elif ostatus.cancel_quantity == self.order.quantity:
            ostatus._status = Status.Cancelled
        elif not ostatus.remaining:
            ostatus._status = Status.Filled
        elif ostatus.deal_quantity:
            ostatus._status = Status.Filling
        elif ostatus.status_code == '0000':
            ostatus._status = Status.Submitted
        elif ostatus.status_code == '8014':
            ostatus._status = Status.PreSubmitted
        else:
            ostatus._status = Status.Failed

    def supdate_status(self):
        ostatus = self.status
        seqno = self.order.seqno
        self.calculate_remain()
        if not seqno:
            ostatus._status = Status.PendingSubmit
        elif ostatus.cancel_quantity == self.order.quantity:
            ostatus._status = Status.Cancelled
        elif not ostatus.remaining:
            ostatus._status = Status.Filled
        elif ostatus.deal_quantity:
            ostatus._status = Status.Filling
        elif ostatus.status_code == '00':
            ostatus._status = Status.Submitted
        elif ostatus.status_code == 'PR':
            ostatus._status = Status.PreSubmitted
        elif ostatus.status_code == '88':
            ostatus._status = Status.Failed
        else:
            ostatus._status = Status.Failed


class Status:
    Cancelled = 'Cancelled'
    Filled = 'Filled'
    Filling = 'Filling'
    Inactive = 'Inactive'
    Failed = 'Failed'
    PendingSubmit = 'PendingSubmit'
    PreSubmitted = 'PreSubmitted'
    Submitted = 'Submitted'
    _DoneStates = {'Cancelled', 'Filling', 'Filled', 'Inactive', 'Failed'}
    # Failed, PartFilled
    _ActiveStates = {'PendingSubmit', 'PreSubmitted', 'Submitted'}


@attrs
class OrderStatus(BaseObj):
    """ the status of order after placed

    Attributes:
        order_id (str): the unique id of order
        status (str): the status of order
        status_code (str): the status code of order
        errmsg (str): error message of order
        modified_price(float or int): the modified price of the order 
        deal_price (float or int): the deal price of the order
        deal_quantity (int): the deal quantity of the order
        cancel_quantity (int): the cancel quantity of the order
        remaining (int): the rest of order quantity still wait for match
        avg_fillprice (float): the mean of deal price
        last_fillprice (float): the latest deal price of the order
        order_datetime (:obj:datetime): the timestamp of order send to server
    """
    _defaults = dict(
        order_id='',
        status='',
        status_code=0,
        msg='',
        modified_price=0,
        deal_quantity=0,
        cancel_quantity=0,
        remaining=0,
        avg_deal_price=0,
        deal_amount=0,
        last_deal_datetime=None,
        order_datetime=None,
    )
    _DoneStates = {'Cancelled', 'Filling', 'Filled', 'Inactive', 'Failed'}
    # Failed, PartFilled
    _ActiveStates = {'PendingSubmit', 'PreSubmitted', 'Submitted'}
    # need to define metaclass for check wether input inside defaults


@attrs
class Order(BaseObj):
    """ The basic order object to place order

    Attributes:
        action (str): order action to buy or sell
            - OrderProp.Stock.action.Buy
            - OrderProp.Stock.action.Sell
            - OrderProp.Future.action.Buy
            - OrderProp.Future.action.Sell
        price_type (str): pricing type of order
            - OrderProps.Stock.price_type.LimitPrice
            - OrderProps.Stock.price_type.Close
            - OrderProps.Stock.price_type.LimitUp
            - OrderProps.Stock.price_type.LimitDown
            - OrderProps.Future.price_type.LMT
            - OrderProps.Future.price_type.MKT
            - OrderProps.Future.price_type.MKP
        order_type (str): the type of order
            - OrderProps.Stock.order_type.Common
            - OrderProps.Stock.order_type.BlockTrade
            - OrderProps.Stock.order_type.Fixing
            - OrderProps.Stock.order_type.Odd
            - OrderProps.Future.order_type.ROD: Rest of Day
            - OrderProps.Future.order_type.IOC: Immediate-or-Cancel
            - OrderProps.Future.order_type.FOK: Fill-or-Kill
        order_cond (str): order condition
            - OrderProps.Stock.order_cond.Cash
            - OrderProps.Stock.order_cond.Netting
            - OrderProps.Stock.order_cond.MarginTrading
            - OrderProps.Stock.order_cond.ShortSelling
        octype (str): the type or order to open new position or close position 
            - OrderProps.Future.octype.Auto
            - OrderProps.Future.octype.NewPosition
            - OrderProps.Future.octype.Cover
            - OrderProps.Future.octype.DayTrade
        price (float or int): the price of order
        quantity (int): the quantity of order
        account (:obj:Account): which account to place this order
        ca (binary): the ca of this order

    """
    _defaults = dict(
        product_id='',
        action='',
        price_type='',
        order_type='',
        order_cond=OrderProps.Stock.order_cond.Cash,
        octype=OrderProps.Future.octype.Auto,
        mttype='',
        price=0,
        quantity=0,
        seqno='',
        ordno='',
        first_sell=OrderProps.Stock.first_sell.No,
        account=Account(),
        ca=b'',
    )
    _ignore_nondef = ('ca',)

    def __init__(self, price, quantity, action, price_type, order_type, *args,
                 **kwargs):
        """ the __init__ method of order

        Args:
            price (float or int): the price of order
            quantity (int): the quantity of order
            action (str): order action to buy or sell
                - OrderProp.Stock.action.Buy
                - OrderProp.Stock.action.Sell
                - OrderProp.Future.action.Buy
                - OrderProp.Future.action.Sell
            price_type (str): pricing type of order
                - OrderProps.Stock.price_type.LimitPrice
                - OrderProps.Stock.price_type.Close
                - OrderProps.Stock.price_type.LimitUp
                - OrderProps.Stock.price_type.LimitDown
                - OrderProps.Future.price_type.LMT
                - OrderProps.Future.price_type.MKT
                - OrderProps.Future.price_type.MKP
            order_type (str): the type of order
                - OrderProps.Stock.order_type.Common
                - OrderProps.Stock.order_type.BlockTrade
                - OrderProps.Stock.order_type.Fixing
                - OrderProps.Stock.order_type.Odd
                - OrderProps.Future.order_type.ROD: Rest of Day
                - OrderProps.Future.order_type.IOC: Immediate-or-Cancel
                - OrderProps.Future.order_type.FOK: Fill-or-Kill
            order_cond (str): order condition
                - OrderProps.Stock.order_cond.Cash
                - OrderProps.Stock.order_cond.Netting
                - OrderProps.Stock.order_cond.MarginTrading
                - OrderProps.Stock.order_cond.ShortSelling
            octype (str): the type or order to open new position or close position 
                - OrderProps.Future.octype.Auto
                - OrderProps.Future.octype.NewPosition
                - OrderProps.Future.octype.Cover
                - OrderProps.Future.octype.DayTrade
            account (:obj:Account): which account to place this order
        """
        BaseObj.__init__(
            self, *args, **{
                **kwargs,
                **dict(
                    action=action,
                    price_type=price_type,
                    order_type=order_type,
                    price=price,
                    quantity=quantity)
            })


class LimitOrder(Order):
    _force_def = dict(price_type=OrderProps.Future.price_type.LMT)

    def __init__(self,
                 action,
                 price,
                 quantity,
                 order_type=OrderProps.Future.order_type.ROD,
                 *args,
                 **kwargs):
        """ LimitOrder

        Args:
            product_id (str, optional): the code of product that order to placing 
                                        if not provide will gen from contract when placing order 
            action (srt): {B, S}, order action to buy or sell
                - B: buy
                - S: sell
            price (float or int): the price of order
            quantity (int): the quantity of order
            order_type (str, optional): {ROD, IOC, FOK}, the type of order
                - ROD: Rest of Day
                - IOC: Immediate-or-Cancel
                - FOK: Fill-or-Kill
            octype (str, optional): {' ', '0', '1', '6'}, the type or order 
                                    to open new position or close position 
                                    if not provide will become auto mode 
                - ' ': auto
                - '0': new position
                - '1': close position
                - '6': day trade
        """
        BaseObj.__init__(
            self, *args, **{
                **kwargs,
                **dict(
                    action=action,
                    order_type=order_type,
                    price=price,
                    quantity=quantity)
            })


class MarketOrder(Order):
    _force_def = dict(price_type=OrderProps.Future.price_type.MKT)

    def __init__(self,
                 action,
                 quantity,
                 order_type=OrderProps.Future.order_type.IOC,
                 *args,
                 **kwargs):
        """ MarketOrder

        Args:
            product_id (str, optional): the code of product that order to placing 
                                        if not provide will gen from contract when placing order 
            action (srt): {B, S}, order action to buy or sell
                - B: buy
                - S: sell
            quantity (int): the quantity of order
            order_type (str, optional): {IOC, FOK}, the type of order
                - IOC: Immediate-or-Cancel
                - FOK: Fill-or-Kill
            octype (str, optional): {' ', '0', '1', '6'}, the type or order 
                                    to open new position or close position 
                                    if not provide will become auto mode 
                - ' ': auto
                - '0': new position
                - '1': close position
                - '6': day trade
        """
        BaseObj.__init__(
            self, *args, **{
                **kwargs,
                **dict(action=action, order_type=order_type, quantity=quantity)
            })


class MarketRangeOrder(Order):
    _force_def = dict(price_type=OrderProps.Future.price_type.MKP)

    def __init__(self,
                 action,
                 quantity,
                 order_type=OrderProps.Future.order_type.IOC,
                 *args,
                 **kwargs):
        """ MarketRangeOrder

        Args:
            product_id (str, optional): the code of product that order to placing 
                                        if not provide will gen from contract when placing order 
            action (srt): {B, S}, order action to buy or sell
                - B: buy
                - S: sell
            quantity (int): the quantity of order
            order_type (str, optional): {IOC, FOK}, the type of order
                - IOC: Immediate-or-Cancel
                - FOK: Fill-or-Kill
            octype (str, optional): {' ', '0', '1', '6'}, the type or order 
                                    to open new position or close position 
                                    if not provide will become auto mode 
                - ' ': auto
                - '0': new position
                - '1': close position
                - '6': day trade
        """
        BaseObj.__init__(
            self, *args, **{
                **kwargs,
                **dict(action=action, order_type=order_type, quantity=quantity)
            })
