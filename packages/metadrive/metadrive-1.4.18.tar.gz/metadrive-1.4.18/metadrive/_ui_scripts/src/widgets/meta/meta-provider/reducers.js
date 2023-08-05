import { Map } from 'immutable';
import { SET_DATA } from './actions';

const initialState = {
  data: Map()
};

const meta = (state = initialState, action) => {
  switch (action.type) {
    case SET_DATA:
      return {
        data: state.data.set(action.key, {
          ...state.data.get(action.key),
          ...action.data
        })
      };

    default:
      return state;
  }
};

export default meta;
