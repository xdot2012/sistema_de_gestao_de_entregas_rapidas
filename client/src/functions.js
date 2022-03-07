export function toDate(dateStr) {
  const parts = dateStr.split('-');
  return new Date(parts[2], parts[1] - 1, parts[0]);
}

export function DatetimeToDate(datetimeStr) {
  const dateStr = datetimeStr.slice(0, datetimeStr.indexOf('T'));
  const timeStr = datetimeStr.slice(datetimeStr.indexOf('T') + 1);

  const timeParts = timeStr.split(':');
  const parts = dateStr.split('-');
  return new Date(parts[2], parts[1] - 1, parts[0], timeParts[0], timeParts[1]);
}
