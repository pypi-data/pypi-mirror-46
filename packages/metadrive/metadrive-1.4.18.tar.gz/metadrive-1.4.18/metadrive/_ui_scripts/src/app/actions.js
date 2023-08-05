/*
 * action types
 */
export const REQUEST_DRIVERS = 'REQUEST_DRIVERS';
export const REQUEST_DRIVER_DETAILS = 'REQUEST_DRIVER_DETAILS';
export const REQUEST_DRIVES = 'REQUEST_DRIVES';
export const RECEIVE_DRIVERS = 'RECEIVE_DRIVERS';
export const RECEIVE_DRIVER_DETAILS = 'RECEIVE_DRIVER_DETAILS';
export const RECEIVE_DRIVES = 'RECEIVE_DRIVES';
export const ERROR_DRIVERS = 'ERROR_DRIVERS';
export const ERROR_DRIVER_DETAILS = 'ERROR_DRIVER_DETAILS';
export const ERROR_DRIVES = 'ERROR_DRIVES';

/*
 * action creators
 */
export const requestDrivers = () => ({
  type: REQUEST_DRIVERS
});

export const requestDriverDetails = driver => ({
  type: REQUEST_DRIVER_DETAILS,
  driver
});

export const requestDrives = () => ({
  type: REQUEST_DRIVES
});

export const receiveDrivers = data => ({
  type: RECEIVE_DRIVERS,
  data
});

export const receiveDriverDetails = (driver, data) => ({
  type: RECEIVE_DRIVER_DETAILS,
  driver,
  data
});

export const receiveDrives = data => ({
  type: RECEIVE_DRIVES,
  data
});

export const errorDrivers = () => ({
  type: ERROR_DRIVERS
});

export const errorDriverDetails = driver => ({
  type: ERROR_DRIVER_DETAILS,
  driver
});

export const errorDrives = () => ({
  type: ERROR_DRIVES
});

export function fetchDrivers() {
  return (dispatch, getState) => {
    dispatch(requestDrivers());
    const {
      app: {
        api: { server }
      }
    } = getState();

    return fetch(`${server}/drivers`)
      .then(response => response.json())
      .then(data => {
        dispatch(receiveDrivers(data));
        dispatch(fetchDriversDetails());
      })
      .catch(error => dispatch(errorDrivers()));
  };
}

export function fetchDriversDetails() {
  return (dispatch, getState) => {
    const {
      app: {
        api: { server, drivers }
      }
    } = getState();
    if (drivers.status === 'success') {
      return Promise.all(
        drivers.data.map(item => {
          const driver = item.id.slice(`${server}/driver/`.length);
          dispatch(requestDriverDetails(driver));
          return fetch(item.id)
            .then(response => response.json())
            .then(data => dispatch(receiveDriverDetails(driver, data)))
            .catch(() => dispatch(errorDriverDetails(driver)));
        })
      );
    }
    return Promise.resolve();
  };
}

export function fetchDrives() {
  return (dispatch, getState) => {
    dispatch(requestDrives());
    const {
      app: {
        api: { server }
      }
    } = getState();

    return fetch(`${server}/drives`)
      .then(response => response.json())
      .then(data => dispatch(receiveDrives(data)))
      .catch(() => dispatch(errorDrives()));
  };
}
