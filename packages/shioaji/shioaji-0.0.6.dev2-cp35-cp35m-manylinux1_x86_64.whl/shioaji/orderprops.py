class MetaProps(type):
    def __repr__(cls):
        attrs = [attr for attr in cls.__dict__ if not attr.startswith('_')]
        display_name = cls.__name__ if not cls.__name__.startswith('_') else ""
        return '{}({})'.format(display_name, (', ').join(attrs))

class BaseProps(metaclass=MetaProps):
    pass

class _action(BaseProps):
    Buy = 'Buy'
    Sell = 'Sell'
    Update_Qty = 'UpdateQty'
    Update_Price = 'UpdatePrice'
    Cancel = 'Cancel'


class _stock_price_type(BaseProps):
    LimitPrice = 'LMT'
    Close = 'Close'
    LimitUp = 'LimitUp'
    LimitDown = 'LimitDown'


class _stock_order_type(BaseProps):
    Common = 'Common'  # 整股
    BlockTrade = 'BlockTrade' #鉅額
    Fixing = 'Fixing'  # 定盤
    Odd = 'Odd'  # 零股

class _stock_order_cond(BaseProps):
    Cash = 'Cash' # 現股
    Netting = 'Netting' # 餘額交割
    MarginTrading = 'MarginTrading' # 融資
    ShortSelling = 'ShortSelling' # 融券


class _stock_first_sell(BaseProps):
    Yes = 'true'
    No = 'false'


class _StockOrderProps(BaseProps):
    action = _action
    price_type = _stock_price_type
    order_type = _stock_order_type
    order_cond = _stock_order_cond
    first_sell = _stock_first_sell


class _future_price_type(BaseProps):
    LMT = 'LMT'
    MKT = 'MKT'
    MKP = 'MKP'


class _future_order_type(BaseProps):
    ROD = 'ROD'
    IOC = 'IOC'
    FOK = 'FOK'


class _future_octype(BaseProps):
    Auto = 'Auto'
    NewPosition = 'New'
    Cover = 'Cover'
    DayTrade = 'DayTrade'


class _future_callput(BaseProps):
    Call = 'Call'
    Put = 'Put'


class _FutureOrderPorps(BaseProps):
    action = _action
    price_type = _future_price_type
    order_type = _future_order_type
    octype = _future_octype
    callput = _future_callput
    octype = _future_octype


class OrderProps(BaseProps):
    Stock = _StockOrderProps
    Future = _FutureOrderPorps
