from src.models.market import BookTicker, DepthUpdate, Kline, OrderBook, Trade


def test_kline_from_list_parses_numeric_fields():
    kline = Kline.from_list(
        [
            1499040000000,
            "0.01634790",
            "0.80000000",
            "0.01575800",
            "0.01577100",
            "148976.11427815",
            1499644799999,
            "2434.19055334",
            308,
            "1756.87402397",
            "28.46694368",
            "0",
        ]
    )

    assert kline.close == 0.015771
    assert kline.number_of_trades == 308


def test_trade_from_websocket_payload_maps_aliases():
    trade = Trade.from_stream_payload(
        {
            "e": "trade",
            "E": 123456789,
            "s": "BNBBTC",
            "t": 12345,
            "p": "0.001",
            "q": "100",
            "T": 123456785,
            "m": True,
            "M": True,
        }
    )

    assert trade.symbol == "BNBBTC"
    assert trade.price == 0.001
    assert trade.qty == 100.0
    assert trade.id == 12345


def test_book_ticker_from_stream_payload_maps_numeric_fields():
    ticker = BookTicker.from_stream_payload(
        {
            "u": 400900217,
            "s": "BNBUSDT",
            "b": "25.35190000",
            "B": "31.21000000",
            "a": "25.36520000",
            "A": "40.66000000",
        }
    )

    assert ticker.symbol == "BNBUSDT"
    assert ticker.bid_price == 25.3519
    assert ticker.ask_qty == 40.66


def test_depth_update_from_stream_payload_parses_bids_and_asks():
    update = DepthUpdate.from_stream_payload(
        {
            "e": "depthUpdate",
            "E": 1672515782136,
            "s": "BNBBTC",
            "U": 157,
            "u": 160,
            "b": [["0.0024", "10"]],
            "a": [["0.0026", "100"]],
        }
    )

    assert update.symbol == "BNBBTC"
    assert update.first_update_id == 157
    assert update.bids[0] == (0.0024, 10.0)
    assert update.asks[0] == (0.0026, 100.0)


def test_order_book_normalizes_rest_levels():
    order_book = OrderBook(**{
        "lastUpdateId": 1027024,
        "bids": [["4.00000000", "431.00000000"]],
        "asks": [["4.00000200", "12.00000000"]],
    })

    assert order_book.bids[0] == (4.0, 431.0)
    assert order_book.asks[0] == (4.000002, 12.0)
