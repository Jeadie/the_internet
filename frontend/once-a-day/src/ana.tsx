import { API_KEY } from './constants';
import mixpanel from 'mixpanel-browser';

export interface NewsClickProperties {
  url: string;
  title?: string;
  source: string;
  subtype?: string
}

export default class Ana {  

  static setup(){
    mixpanel.init(API_KEY.MIXPANEL)
  }

  /**
   * Marks a page as visited.
   */
  static visited(page: string) {
    mixpanel.track(`visited-${page}`)
  }    

  /**
   * Maps a current user to an authenticated username (in AWS cognito). All 
   * events can then be tracked against a user, across devices, etc.
   * 
   * @param username Authenticated, unique username.
   */
  static identify_user(username: string) {
    mixpanel.identify(username)
  }

  /**
   * Tracks details of a piece of news content that a user clicks on (given redirect off page). 
   */
  static track_news_click(props: NewsClickProperties) {
    mixpanel.track("news-clicked", props)
  }
}