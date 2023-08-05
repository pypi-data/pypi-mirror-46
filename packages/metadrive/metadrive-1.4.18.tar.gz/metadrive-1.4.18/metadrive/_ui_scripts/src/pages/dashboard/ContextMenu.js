import React, { PureComponent, Fragment } from 'react';
import { connect } from 'react-redux';
import {
  Menu,
  MenuItem,
  Separator,
  Submenu,
  MenuFilter
} from 'react-ultimate-contextmenu';
import { Map } from 'immutable';
import classNames from 'classnames';
import { Spinner, Icon } from '@blueprintjs/core';
import { updateWindows } from './actions';
import { metaWidgets } from '../../widgets/meta';
import { staticWidgets } from '../../widgets/static';
import { widgetIsOpened, openWidget } from './utils';
import { SEP } from '../../constants/common';
import './css/contextmenu.css';

const staticWidgetsKeys = Object.keys(staticWidgets);

class ContextMenu extends PureComponent {
  static getDerivedStateFromProps(props, state) {
    if (!state.isDrivesInitialized) {
      const {
        app: {
          api: { server, drivers, drives }
        }
      } = props;
      if (drivers.status === 'success' && drives.status === 'success') {
        let { driverDrives } = state;

        drivers.data.forEach(({ id }) => {
          const driver = id.slice(`${server}/driver/`.length);
          const [, drive] = drives.data.find(([, drive, status]) =>
            drive.startsWith(`${driver}:`)
          ) || [null, `${driver}:default`, null];

          driverDrives = driverDrives.set(driver, drive);
        });

        return {
          driverDrives,
          isDrivesInitialized: true
        };
      }
    }
    return null;
  }

  handlerSelectWidget = widget => {
    if (!widgetIsOpened(widget, this.props.dashboard)) {
      this.props.updateWindows(openWidget(widget, this.props.dashboard));
    }
  };

  handlerChangeDrive = (driver, drive) => {
    this.setState(state => ({
      driverDrives: state.driverDrives.set(driver, drive)
    }));
  };

  renderDriversMenu = () => {
    const {
      app: {
        api: { drivers, driversDetails }
      }
    } = this.props;
    if (drivers.status === 'success') {
      return (
        <Fragment>
          {driversDetails
            .toArray()
            .map(([driver]) => this.renderDriverSubmenu(driver))}
          {staticWidgetsKeys.length > 0 && <Separator />}
        </Fragment>
      );
    } else if (drivers.status === 'error') {
      return (
        <Fragment>
          {this.renderMenuError(
            'An error has occurred when drivers are loaded'
          )}
          {staticWidgetsKeys.length > 0 && <Separator />}
        </Fragment>
      );
    } else if (drivers.status === 'loading') {
      return (
        <Fragment>
          {this.renderMenuLoader()}
          {staticWidgetsKeys.length > 0 && <Separator />}
        </Fragment>
      );
    }
  };

  renderMenuError = error => <div className="contextmenu_error">{error}</div>;

  renderMenuLoader = () => (
    <div className="contextmenu_loading">
      <Spinner size={Spinner.SIZE_SMALL} />
    </div>
  );

  renderDriverSubmenu = driver => {
    return (
      <Submenu key={driver} label={driver}>
        <div className="contextmenu_subtitle">Drives</div>
        {this.renderDriverDrives(driver)}
        <div className="contextmenu_subtitle">Types</div>
        {this.renderDriverTypes(driver)}
      </Submenu>
    );
  };

  renderDriverDrives = driver => {
    const {
      app: {
        api: { drives }
      }
    } = this.props;

    if (drives.status === 'success') {
      const driverDrives = drives.data.filter(([, drive]) =>
        drive.startsWith(`${driver}:`)
      );
      if (driverDrives.length > 0) {
        const checkedDrive = this.state.driverDrives.get(driver);

        return (
          <ul className="drives">
            {driverDrives.map(([, drive, status]) => (
              <li key={drive} className="drives_item">
                <label
                  className={classNames('drive', {
                    'drive--dead': status === 'DEAD'
                  })}
                >
                  <div className="drive_radio">
                    <input
                      type="radio"
                      name={`${driver}:drive`}
                      value={drive}
                      checked={drive === checkedDrive}
                      onChange={() => this.handlerChangeDrive(driver, drive)}
                    />
                  </div>
                  <div className="drive_id">{drive}</div>
                  <div className="drive_status">{status}</div>
                </label>
              </li>
            ))}
          </ul>
        );
      }
      return this.renderMenuError('No available drives');
    } else if (drives.status === 'error') {
      return this.renderMenuError(
        'An error has occurred when drives are loaded'
      );
    } else if (drives.status === 'loading') {
      return this.renderMenuLoader();
    }
  };

  renderDriverTypes = driver => {
    const {
      app: {
        api: { driversDetails }
      }
    } = this.props;
    const details = driversDetails.get(driver);
    const drive = this.state.driverDrives.get(driver);

    if (details.status === 'success') {
      if (details.data.types) {
        const types = Object.keys(details.data.types);
        if (types.length > 0) {
          return (
            <Fragment>
              <MenuFilter available={types.length > 10} />
              {types.map(type => this.renderMetaWidgets(drive, type))}
            </Fragment>
          );
        }
      }
      return this.renderMenuError('No available types');
    } else if (details.status === 'error') {
      return this.renderMenuError(
        'An error has occurred when driver are loaded'
      );
    } else if (details.status === 'loading') {
      return this.renderMenuLoader();
    }
  };

  renderMetaWidgets = (drive, type) => (
    <Submenu key={type} label={type}>
      <MenuFilter available={Object.keys(metaWidgets).length > 10} />
      {Object.keys(metaWidgets).map(widget => (
        <MenuItem
          leftIcon={<Icon icon={metaWidgets[widget].icon} />}
          key={widget}
          onClick={() =>
            this.handlerSelectWidget(`${drive}${SEP}${type}${SEP}${widget}`)
          }
        >
          {metaWidgets[widget].title}
        </MenuItem>
      ))}
    </Submenu>
  );

  renderStaticWidgets = () =>
    staticWidgetsKeys.length > 0 && (
      <Submenu label="Open static widget...">
        <MenuFilter available={staticWidgetsKeys.length > 10} />
        {staticWidgetsKeys.map(widget => (
          <MenuItem
            leftIcon={<Icon icon={staticWidgets[widget].icon} />}
            key={widget}
            onClick={() => this.handlerSelectWidget(widget)}
          >
            {staticWidgets[widget].title}
          </MenuItem>
        ))}
      </Submenu>
    );

  state = {
    driverDrives: Map(),
    isDrivesInitialized: false
  };

  render() {
    return (
      <Menu>
        {this.renderDriversMenu()}
        {this.renderStaticWidgets()}
      </Menu>
    );
  }
}

const mapStateToProps = ({ app, dashboard }) => ({
  app,
  dashboard
});

const mapDispatchToProps = dispatch => ({
  updateWindows: dashboard => dispatch(updateWindows(dashboard))
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(ContextMenu);
