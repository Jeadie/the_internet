import React from 'react';
import { render, screen } from '@testing-library/react';
import NewsApp from './NewsApp';
import { InternetContent } from './model';

test('renders learn react link', () => {
  render(<NewsApp isLocal={true}/>);
});
