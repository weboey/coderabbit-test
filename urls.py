#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
@CreateTime    : 2024/5/6 14:30
@Author  : 系统订单服务
@file for: 订单模块URL配置
"""

from OrderManagement.views.order_view import order_blueprint

order_url = {
    "/orders": order_blueprint,
}

# 模块URL配置说明:
# - "/orders": 对应订单相关的所有路由
#   包含以下API接口:
#   - POST /orders           创建订单
#   - GET  /orders           分页查询订单列表
#   - GET  /orders/<order_id> 查询单个订单详情
