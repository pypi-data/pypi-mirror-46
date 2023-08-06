#!/usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base

WingsBase = declarative_base()
SparrowBase = declarative_base()


def get_wings_base():
    from .backtest_account_asset import BacktestAccountAsset
    from .backtest_account import BacktestAccount
    from .market_withdraw_rules import MarketWithdrawRules
    return WingsBase


def get_sparrow_base():
    pass
