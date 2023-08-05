import React, { PureComponent } from 'react';
import { connect } from 'react-redux';
import { Mosaic, MosaicWindow } from 'react-mosaic-component';
import { MenuProvider } from 'react-ultimate-contextmenu';
import ContextMenu from './ContextMenu';
import { updateWindows } from './actions';
import { metaWidgets } from '../../widgets/meta';
import MetaProvider from '../../widgets/meta/meta-provider/MetaProvider';
import { staticWidgets } from '../../widgets/static';
import { SEP } from '../../constants/common';

import '@blueprintjs/core/lib/css/blueprint.css';
import '@blueprintjs/icons/lib/css/blueprint-icons.css';
import 'react-mosaic-component/react-mosaic-component.css';
import './css/mosaic-thin-theme.css';
import './css/dashboard.css';

class Dashboard extends PureComponent {
  renderTile = (id, path) => {
    let title;
    let component;
    if (id.indexOf(SEP) > -1) {
      const [drive, type, widget] = id.split(SEP);
      title = `[${drive}:${type}] ${metaWidgets[widget].title}`;
      component = (
        <MetaProvider drive={drive} type={type} widget={widget} {...this.props}>
          {metaWidgets[widget].component()}
        </MetaProvider>
      );
    } else {
      title = staticWidgets[id].title;
      component = staticWidgets[id].component(this.props);
    }
    return typeof this.props.dashboard === 'string' ? (
      component
    ) : (
      <MosaicWindow path={path} title={title} {...this.props}>
        {component}
      </MosaicWindow>
    );
  };

  render() {
    return (
      <div className="dashboard">
        <MenuProvider className="dashboard_content">
          <Mosaic
            className="mosaic-blueprint-theme mosaic-thin-theme"
            renderTile={(id, path) => this.renderTile(id, path)}
            value={this.props.dashboard}
            onChange={this.props.updateWindows}
          />
          <ContextMenu />
        </MenuProvider>
      </div>
    );
  }
}

const mapStateToProps = ({ dashboard }) => ({
  dashboard
});

const mapDispatchToProps = dispatch => ({
  updateWindows: dashboard => dispatch(updateWindows(dashboard))
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(Dashboard);
