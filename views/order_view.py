#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
@CreateTime    : 2024/5/6 14:30
@Author  : 系统订单服务
@file for: 订单视图层，处理HTTP请求和响应
"""
import traceback
from typing import Dict, List, Optional, Union

from sanic import Blueprint, json
from sanic.request import Request
from sanic.response import HTTPResponse

from OrderManagement.services.OrderService import OrderService

# 创建蓝图
order_blueprint = Blueprint('order', url_prefix='/orders')

# 实例化服务类
order_service = OrderService()

@order_blueprint.route('/', methods=['POST'])
async def create_order(request: Request) -> HTTPResponse:
    """创建订单的API接口
    
    请求体应包含:
    {
        "user_id": 123,
        "total_amount": 99.9,
        "status": "pending",
        "items": [
            {"product_id": 1, "product_name": "商品A", "quantity": 2, "price": 49.95},
            {"product_id": 2, "product_name": "商品B", "quantity": 1, "price": 49.95}
        ]
    }
    
    Returns:
        JSON: 包含生成的订单号
    """
    try:
        # 获取请求数据
        order_data = request.json
        
        # 参数校验（这里使用简单的校验，实际应用中可以使用pydantic等库进行更复杂的校验）
        required_fields = ['user_id', 'total_amount', 'status', 'items']
        for field in required_fields:
            if field not in order_data:
                return json({"error": f"缺少必要字段：{field}"}, status=400)
        
        # 创建订单
        order_number = order_service.create_order(order_data)
        
        # 返回成功响应
        return json({"order_number": order_number}, status=201)
        
    except Exception as e:
        # 记录错误日志
        print(f"[ERROR]: 创建订单时发生异常: {str(e)}")
        # 返回错误响应
        return json({"error": str(e)}, status=500)

@order_blueprint.route('/', methods=['GET'])
async def get_orders(request: Request) -> HTTPResponse:
    """分页查询订单列表的API接口
    
    查询参数:
        page: 当前页码，默认为1
        page_size: 每页显示数量，默认为20
    
    Returns:
        JSON: 包含订单列表和总数的响应
    """
    try:
        # 解析查询参数
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 20))
        
        # 查询订单
        orders, total = order_service.get_orders(page, page_size)
        
        # 返回成功响应
        return json({
            "orders": orders,
            "total": total,
            "page": page,
            "page_size": page_size
        })
        
    except Exception as e:
        # 记录错误日志
        print(f"[ERROR]: 查询订单列表时发生异常: {str(e)}")
        # 返回错误响应
        return json({"error": str(e)}, status=500)

@order_blueprint.route('/<order_id:int>', methods=['GET'])
async def get_order_by_id(request: Request, order_id: int) -> HTTPResponse:
    """根据订单ID查询详情的API接口
    
    Args:
        order_id: URL中的订单ID参数
        
    Returns:
        JSON: 包含订单详细信息的响应
    """
    try:
        # 查询订单
        order = order_service.get_order_by_id(order_id)
        
        if order is None:
            return json({"error": "订单不存在"}, status=404)
        
        # 返回成功响应
        return json(order)
        
    except Exception as e:
        # 记录错误日志
        print(f"[ERROR]: 查询订单详情时发生异常: {str(e)}")
        # 返回错误响应
        return json({"error": str(e)}, status=500)
