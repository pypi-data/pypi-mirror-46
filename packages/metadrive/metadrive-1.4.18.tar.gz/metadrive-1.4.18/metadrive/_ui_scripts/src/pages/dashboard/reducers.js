import { UPDATE_WINDOWS } from './actions';

const initialState = null;

const dashboard = (state = initialState, action) => {
  switch (action.type) {
    case UPDATE_WINDOWS:
      return action.dashboard;

    default:
      return state;
  }
};

export default dashboard;
