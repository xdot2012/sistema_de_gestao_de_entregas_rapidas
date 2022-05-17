import print from 'print-js';

export const LATE_TIME = 10;
export const WARN_TIME = 5;

export function toDate(dateStr) {
  const parts = dateStr.split('-');
  return new Date(parts[2], parts[1] - 1, parts[0]);
}

export function stringToDate(datetimeStr) {
  const dateStr = datetimeStr.slice(0, datetimeStr.indexOf('T'));
  const timeStr = datetimeStr.slice(datetimeStr.indexOf('T') + 1);

  const timeParts = timeStr.split(':');
  const parts = dateStr.split('-');
  return new Date(parts[2], parts[1] - 1, parts[0], timeParts[0], timeParts[1]);
}

export function getDifInMinutes(startDate, endDate) {
  return Math.round(Math.abs(endDate - startDate) / 60000);
}

export function calendarDate(datetimeStr) {
  const dateStr = datetimeStr.slice(0, datetimeStr.indexOf('T'));

  const parts = dateStr.split('-');
  return `${parts[2]}-${parts[1]}-${parts[0]}`;
}

export function isOut(item) {
  return item.ready_on != null;
}

export function isLate(dateTime) {
  return getDifInMinutes(dateTime, Date.now()) >= LATE_TIME;
}

export function isWarn(dateTime) {
  return getDifInMinutes(dateTime, Date.now()) >= WARN_TIME;
}

export function getOrderStatus(dateTime) {
  let response = 'UNDEFINED';
  if (isLate(dateTime)) {
    response = 'LATE';
  } else if (isWarn(dateTime)) {
    response = 'WARN';
  }
  return response;
}

export function getTotalProducts(orderList) {
  let total = 0;
  for (let i = 0; i < orderList.length; i += 1) {
    total += orderList[i].quantity;
  }
  return total;
}

export function getPriority(order) {
  const priorityData = {
    waiting_time: getDifInMinutes(stringToDate(order.created_on), Date.now()),
    quantity: getTotalProducts(order.products),
    selected: false,
  };
  return Object.assign(order, priorityData);
}

export function sortOrdersByTime(a, b) {
  if (a.waiting_time < b.waiting_time) {
    return 1;
  }
  if (a.waiting_time > b.waiting_time) {
    return -1;
  }
  return 0;
}

export function sortOrdersByDistance(a, b) {
  if (a.address.distance < b.address.distance) {
    return -1;
  }
  if (a.address.distance > b.address.distance) {
    return 1;
  }
  return 0;
}

export function formatAddress(obj) {
  let address = `Rua ${obj.street} nº${obj.number}, Bairro ${obj.district} - ${obj.city_name}/${obj.state_name}.CEP: ${obj.code};\n`;
  if (obj.reference) {
    address += `Referência: ${obj.reference}`;
  }
  return address;
}

export function formatAddressNominatin(obj) {
  return `Rua ${obj.street}, ${obj.city_name}, ${obj.state_name}, ${obj.code}`;
}

export function formatPhone(phone) {
  return phone.replace(' ', '').replace('(', '').replace(')', '').replace('-', '');
}

export function printJSONRoute(data, headers) {
  print({
    printable: data,
    type: 'json',
    properties: headers,
  });
}
