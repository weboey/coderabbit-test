"""
@CreateTime    : 2024/5/6 14:30
@Author  : 系统订单服务
@file for: 订单业务逻辑层
"""
import traceback
import random
import time
from typing import Dict, List, Optional, Union

from logger_control import SharingProgramInfo, log_info
from OrderManagement.dao.OrderDao import OrderDao

# 假设的product_service，实际应导入真实的库存服务
class ProductService:
    """商品服务类，用于处理与商品相关的操作"""
    @staticmethod
    def check_and_decrease_stock(product_id: int, quantity: int) -> bool:
        """检查并扣减库存
        
        Args:
            product_id: 商品ID
            quantity: 需要扣减的数量
            
        Returns:
            bool: 库存是否足够且成功扣减
        """
        # 实际实现中应调用真正的库存服务
        # 这里仅做模拟实现
        SharingProgramInfo.info(f"[INFO]: 检查并扣减商品 {product_id} 的库存，数量：{quantity}")
        # 模拟成功扣减
        return True

product_service = ProductService()

class OrderService:
    """订单服务类，处理订单创建、查询等核心业务逻辑"""
    
    def __init__(self):
        self.order_dao = OrderDao()
        
    def create_order(self, order_data: Dict) -> str:
        """创建订单
        
        Args:
            order_data: 包含订单信息的字典，包含:
                - user_id: 用户ID
                - total_amount: 订单总金额
                - status: 订单状态
                - items: 订单商品列表，每个元素包含商品信息
        
        Returns:
            str: 生成的订单号
            
        Raises:
            Exception: 创建订单时发生异常
            ValueError: 参数校验失败
        """
        try:
            # 参数校验
            if not isinstance(order_data, dict):
                raise ValueError("订单数据必须为字典类型")
                
            required_fields = ['user_id', 'total_amount', 'status', 'items']
            for field in required_fields:
                if field not in order_data:
                    raise ValueError(f"缺少必要字段：{field}")
            
            if not isinstance(order_data['items'], list) or not order_data['items']:
                raise ValueError("订单商品列表不能为空")
            
            # 检查库存
            for item in order_data['items']:
                product_id = item.get('product_id')
                quantity = item.get('quantity')
                
                if not product_id or not quantity:
                    raise ValueError(f"商品信息不完整：{item}")
                
                if quantity <= 0:
                    raise ValueError(f"商品数量必须大于0：{item}")
                
                # 调用库存服务检查并扣减库存
                if not product_service.check_and_decrease_stock(product_id, quantity):
                    raise ValueError(f"商品 {product_id} 库存不足")
            
            # 创建订单
            return self.order_dao.create_order(order_data)
            
        except Exception as e:
            SharingProgramInfo.info(f"\n[ERROR]: 创建订单失败: {str(e)}")
            log_info.error(f"\n[ERROR]: 创建订单失败: {traceback.print_exc()}")
            raise e
            
    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        """根据订单ID查询订单详情
        
        Args:
            order_id: 订单ID
            
        Returns:
            dict: 订单详细信息，包含订单基本信息和所有订单项
        """
        try:
            return self.order_dao.get_order_by_id(order_id)
            
        except Exception as e:
            SharingProgramInfo.info(f"\n[ERROR]: 查询订单详情失败: {str(e)}")
            log_info.error(f"\n[ERROR]: 查询订单详情失败: {traceback.print_exc()}")
            raise e
            
    def get_orders(self, page: int = 1, page_size: int = 20) -> tuple:
        """分页查询订单列表
        
        Args:
            page: 当前页码，默认为1
            page_size: 每页显示数量，默认为20
            
        Returns:
            tuple: 包含两个元素的元组:
                - list: 当前页的订单列表
                - int: 总订单数量
        """
        try:
            return self.order_dao.get_orders(page, page_size)
            
        except Exception as e:
            SharingProgramInfo.info(f"\n[ERROR]: 查询订单列表失败: {str(e)}")
            log_info.error(f"\n[ERROR]: 查询订单列表失败: {traceback.print_exc()}")
            raise e
