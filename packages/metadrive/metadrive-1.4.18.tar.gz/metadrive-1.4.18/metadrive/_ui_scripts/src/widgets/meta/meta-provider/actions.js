/*
 * action types
 */
export const SET_DATA = 'SET_DATA';

/*
 * action creators
 */
export const setData = (key, data) => ({
  type: SET_DATA,
  key,
  data
});
