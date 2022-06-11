import React from 'react';
import './App.css';
import { InternetContent, getInternetContentFilterKey } from './model';
import { local_data } from './local_data';
import { Content } from './Content';
import { TableFilter } from "./TableFilter"


interface TableProps {
  isLocal: boolean
}

interface TableState {
  content: InternetContent[]
  filters: string[]
}

export class Table extends React.Component<TableProps, TableState> {
constructor(props: TableProps) {
    super(props)
    this.state = {content: [], filters: []}
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
    const {content, filters} = this.state
    const visibleContent = filters.length > 0 ? content.filter((x) => filters.includes(getInternetContentFilterKey(x)) ) : content
    console.log(visibleContent.length, filters)
    return (
        <div>
            <TableFilter
                onChange={(values: string[]) => {this.setState({filters: values})}}
                sources={Array.from(new Set(content.map((c) => getInternetContentFilterKey(c))))}
            />
            <div className="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 lg:mx-4 md:mx-2">
                {visibleContent.map((c) => (
                <Content news={c} />
                ))}
            </div>
        </div>
    );
  }
}
