import {
  Corner,
  getPathToCorner,
  getNodeAtPath,
  getOtherDirection,
  updateTree
} from 'react-mosaic-component';

/**
 * Check opened or not widget
 * @param widget - widget's id
 * @param dashboard - state of dashboard
 */
export function widgetIsOpened(widget, dashboard = null) {
  if (dashboard) {
    if (typeof dashboard === 'string') {
      return dashboard === widget;
    }
    return (
      widgetIsOpened(widget, dashboard.first) ||
      widgetIsOpened(widget, dashboard.second)
    );
  }
  return false;
}

/**
 * Open widget
 * @param widget - widget's id
 * @param dashboard - state of dashboard
 */
export function openWidget(widget, dashboard = null) {
  if (dashboard) {
    const path = getPathToCorner(dashboard, Corner.BOTTOM_RIGHT);
    const parent = getNodeAtPath(dashboard, path.slice(0, -1));
    const direction = parent ? getOtherDirection(parent.direction) : 'row';
    const first = getNodeAtPath(dashboard, path);
    const second = widget;

    return updateTree(dashboard, [
      {
        path,
        spec: {
          $set: {
            direction,
            first,
            second
          }
        }
      }
    ]);
  }
  return widget;
}
