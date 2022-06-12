import './App.css';
import { getInternetContentFilterKey, InternetContent } from './model';


interface ContentProps {
    news: InternetContent
  }

export function Content({ news }: ContentProps) {
    return (
        <article className="col-span-1 p-6 my-2 mx-2 bg-white sm:p-8 rounded-xl ring ring-test-50 hover:bg-test-50">
            <div className="flex items-start">
        
            <div className="sm:ml-8">
                <strong className="rounded border border-test-500 bg-test-500 px-3 py-1.5 text-[10px] font-medium text-white">
                { getInternetContentFilterKey(news) }
                </strong>
        
                <h2 className="mt-4 text-lg font-medium sm:text-xl">
                <a href={news.url} className="hover:underline">  {news.title} </a>
                </h2>
        
                <p aok-hidden={news.description!=""} className="mt-1 text-sm text-gray-700"> { news.description } </p>
        
                <div className="mt-4 sm:flex sm:items-center sm:gap-2">
                <div className="flex items-center text-gray-500">
                    <p className="ml-1 text-xs font-medium">{ new Date(news.timestamp * 1000).toDateString() }</p>
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