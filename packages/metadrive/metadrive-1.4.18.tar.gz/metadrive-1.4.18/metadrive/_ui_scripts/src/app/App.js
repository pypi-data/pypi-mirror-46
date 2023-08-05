import React, { PureComponent } from 'react';
import { connect } from 'react-redux';
import { Router, Route } from 'react-router-dom';
import createHistory from 'history/createBrowserHistory';
import { fetchDrivers, fetchDrives } from './actions';
import Dashboard from '../pages/dashboard/Dashboard';
import './css/App.css';

const history = createHistory();

class App extends PureComponent {
  constructor(props) {
    super(props);

    const {
      app: {
        api: { server }
      },
      fetchDrivers,
      fetchDrives
    } = props;
    if (server) {
      fetchDrivers();
      fetchDrives();
    }
  }

  render() {
    return (
      <Router history={history}>
        <Route exact path="/" component={Dashboard} />
      </Router>
    );
  }
}

const mapStateToProps = ({ app }) => ({
  app
});

const mapDispatchToProps = dispatch => ({
  fetchDrivers: () => dispatch(fetchDrivers()),
  fetchDrives: () => dispatch(fetchDrives())
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(App);
