"""
@CreateTime    : 2024/5/6 14:30
@Author  : 系统订单服务
@file for: 订单数据访问层
"""
import traceback
from psycopg2 import sql
from psycopg2.extras import execute_values

from logger_control import SharingProgramInfo, log_info
from middleware.pgBaseDao import PgBaseDao

class OrderDao(PgBaseDao):
    """订单数据访问类，封装与订单相关的数据库操作"""

    def __init__(self):
        PgBaseDao.__init__(self)

    def create_order(self, order_data):
        """创建订单并返回生成的订单号
        
        Args:
            order_data: 包含订单信息的字典，包含:
                - user_id: 用户ID
                - total_amount: 订单总金额
                - status: 订单状态
                - items: 订单商品列表，每个元素包含商品信息
        
        Returns:
            str: 生成的订单号
        """
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            cur = self.get_cursor(conn)
            
            # 开始事务
            conn.autocommit = False
            
            # 首先插入订单主表
            master_sql = sql.SQL("""
                INSERT INTO orders (
                    user_id, 
                    total_amount,
                    status,
                    order_number,
                    created_at
                ) VALUES (%s, %s, %s, %s, NOW()) RETURNING order_id
            """)
            
            # 生成订单号（实际应用中应使用更复杂的规则）
            order_number = f"ON{int(time.time())}{random.randint(1000, 9999)}"
            
            cur.execute(
                master_sql,
                [
                    order_data['user_id'], 
                    order_data['total_amount'],
                    order_data['status'],
                    order_number
                ]
            )
            
            # 获取自动生成的订单ID
            order_id = cur.fetchone()[0]
            
            # 插入订单明细
            if 'items' in order_data and order_data['items']:
                item_sql = sql.SQL("""
                    INSERT INTO order_items (
                        order_id,
                        product_id,
                        product_name,
                        quantity,
                        price,
                        subtotal
                    ) VALUES (%s, %s, %s, %s, %s, %s)
                """)
                
                item_values = [
                    (
                        order_id,
                        item['product_id'],
                        item['product_name'],
                        item['quantity'],
                        item['price'],
                        item['quantity'] * item['price']
                    ) for item in order_data['items']
                ]
                
                execute_values(cur, item_sql, item_values)
            
            # 提交事务
            conn.commit()
            
            return order_number
            
        except Exception as e:
            if conn:
                conn.rollback()
            log_info.error(f"\n[ERROR]: 创建订单失败: {traceback.print_exc()}")
            log_info.error(f"\n {str(e)}")
            raise e
            
        finally:
            self.put_connect(conn, cur)
            
    def get_order_by_id(self, order_id):
        """根据订单ID查询订单详情
        
        Args:
            order_id: 订单ID
            
        Returns:
            dict: 订单详细信息，包含订单基本信息和所有订单项
        """
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            cur = self.get_cursor(conn)
            
            sql = sql.SQL("""
                SELECT 
                    o.*,
                    i.order_item_id,
                    i.product_id,
                    i.product_name,
                    i.quantity,
                    i.price,
                    i.subtotal
                FROM orders o
                LEFT JOIN order_items i ON o.order_id = i.order_id
                WHERE o.order_id = %s
                ORDER BY i.order_item_id
            """)
            
            cur.execute(sql, [order_id])
            results = cur.fetchall()
            
            if not results:
                return None
            
            # 转换为字典格式
            keys = [col[0] for col in cur.description]
            data_list = []
            for item in results:
                data_dict = dict()
                for i, key in enumerate(keys):
                    new_key = str(key).upper()
                    data_dict[new_key] = item[i]
                data_list.append(data_dict)
            
            # 将结果拆分为主表和子表
            main_order = {k: v for k, v in data_list[0].items() if not k.startswith('ORDER_ITEM_ID')}
            items = [{k: v for k, v in data.items() if k in [
                'ORDER_ITEM_ID', 'PRODUCT_ID', 'PRODUCT_NAME',
                'QUANTITY', 'PRICE', 'SUBTOTAL'
            ]} for data in data_list]
            
            main_order['ITEMS'] = items
            
            return main_order
            
        except Exception as e:
            log_info.error(f"\n[ERROR]: 查询订单详情失败: {traceback.print_exc()}")
            log_info.error(f"\n {str(e)}")
            raise e
            
        finally:
            self.put_connect(conn, cur)
            
    def get_orders(self, page=1, page_size=20):
        """分页查询订单列表
        
        Args:
            page: 当前页码，默认为1
            page_size: 每页显示数量，默认为20
            
        Returns:
            tuple: 包含两个元素的元组:
                - list: 当前页的订单列表
                - int: 总订单数量
        """
        conn = None
        cur = None
        try:
            conn = self.get_connection()
            cur = self.get_cursor(conn)
            
            offset = (page - 1) * page_size
            
            # 使用CTE进行分页查询
            sql = sql.SQL("""
                WITH ordered_orders AS (
                    SELECT order_id
                    FROM orders
                    ORDER BY created_at DESC
                    LIMIT %s
                    OFFSET %s
                )
                SELECT 
                    o.*,
                    i.order_item_id,
                    i.product_id,
                    i.product_name,
                    i.quantity,
                    i.price,
                    i.subtotal
                FROM ordered_orders oo
                JOIN orders o ON oo.order_id = o.order_id
                LEFT JOIN order_items i ON o.order_id = i.order_id
                ORDER BY o.created_at DESC, i.order_item_id
            """)
            
            cur.execute(sql, [page_size, offset])
            results = cur.fetchall()
            
            # 转换为字典格式
            keys = [col[0] for col in cur.description]
            data_list = []
            for item in results:
                data_dict = dict()
                for i, key in enumerate(keys):
                    new_key = str(key).upper()
                    data_dict[new_key] = item[i]
                data_list.append(data_dict)
            
            # 处理结果集，按订单ID分组
            orders_map = {}
            for data in data_list:
                order_id = data['ORDER_ID']
                if order_id not in orders_map:
                    orders_map[order_id] = {
                        'MAIN': {},
                        'ITEMS': []
                    }
                
                # 区分主表和明细项字段
                for k, v in data.items():
                    if k.startswith('ORDER_ITEM_ID'):
                        if v is not None:
                            item = {k: v for k, v in data.items() if k in [
                                'ORDER_ITEM_ID', 'PRODUCT_ID', 'PRODUCT_NAME',
                                'QUANTITY', 'PRICE', 'SUBTOTAL'
                            ]}
                            if item not in orders_map[order_id]['ITEMS']:
                                orders_map[order_id]['ITEMS'].append(item)
                    else:
                        if k not in orders_map[order_id]['MAIN']:
                            orders_map[order_id]['MAIN'][k] = v
            
            # 获取总数
            count_sql = "SELECT COUNT(*) FROM orders"
            cur.execute(count_sql)
            total = cur.fetchone()[0]
            
            return list(orders_map.values()), total
            
        except Exception as e:
            log_info.error(f"\n[ERROR]: 查询订单列表失败: {traceback.print_exc()}")
            log_info.error(f"\n {str(e)}")
            raise e
            
        finally:
            self.put_connect(conn, cur)
