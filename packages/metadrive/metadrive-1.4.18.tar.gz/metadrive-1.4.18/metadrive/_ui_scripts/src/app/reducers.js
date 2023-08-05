import { merge } from 'lodash';
import { Map } from 'immutable';
import {
  REQUEST_DRIVERS,
  REQUEST_DRIVER_DETAILS,
  REQUEST_DRIVES,
  RECEIVE_DRIVERS,
  RECEIVE_DRIVER_DETAILS,
  RECEIVE_DRIVES,
  ERROR_DRIVERS,
  ERROR_DRIVER_DETAILS,
  ERROR_DRIVES
} from './actions';

const initialState = {
  api: {
    server: process.env.REACT_APP_API_SERVER.replace(/\/$/, ''),
    drivers: {
      data: [],
      status: null
    },
    driversDetails: Map(),
    drives: {
      data: [],
      status: null
    }
  }
};

const initDriversDetails = (state, data = []) => {
  const initialValue = {};
  data.forEach(item => {
    const driver = item.id.slice(`${state.api.server}/driver/`.length);
    initialValue[driver] = {
      data: {},
      status: null
    };
  });
  return Map(initialValue);
};

const getSection = action => {
  switch (action.type) {
    case REQUEST_DRIVERS:
    case RECEIVE_DRIVERS:
    case ERROR_DRIVERS:
      return 'drivers';
    case REQUEST_DRIVES:
    case RECEIVE_DRIVES:
    case ERROR_DRIVES:
      return 'drives';
    default:
      return '';
  }
};

const getStatus = action => {
  switch (action.type) {
    case REQUEST_DRIVERS:
    case REQUEST_DRIVER_DETAILS:
    case REQUEST_DRIVES:
      return 'loading';
    case RECEIVE_DRIVERS:
    case RECEIVE_DRIVER_DETAILS:
    case RECEIVE_DRIVES:
      return 'success';
    case ERROR_DRIVERS:
    case ERROR_DRIVER_DETAILS:
    case ERROR_DRIVES:
      return 'error';
    default:
      return null;
  }
};

const getData = action => {
  switch (action.type) {
    case REQUEST_DRIVERS:
    case ERROR_DRIVERS:
    case REQUEST_DRIVES:
    case ERROR_DRIVES:
      return [];
    case RECEIVE_DRIVERS:
    case RECEIVE_DRIVER_DETAILS:
    case RECEIVE_DRIVES:
      return action.data;
    case REQUEST_DRIVER_DETAILS:
    case ERROR_DRIVER_DETAILS:
      return {};
    default:
      return null;
  }
};

const getDriversDetails = (state, action) => {
  switch (action.type) {
    case REQUEST_DRIVERS:
    case ERROR_DRIVERS:
    case REQUEST_DRIVES:
    case RECEIVE_DRIVES:
    case ERROR_DRIVES:
      return state.api.driversDetails;
    case RECEIVE_DRIVERS:
      return initDriversDetails(state, action.data);
    default:
      return null;
  }
};

const app = (state = initialState, action) => {
  switch (action.type) {
    case REQUEST_DRIVERS:
    case RECEIVE_DRIVERS:
    case ERROR_DRIVERS:
    case REQUEST_DRIVES:
    case RECEIVE_DRIVES:
    case ERROR_DRIVES:
      return merge({}, state, {
        api: {
          [getSection(action)]: {
            data: getData(action),
            status: getStatus(action)
          },
          driversDetails: getDriversDetails(state, action)
        }
      });
    case REQUEST_DRIVER_DETAILS:
    case RECEIVE_DRIVER_DETAILS:
    case ERROR_DRIVER_DETAILS:
      return merge({}, state, {
        api: {
          driversDetails: state.api.driversDetails.set(action.driver, {
            data: getData(action),
            status: getStatus(action)
          })
        }
      });
    default:
      return state;
  }
};

export default app;
