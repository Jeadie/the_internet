import React from 'react';
import logo from './logo.svg';
import './App.css';
import { InternetContent } from './model';
import { render } from '@testing-library/react';


function AppHeader() {
    return (
      <div className="max-w-xl mx-auto text-center">
        <h1 className="text-3xl font-extrabold sm:text-5xl">
          The Internet
        </h1>
        <p className="mt-4 sm:leading-relaxed sm:text-xl">
            The entire internet in one place.
          </p>
    </div>
    )
  }

interface ContentProps {
  news: InternetContent
}


function Content({ news }: ContentProps) {
  return (
    <article className="col-span-1 p-6 my-2 mx-2 bg-white sm:p-8 rounded-xl ring ring-indigo-50 hover:bg-indigo-50">
        <div className="flex items-start">
      
          <div className="sm:ml-8">
            <strong className="rounded border border-indigo-500 bg-indigo-500 px-3 py-1.5 text-[10px] font-medium text-white">
              { news.location }
            </strong>
      
            <h2 className="mt-4 text-lg font-medium sm:text-xl">
              <a href={news.url} className="hover:underline">  {news.title} </a>
            </h2>
      
            <p aok-hidden={news.description!=""} className="mt-1 text-sm text-gray-700"> { news.description } </p>
      
            <div className="mt-4 sm:flex sm:items-center sm:gap-2">
              <div className="flex items-center text-gray-500">
                <p className="ml-1 text-xs font-medium">{ news.timestamp }</p>
              </div>
              <span aok-hidden={news.comments > 0 || news.upvotes > 0} className="hidden sm:block" aria-hidden="true">&middot;</span>
              

              <p className="mt-2 text-xs font-medium text-gray-500 sm:mt-0">
                  Comments <a>{ news.comments } </a>,
                  Upvotes <a >{ news.upvotes }</a>,
              </p>
            </div>
          </div>
          </div>
    </article>
  )
}

export default class App extends React.Component {
  content: InternetContent[]

  constructor() {
    super({})
    this.content = JSON.parse('[{"url":"https://github.com/Jeadie","timestamp":1654067172097,"location":"Github","title":"Jack Eadie","description":"Software engineer at Amazon. Giving people groceries.","mainCategory":"Profile","upvotes":4,"comments":6,"imageSourceUrl":"https://avatars.githubusercontent.com/u/23766767?v=4"}]')
  }

  // componentDidMount() {
  //   fetch(ENDPOINT)
  //   .then(res => res.json())
  //   .then((data) => {
  //     this.setState({ contacts: data })
  //   })
  //   .catch(console.log)
  // }

  render() {
    return (
      <div className="App">
        <AppHeader/>
        <div className="grid sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 lg:mx-4 md:mx-2">
          {this.content.map((c) => (
            <Content news={c} />
          ))}
        </div>
      </div>
    );
  }
}
