import Ana from '../ana';
import './App.css';
import { getInternetContentFilterKey, InternetContent } from './model';

export const openInNewTab = (url: string): void => {
    // Avoid security problems with: `noopener,noreferrer`
    const newWindow = window.open(url, '_blank', 'noopener,noreferrer')
    if (newWindow) newWindow.opener = null
  }

  
interface ContentProps {
    news: InternetContent
  }


export function Content({ news }: ContentProps) {
    const clicked = () => {
        openInNewTab(news.url);
        Ana.track_news_click({
            url: news.url,
            title: news.title,
            source: news.location,
            subtype: news.mainCategory
        })
    }
    return (
        <article onClick={() => clicked()}  className="news-content shadow-lg hover:shadow-2xl col-span-1 p-6 my-2 mx-2 bg-white sm:p-8 rounded-xl ring ring-test-50 hover:bg-test-50">
            <div className="flex">
        
            <div className="sm:ml-8">
                <strong className='rounded border border-test-500 bg-test-500 px-3 py-1.5 text-[10px] font-medium text-white'>
                    {/* <strong > */}
                    { getInternetContentFilterKey(news) }
                    {/* </strong> */}
                </strong>
        
                <h2 className="mt-4 text-lg font-medium sm:text-xl">

                {/* No href. openInNewTab() for whole card. Avoid double redirect. */}
                <a className="hover:underline">  {news.title} </a>
                </h2>
        
                <p aok-hidden={news.description!=""} className="mt-1 text-sm text-gray-700 hover:text-clip">{news.description}</p>
        
                <div className="mt-4 sm:flex sm:items-center sm:gap-2">
                <div className="flex items-center text-gray-500 pr-2 ">
                    <p className="ml-1 text-xs font-medium">{ new Date(news.timestamp * 1000).toDateString() }</p>
                </div>
                {(news.comments > 0 || news.upvotes > 0) &&  (
                    <div>
                        <p className="mt-2 text-xs font-medium text-gray-500 sm:mt-0"> Comments: { news.comments }, Upvotes: { news.upvotes }</p>
                    </div>
                )}
                </div>
            </div>
            </div>
        </article>
    )
}