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
  showTableFilter: boolean
}

export class Table extends React.Component<TableProps, TableState> {
constructor(props: TableProps) {
    super(props)
    this.state = {content: [], filters: [], showTableFilter: false}
  }


  delay = (ms: number) => new Promise(res => setTimeout(res, ms));

  componentDidMount() {

    if (this.props.isLocal) {
      this.delay(1000).then( () => {
        this.setState({
          content: JSON.parse(local_data),
          showTableFilter: true
        })
      })
    } else {
      fetch("https://api.onceaday.link/api")
      .then(response => response.json())
      .then(data => {
        this.setState({content: data, showTableFilter: true})
      })
      .catch(err => console.log(err));
    }
  }

  getVisibleContent(state: TableState): InternetContent[] {
    /**
     * Returns the content that should be visible to the user. 
     * 
     * Content will be visible iff
     *   1. When filter keys are present/selected, the content has a filter key within the selected set.
     *   2. The URL of the internet content is not already in the visible content (i.e. duplicate 
     *        external URLs are removed; this can occur when multiple sources have the same content)
     */
    const {content, filters} = this.state
    const visibleContent = filters.length > 0 ? content.filter((x) => filters.includes(getInternetContentFilterKey(x)) ) : content

    const urlToVisibleContent = new Map(visibleContent.map(item =>[item.url, item]))    
     return Array.from(urlToVisibleContent.values()).sort(() => (Math.random() > .5) ? 1 : -1)
    
  }

  getFilterKeys(state: TableState): string[] {
    /**
     * Returns the possible content filter keys from the current Internet Content.
     */
    return Array.from(new Set(this.state.content.map((c) => getInternetContentFilterKey(c))))
  }


  render() {
    const visibleContent = this.getVisibleContent(this.state)
    return (
        <div>
            <TableFilter isDisabled={!this.state.showTableFilter} onChange={(values: string[]) => {this.setState({filters: values})}} sources={this.getFilterKeys(this.state)}/>
            <div className="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 lg:mx-4 md:mx-2">
                {visibleContent.map((c) => (<Content news={c} /> ))}
            </div>
        </div>
    );
  }
}
