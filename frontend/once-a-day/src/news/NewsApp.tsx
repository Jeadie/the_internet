import React from 'react';
import './App.css';
import { InternetContent } from './model';
import { local_data } from './local_data';
import { NewsAppHeader } from './NewsAppHeader';
import { Table } from './Table';

interface IProps {
  isLocal: boolean
}

interface NewsAppState {
  content: InternetContent[]
}

export default class NewsApp extends React.Component<IProps, NewsAppState> {
  constructor(props: IProps) {
    super(props)
    this.state = {content: []}
  }

  componentDidMount() {
    if (this.props.isLocal) {
      this.setState({
        content: JSON.parse(local_data)
      })
    } else {
      fetch("https://api.onceaday.link/api")
      .then(response => response.json())
      .then(data => {
        this.setState({content: data})
      })
      .catch(err => console.log(err));
    }
  }

  render() {
    const {content} = this.state
    return (
      <div className="App">
        <NewsAppHeader/>
          <div className="py-2 flex flex-row">
          <div className="xl:basis-1/6 lg:basis-1/6"></div>
            <Table isLocal={this.props.isLocal}/>
            <div className="xl:basis-1/6 lg:basis-1/6"></div>
          </div>
          
        </div>
    );
  }
}
