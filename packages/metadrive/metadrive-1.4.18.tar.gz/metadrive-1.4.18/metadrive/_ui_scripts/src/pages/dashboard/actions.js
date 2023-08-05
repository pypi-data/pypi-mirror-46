/*
 * action types
 */
export const UPDATE_WINDOWS = 'UPDATE_WINDOWS';

/*
 * action creators
 */
export const updateWindows = dashboard => ({
  type: UPDATE_WINDOWS,
  dashboard
});
