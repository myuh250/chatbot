import React, { useState, useEffect } from 'react';
import { Users, Package, Clock, TrendingUp, Download, Search, Filter } from 'lucide-react';
import './admin.css';

const Admin = () => {
  const [customerData, setCustomerData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');
  const [sortBy, setSortBy] = useState('date');

  // Sample data - thay thế bằng data thật từ API
  useEffect(() => {
    const sampleData = [
      {
        id: 1,
        customerName: 'Nguyễn Văn A',
        phone: '0123456789',
        orderType: 'Bánh sinh nhật',
        quantity: 1,
        price: 350000,
        deliveryDate: '2024-01-15',
        address: '123 Đường ABC, Quận 1, TP.HCM',
        status: 'pending',
        timestamp: '2024-01-10 14:30:00',
        notes: 'Bánh kem vani, viết chữ "Happy Birthday"'
      },
      {
        id: 2,
        customerName: 'Trần Thị B',
        phone: '0987654321',
        orderType: 'Bánh kem',
        quantity: 2,
        price: 200000,
        deliveryDate: '2024-01-16',
        address: '456 Đường XYZ, Quận 3, TP.HCM',
        status: 'confirmed',
        timestamp: '2024-01-10 15:45:00',
        notes: 'Bánh kem chocolate, size nhỏ'
      },
      {
        id: 3,
        customerName: 'Lê Văn C',
        phone: '0369258147',
        orderType: 'Bánh mì',
        quantity: 10,
        price: 150000,
        deliveryDate: '2024-01-14',
        address: '789 Đường MNO, Quận 5, TP.HCM',
        status: 'completed',
        timestamp: '2024-01-09 09:15:00',
        notes: 'Bánh mì thịt nướng, giao sáng sớm'
      },
      {
        id: 4,
        customerName: 'Phạm Thị D',
        phone: '0741852963',
        orderType: 'Bánh cưới',
        quantity: 1,
        price: 2500000,
        deliveryDate: '2024-01-20',
        address: '321 Đường PQR, Quận 7, TP.HCM',
        status: 'pending',
        timestamp: '2024-01-11 11:20:00',
        notes: 'Bánh cưới 3 tầng, theme màu hồng'
      },
      {
        id: 5,
        customerName: 'Hoàng Văn E',
        phone: '0852741963',
        orderType: 'Bánh ngọt',
        quantity: 20,
        price: 800000,
        deliveryDate: '2024-01-17',
        address: '654 Đường STU, Quận 10, TP.HCM',
        status: 'confirmed',
        timestamp: '2024-01-11 16:30:00',
        notes: 'Mix bánh ngọt cho tiệc công ty'
      }
    ];
    setCustomerData(sampleData);
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
    const headers = ['Tên khách hàng', 'Số điện thoại', 'Loại bánh', 'Số lượng', 'Giá', 'Ngày giao', 'Địa chỉ', 'Trạng thái', 'Ghi chú'];
    const csvContent = [
      headers.join(','),
      ...sortedData.map(row => [
        row.customerName,
        row.phone,
        row.orderType,
        row.quantity,
        row.price,
        row.deliveryDate,
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
              <th>Ngày giao</th>
              <th>Địa chỉ</th>
              <th>Trạng thái</th>
              <th>Ghi chú</th>
            </tr>
          </thead>
          <tbody>
            {sortedData.map((row, index) => (
              <tr key={row.id}>
                <td>{index + 1}</td>
                <td className="customer-name">{row.customerName}</td>
                <td>{row.phone}</td>
                <td className="order-type">{row.orderType}</td>
                <td>{row.quantity}</td>
                <td className="price">{formatCurrency(row.price)}</td>
                <td>{formatDate(row.deliveryDate)}</td>
                <td className="address">{row.address}</td>
                <td>
                  <span className={`status ${getStatusColor(row.status)}`}>
                    {getStatusText(row.status)}
                  </span>
                </td>
                <td className="notes">{row.notes}</td>
              </tr>
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
