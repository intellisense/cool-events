import _ from 'lodash';
import moment from 'moment';

export function removeNamespace(namespace, types) {
  // https://stackoverflow.com/a/47646215/860103
  return _.reduce(types, (typeObj, typeValue, typeName) => {
    typeObj[typeName] = _.reduce(typeValue, (obj, v, k) => {
      obj[k] = v.replace(namespace, '');
      return obj;
    }, {});
    return typeObj;
  }, {});
}

export function formatDateTime(value, format = 'MMMM Do YYYY, h:mm a') {
  return value ? moment(String(value)).format(format) : '';
}
