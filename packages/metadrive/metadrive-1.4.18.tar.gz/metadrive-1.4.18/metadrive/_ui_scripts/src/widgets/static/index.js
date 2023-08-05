import React from 'react';
import { IconNames } from '@blueprintjs/icons';
import GithubUSer from './github-user/GithubUser';
import Clock from './clock/Clock';

/**
 * widget types
 */
export const STATIC_GITHUB_USER = 'STATIC_GITHUB_USER';
export const STATIC_CLOCK = 'STATIC_CLOCK';

/**
 * widget creators
 */
export const staticWidgets = {
  [STATIC_GITHUB_USER]: {
    icon: IconNames.USER,
    title: 'GitHub User',
    component: ({ location, history }) => (
      <GithubUSer location={location} history={history} />
    )
  },
  [STATIC_CLOCK]: {
    icon: IconNames.TIME,
    title: 'Clock',
    component: () => <Clock />
  }
};
