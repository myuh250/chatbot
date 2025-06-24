import React, { useState, useEffect } from 'react';
import { Users, Package, Clock, TrendingUp, Download, Search, Filter } from 'lucide-react';
import './admin.css';

const API_BASE_URL = 'http://localhost:8000';

const Admin = () => {
  const [customerData, setCustomerData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [sortBy, setSortBy] = useState('date');

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/chatbot/orders-final`);
        const data = await res.json();

        const mapped = data.map((order, idx) => {
          const orderType = order.danh_sach_banh && order.danh_sach_banh.length > 0
            ? order.danh_sach_banh.map(b => b.ten_banh).join(', ')
            : '';
          const quantity = order.danh_sach_banh && order.danh_sach_banh.length > 0
            ? order.danh_sach_banh.reduce((sum, b) => sum + (b.so_luong || 0), 0)
            : 0;

          return {
            id: order.id || idx + 1,
            customerName: order.ten_khach_hang || '',
            phone: order.so_dien_thoai || '',
            orderType: orderType,
            quantity: quantity,
            price: order.tong_tien || 0, 
            gio_giao: order.gio_giao || '', 
            address: order.dia_chi || '',
            status: order.status || 'pending', 
            notes: order.ghi_chu || '',
            danh_sach_banh: order.danh_sach_banh || []
          };
        });

        setCustomerData(mapped);
      } catch (err) {
        setCustomerData([]);
      }
    };

    fetchOrders();
  }, []);

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'status-pending';
      case 'confirmed': return 'status-confirmed';
      case 'completed': return 'status-completed';
      default: return 'status-pending';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'pending': return 'Chờ xác nhận';
      case 'confirmed': return 'Đã xác nhận';
      case 'completed': return 'Hoàn thành';
      default: return 'Chờ xác nhận';
    }
  };

  const filteredData = customerData.filter(item => {
    const matchesSearch = item.customerName.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.phone.includes(searchTerm) ||
                         item.orderType.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filterStatus === 'all' || item.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  const sortedData = [...filteredData].sort((a, b) => {
    switch (sortBy) {
      case 'date':
        return new Date(b.timestamp) - new Date(a.timestamp);
      case 'price':
        return b.price - a.price;
      case 'name':
        return a.customerName.localeCompare(b.customerName);
      default:
        return 0;
    }
  });

  const totalRevenue = customerData.reduce((sum, item) => sum + item.price, 0);
  const completedOrders = customerData.filter(item => item.status === 'completed').length;
  const pendingOrders = customerData.filter(item => item.status === 'pending').length;

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(amount);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('vi-VN');
  };

  const exportToCSV = () => {
    const headers = ['Tên khách hàng', 'Số điện thoại', 'Loại bánh', 'Số lượng', 'Giá', 'Giờ giao', 'Địa chỉ', 'Trạng thái', 'Ghi chú'];
    const csvContent = [
      headers.join(','),
      ...sortedData.map(row => [
        row.customerName,
        row.phone,
        row.orderType,
        row.quantity,
        row.price,
        row.gio_giao,
        `"${row.address}"`,
        getStatusText(row.status),
        `"${row.notes}"`
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'bakery_orders.csv';
    link.click();
  };

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>Thống Kê & Quản Lý Đơn Hàng</h1>
        <p>Thông tin đơn hàng được trích xuất từ chatbot</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <Package />
          </div>
          <div className="stat-content">
            <h3>{customerData.length}</h3>
            <p>Tổng đơn hàng</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <TrendingUp />
          </div>
          <div className="stat-content">
            <h3>{formatCurrency(totalRevenue)}</h3>
            <p>Tổng doanh thu</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Clock />
          </div>
          <div className="stat-content">
            <h3>{pendingOrders}</h3>
            <p>Đơn chờ xử lý</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <Users />
          </div>
          <div className="stat-content">
            <h3>{completedOrders}</h3>
            <p>Đơn hoàn thành</p>
          </div>
        </div>
      </div>

      <div className="table-controls">
        <div className="search-filter-group">
          <div className="search-box">
            <Search size={20} />
            <input
              type="text"
              placeholder="Tìm kiếm theo tên, SĐT, loại bánh..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>

          <div className="filter-group">
            <Filter size={20} />
            <select
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
            >
              <option value="all">Tất cả trạng thái</option>
              <option value="pending">Chờ xác nhận</option>
              <option value="confirmed">Đã xác nhận</option>
              <option value="completed">Hoàn thành</option>
            </select>
          </div>

          <div className="sort-group">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="date">Sắp xếp theo thời gian</option>
              <option value="price">Sắp xếp theo giá</option>
              <option value="name">Sắp xếp theo tên</option>
            </select>
          </div>
        </div>

        <button className="export-btn" onClick={exportToCSV}>
          <Download size={20} />
          <span>Xuất CSV</span>
        </button>
      </div>

      <div className="data-table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>STT</th>
              <th>Khách hàng</th>
              <th>Số điện thoại</th>
              <th>Loại bánh</th>
              <th>Số lượng</th>
              <th>Giá tiền</th>
              <th>Giờ giao</th>
              <th>Địa chỉ</th>
              <th>Trạng thái</th>
              <th>Ghi chú</th>
            </tr>
          </thead>
          <tbody>
            {sortedData.length === 0 && (
              <tr>
                <td colSpan={10} className="no-data">
                  Không tìm thấy dữ liệu phù hợp
                </td>
              </tr>
            )}
            {sortedData.map((row, index) => (
              row.danh_sach_banh && row.danh_sach_banh.length > 0
                ? row.danh_sach_banh.map((b, i) => (
                    <tr key={`${row.id}-${i}`}>
                      {i === 0 ? (
                        <>
                          <td rowSpan={row.danh_sach_banh.length}>{index + 1}</td>
                          <td rowSpan={row.danh_sach_banh.length} className="customer-name">{row.customerName}</td>
                          <td rowSpan={row.danh_sach_banh.length}>{row.phone}</td>
                        </>
                      ) : null}
                      <td className="order-type">{b.ten_banh}</td>
                      <td>{b.so_luong}</td>
                      {i === 0 ? (
                        <>
                          <td rowSpan={row.danh_sach_banh.length} className="price">{formatCurrency(row.price)}</td>
                          <td rowSpan={row.danh_sach_banh.length}>{row.gio_giao}</td>
                          <td rowSpan={row.danh_sach_banh.length} className="address">{row.address}</td>
                          <td rowSpan={row.danh_sach_banh.length}>
                            <span className={`status ${getStatusColor(row.status)}`}>
                              {getStatusText(row.status)}
                            </span>
                          </td>
                          <td rowSpan={row.danh_sach_banh.length} className="notes">{row.notes}</td>
                        </>
                      ) : null}
                    </tr>
                  ))
                : (
                  <tr key={row.id}>
                    <td>{index + 1}</td>
                    <td className="customer-name">{row.customerName}</td>
                    <td>{row.phone}</td>
                    <td className="order-type">{row.orderType}</td>
                    <td>{row.quantity}</td>
                    <td className="price">{formatCurrency(row.price)}</td>
                    <td>{row.gio_giao}</td>
                    <td className="address">{row.address}</td>
                    <td>
                      <span className={`status ${getStatusColor(row.status)}`}>
                        {getStatusText(row.status)}
                      </span>
                    </td>
                    <td className="notes">{row.notes}</td>
                  </tr>
                )
            ))}
          </tbody>
        </table>
      </div>

      {sortedData.length === 0 && (
        <div className="no-data">
          <p>Không tìm thấy dữ liệu phù hợp</p>
        </div>
      )}
    </div>
  );
};

export default Admin;