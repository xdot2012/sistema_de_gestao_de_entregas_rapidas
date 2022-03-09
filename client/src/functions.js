export const LATE_TIME = 10;
export const WARN_TIME = 5;

export function toDate(dateStr) {
  const parts = dateStr.split('-');
  return new Date(parts[2], parts[1] - 1, parts[0]);
}

export function dateTimeToDate(datetimeStr) {
  const dateStr = datetimeStr.slice(0, datetimeStr.indexOf('T'));
  const timeStr = datetimeStr.slice(datetimeStr.indexOf('T') + 1);

  const timeParts = timeStr.split(':');
  const parts = dateStr.split('-');
  return new Date(parts[2], parts[1] - 1, parts[0], timeParts[0], timeParts[1]);
}

export function getDifInMinutes(startDate, endDate) {
  return Math.round(Math.abs(startDate - endDate) / 60000);
}

export function isLate(dateTime) {
  return getDifInMinutes(Date.now(), dateTime) >= LATE_TIME;
}

export function isWarn(dateTime) {
  return getDifInMinutes(Date.now(), dateTime) >= WARN_TIME;
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
