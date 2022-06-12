import React from 'react';


interface IProps {
}

interface HomeAppState {
}

export default class HomeApp extends React.Component<IProps, HomeAppState> {
  constructor(props: IProps) {
    super(props)
  }

  render() {
    return (<p>I am on the home page.</p> )
  }
}