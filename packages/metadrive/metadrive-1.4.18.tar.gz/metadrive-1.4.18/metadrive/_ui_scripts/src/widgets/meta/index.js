import React from 'react';
import { IconNames } from '@blueprintjs/icons';
import Search from './search/Search';

/**
 * widget types
 */
export const META_SEARCH = 'META_SEARCH';

/**
 * widget creators
 */
export const metaWidgets = {
  [META_SEARCH]: {
    title: 'Search',
    icon: IconNames.SEARCH,
    component: () => <Search />
  }
};
