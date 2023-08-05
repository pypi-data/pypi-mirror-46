import { combineReducers } from 'redux';
import app from './app/reducers';
import dashboard from './pages/dashboard/reducers';
import meta from './widgets/meta/meta-provider/reducers';

export default combineReducers({
  app,
  dashboard,
  meta
});
